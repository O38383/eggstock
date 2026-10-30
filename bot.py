"""
Steal An Egg - Stock Radar Bot
Listens to a Discord channel where SenZ V2 posts spawn alerts,
parses the embeds, tracks running stats, and serves them as JSON
over a small HTTP API for an OBS overlay to poll.
"""

import os
import re
import json
import asyncio
import logging
from datetime import datetime, timezone
from collections import deque
from pathlib import Path

import discord
from discord import app_commands
import aiohttp
from aiohttp import web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("steal-egg-bot")

# ---------- Config (from environment variables) ----------
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
STOCK_NOTIFY_CHANNEL_ID = int(os.environ["STOCK_NOTIFY_CHANNEL_ID"])
LAST_SEEN_CHANNEL_ID = int(os.environ.get("LAST_SEEN_CHANNEL_ID", "0") or 0)
SENZ_BOT_USER_ID = os.environ.get("SENZ_BOT_USER_ID")  # optional, tighten matching if set
PORT = int(os.environ.get("PORT", "8080"))
GAP_WINDOW_SIZE = int(os.environ.get("GAP_WINDOW_SIZE", "20"))
FALLBACK_INTERVAL_SECONDS = int(os.environ.get("FALLBACK_INTERVAL_SECONDS", "456"))
# How many messages to scan from #stock-notify on startup to bootstrap history.
STOCK_HISTORY_LIMIT = int(os.environ.get("STOCK_HISTORY_LIMIT", "100"))
OVERLAY_DIR = Path(__file__).parent / "overlay"
WEBSITE_DIR = Path(__file__).parent / "website"

# Auto-assign role on member join (default: 👥 Member ID 1546502687451910196)
AUTO_ASSIGN_ROLE_ID = int(os.environ.get("AUTO_ASSIGN_ROLE_ID", "1546502687451910196") or 1546502687451910196)
AUTO_ASSIGN_ROLE_NAME = os.environ.get("AUTO_ASSIGN_ROLE_NAME", "Member")

# Roblox universe ID for "Steal An Egg" (10563114921).
ROBLOX_UNIVERSE_ID = int(os.environ.get("ROBLOX_UNIVERSE_ID", "10563114921"))
ROBLOX_PLACE_ID = int(os.environ.get("ROBLOX_PLACE_ID", "107778070777162"))
ROBLOX_POLL_SECONDS = int(os.environ.get("ROBLOX_POLL_SECONDS", "60"))

# ---------- Discord OAuth2 & guilds.join Config ----------
import oauth_db
oauth_db.init_db()

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "1434388617676984392")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET", "S3V7qmk0oZG3umDdCuiE1abqeNq_DthB")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI", "https://eggstock.xyz/api/auth/discord/callback")
DISCORD_GUILD_ID = os.environ.get("DISCORD_GUILD_ID", "")
OAUTH_SCOPES = "identify guilds.join"

_active_user_sessions = {}  # session_token -> user_dict
_oauth_states = {}  # state -> timestamp

# ---------- Security config ----------
import secrets as _secrets
# Secret token required on /api/status — set API_TOKEN in Railway env vars.
# If not set, a random one is generated each deploy (locks out scrapers who
# don't have the current token).
API_TOKEN = os.environ.get("API_TOKEN") or _secrets.token_hex(32)
log.info(f"API token loaded (first 8 chars): {API_TOKEN[:8]}...")

# Allowed origins for CORS (eggstock.xyz + localhost dev)
ALLOWED_ORIGINS = {
    "https://eggstock.xyz",
    "https://www.eggstock.xyz",
    "https://ideal-trust-production-6d45.up.railway.app",
    "https://divine-gentleness-production-c60f.up.railway.app",
    "https://eggstock-web-production.up.railway.app",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
}
# Rate limit: max requests per IP per window
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "60"))      # seconds
RATE_LIMIT_MAX = int(os.environ.get("RATE_LIMIT_MAX", "300"))           # requests per window
RATE_LIMIT_API_MAX = int(os.environ.get("RATE_LIMIT_API_MAX", "120"))   # /api/*
# Max request body size (prevent abuse on POST if any future routes)
MAX_REQUEST_SIZE = 1024  # 1 KB — we only serve GET requests

# ---------- In-memory state ----------
state = {
    "session_drops": 0,
    "session_started_at": datetime.now(timezone.utc).isoformat(),
    "last_drop_time": None,
    "last_drop": None,
    "rarity_counts": {"secret": 0, "eternal": 0, "divine": 0},
    "since_rarity": {"secret": None, "eternal": None, "divine": None},
    "recent_drops": deque(maxlen=50),
    "last_seen_snapshot": None,

    "gaps_overall": deque(maxlen=GAP_WINDOW_SIZE),
    "gaps_by_rarity": {
        "secret": deque(maxlen=GAP_WINDOW_SIZE),
        "eternal": deque(maxlen=GAP_WINDOW_SIZE),
        "divine": deque(maxlen=GAP_WINDOW_SIZE),
    },
    "last_drop_ts_overall": None,
    "last_drop_ts_by_rarity": {"secret": None, "eternal": None, "divine": None},
    "last_wave_ts_overall": None,
    "last_wave_ts_by_rarity": {"secret": None, "eternal": None, "divine": None},

    # Dedup guard: (rarity, egg, location) -> unix ts it was last recorded.
    # Prevents the same spawn being counted twice if SenZ V2 double-posts,
    # retries, or if a message somehow gets processed more than once.
    "_recent_signatures": {},
    "playing_now": None,
    "playing_now_updated_at": None,
    "discord_members": None,
    "discord_online": None,
}

DEDUP_WINDOW_SECONDS = int(os.environ.get("DEDUP_WINDOW_SECONDS", "600"))
WAVE_CLUSTER_WINDOW_SECONDS = int(os.environ.get("WAVE_CLUSTER_WINDOW_SECONDS", "90"))
MIN_WAVE_GAP_SECONDS = int(os.environ.get("MIN_WAVE_GAP_SECONDS", "120"))

# ---------- Parsing ----------
# Example title formats seen from SenZ V2:
#   "Secret Egg Spawned!! - 8:39 AM"
#   "Eternal Egg Spawned!! - 9:55 PM"
#   "Divine Egg Spawned!! - ..."
TITLE_RE = re.compile(r"(Secret|Eternal|Divine)\s+Egg\s+Spawned", re.IGNORECASE)

# IMPORTANT: these must NOT be applied via naive "split on first colon" logic.
# Real messages look like: "<:Yeti:1544970985315504190>**Egg:** Yeti" -- the
# emoji tag itself contains colons, so a plain split(":", 1) grabs junk from
# inside the emoji tag instead of the real value after "Egg:"/"Location:".
# These regexes anchor on the literal "**Egg:**" / "**Location:**" markers
# and take everything after them instead.
FIELD_RE = re.compile(r"\*\*Egg:\*\*\s*(.+)", re.IGNORECASE)
LOCATION_RE = re.compile(r"\*\*Location:\*\*\s*(.+)", re.IGNORECASE)
ALLOWED_RARITIES = {"secret", "eternal", "divine"}


def sanitize_drop_field(val: str, max_len: int = 64) -> str:
    """Sanitize strings extracted from Discord embeds to prevent injection or corruption."""
    if not val:
        return "Unknown"
    # Strip HTML-like tags
    cleaned = re.sub(r"<[^>]+>", "", val)
    # Strip non-printable and control characters
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    # Strip markdown syntax
    cleaned = cleaned.replace("*", "").replace("`", "").replace("_", "")
    cleaned = cleaned.strip()
    return cleaned[:max_len] if cleaned else "Unknown"


def parse_embed(embed: discord.Embed):
    """Extract rarity, egg name, and location from a SenZ V2 spawn embed with strict sanitization."""
    title = embed.title or ""
    m = TITLE_RE.search(title)
    if not m:
        return None
    rarity = m.group(1).lower()
    if rarity not in ALLOWED_RARITIES:
        return None

    text_blob = embed.description or ""
    for field in embed.fields:
        text_blob += f"\n{field.name}: {field.value}"

    egg_match = FIELD_RE.search(text_blob)
    loc_match = LOCATION_RE.search(text_blob)

    egg_name = sanitize_drop_field(egg_match.group(1) if egg_match else "")
    location = sanitize_drop_field(loc_match.group(1) if loc_match else "")

    return {
        "rarity": rarity,
        "egg": egg_name,
        "location": location,
    }


# Known pet to world mappings in Steal An Egg
PET_WORLD_MAP = {
    "Kitsune": "Cherry Blossom",
    "Unicorn": "Forest",
    "Nightflame": "Volcano",
    "Phoenix": "Volcano",
    "Eternal Lunar Dragon": "Cosmic",
    "Oni Tiger": "Cherry Blossom",
    "Mosasaurus": "Prehistoric",
    "Ice Dragon": "Snow",
    "Lava Dragon": "Volcano",
    "Gorilla King": "Jungle",
    "El Maja": "Desert",
    "Cerberus": "Volcano",
    "Mutant Shark": "Titan Temple",
    "Stag": "Forest",
    "Kraken": "Abyss Ocean",
    "Tralaledon": "Prehistoric",
    "Cosmic Dragon": "Cosmic",
    "Cosmic Skeleton Boss": "Cosmic",
    "Yeti": "Snow",
    "TRex": "Prehistoric",
    "Snake King": "Desert",
    # Angels & Demons Update
    "Pure Jellyfish": "Angels",
    "Centaur": "Angels",
    "Pegasus": "Angels",
    "ArchAngel": "Angels",
    "Holy Peacock": "Angels",
    "Sacred Moth": "Angels",
    "Light Dove": "Angels",
    "Winged Lamb": "Angels",
    "Gargoyle": "Demons",
    "RazorFang": "Demons",
    "Skeleton Horse": "Demons",
    "World Burner": "Demons",
    "Demon Hound": "Demons",
    "Imp": "Demons",
    "Flame Sprite": "Demons",
    "Toro": "Demons",
    "Equinox": "Angels & Demons",
    "Aetheron": "Angels & Demons",
    # Update 7 Enchanted Forest (Verified Official Roster)
    "Prism Gecko": "Enchanted Forest",
    "Petal Beetle": "Enchanted Forest",
    "Enchanted Bluejay": "Enchanted Forest",
    "Astral Jackalope": "Enchanted Forest",
    "Spirit Panda": "Enchanted Forest",
    "Starry Fox": "Enchanted Forest",
    "Celestial Sunlion": "Enchanted Forest",
    "Royal Skywhale": "Enchanted Forest",
    # Halloween Event Update Biomes (Verified Official Roster)
    "Whiskers": "Graveyard",
    "Jesterpop": "Graveyard",
    "Candlefang": "Graveyard",
    "Spirit Knight": "Graveyard",
    "Graveyard Brute": "Graveyard",
    "Ghost Reaper": "Graveyard",
    "Hooded Gerbil": "Haunted Swamp",
    "Toadstool": "Haunted Swamp",
    "Patchwork Imp": "Haunted Swamp",
    "Haunted Scorpio": "Haunted Swamp",
    "BloodBloom": "Haunted Swamp",
    "Shelltide Voyager": "Haunted Swamp",
    "Mimic Chest": "Abandoned Manor",
    "Crowshade": "Abandoned Manor",
    "Hexed Pumpkin": "Abandoned Manor",
    "Werewolf": "Abandoned Manor",
    "Gorillastein": "Abandoned Manor",
    "Voidseer Pumpkin": "Abandoned Manor",
    # Event Spawns
    "Blood Moon": "Events",
    "Pumpkin Moon": "Events",
    "Butterfly Bloom": "Events",
    "Phantom Express": "Events",
    "Halloween Egg": "Events",
}


def extract_message_text(message: discord.Message) -> str:
    """Recursively extract all text content from a discord.Message across content, components, and embeds."""
    parts = []
    if message.content:
        parts.append(message.content)

    def walk_component(comp):
        content = getattr(comp, "content", None)
        if content:
            parts.append(str(content))
        children = getattr(comp, "children", None)
        if children:
            for child in children:
                walk_component(child)

    for comp in getattr(message, "components", []):
        walk_component(comp)

    for embed in getattr(message, "embeds", []):
        if embed.title:
            parts.append(embed.title)
        if embed.description:
            parts.append(embed.description)
        for field in embed.fields:
            if field.name:
                parts.append(field.name)
            if field.value:
                parts.append(field.value)

    return "\n".join(parts)


async def fetch_message_raw(channel_id: int, message_id: int) -> dict:
    """Fallback fetch directly via Discord REST API v10 to bypass any library component parsing gaps."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}"
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    log.warning(f"fetch_message_raw HTTP {resp.status} for msg {message_id}")
    except Exception as exc:
        log.warning(f"fetch_message_raw error for msg {message_id}: {exc}")
    return {}


async def fetch_channel_messages_raw(channel_id: int, limit: int = 10) -> list:
    """Fallback fetch messages directly via Discord REST API v10."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}"
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    log.warning(f"fetch_channel_messages_raw HTTP {resp.status} for channel {channel_id}")
    except Exception as exc:
        log.warning(f"fetch_channel_messages_raw error for channel {channel_id}: {exc}")
    return []


def extract_text_from_raw(data: dict) -> str:
    """Recursively extract all text content from raw Discord API message JSON (handling type 17/10 components)."""
    parts = []
    if data.get("content"):
        parts.append(str(data["content"]))

    def walk_raw_components(comps):
        for c in comps:
            if isinstance(c, dict):
                if c.get("content"):
                    parts.append(str(c["content"]))
                if c.get("components"):
                    walk_raw_components(c["components"])

    walk_raw_components(data.get("components", []))

    for embed in data.get("embeds", []):
        if embed.get("title"):
            parts.append(str(embed["title"]))
        if embed.get("description"):
            parts.append(str(embed["description"]))
        for field in embed.get("fields", []):
            if field.get("name"):
                parts.append(str(field["name"]))
            if field.get("value"):
                parts.append(str(field["value"]))

    return "\n".join(parts)


def parse_drop_message(message: discord.Message = None, raw_text: str = None):
    """Parse a spawn alert message whether formatted as an embed, component, or raw text."""
    if not raw_text and message:
        # 1. Check standard embeds first
        for embed in getattr(message, "embeds", []):
            parsed = parse_embed(embed)
            if parsed:
                return parsed
        full_text = extract_message_text(message)
    else:
        full_text = raw_text or ""

    m = TITLE_RE.search(full_text)
    if m:
        rarity = m.group(1).lower()
        if rarity in ALLOWED_RARITIES:
            egg_match = FIELD_RE.search(full_text)
            loc_match = LOCATION_RE.search(full_text)
            egg_name = sanitize_drop_field(egg_match.group(1) if egg_match else "")
            location = sanitize_drop_field(loc_match.group(1) if loc_match else "")
            if not location or location == "Unknown":
                location = PET_WORLD_MAP.get(egg_name, "Active World")
            return {
                "rarity": rarity,
                "egg": egg_name,
                "location": location,
            }
    return None


# ---------- Last-seen embed parsing (real format captured from SenZ V2) ----------
# More lenient: handles em-dash (—) or regular dash (-), optional emoji tag,
# and variations in spacing or markdown formatting.
SECTION_RE = re.compile(
    r"(?:###\s*)?(?:<:\w+:\d+>\s*)?(Divine|Eternal|Secret)\s*[—\-]+\s*Last\s*Seen",
    re.IGNORECASE,
)
# Match item lines: optional emoji, egg name, then a Discord timestamp <t:UNIX:R>
ITEM_RE = re.compile(r"(?:<:\w+:\d+>\s*)?(.+?)\s*[—\-]+\s*<t:(\d+):R>")


def parse_last_seen(content: str):
    sections = {"divine": [], "eternal": [], "secret": []}
    current = None
    for line in content.splitlines():
        line = line.strip()
        sec_match = SECTION_RE.search(line)
        if sec_match:
            current = sec_match.group(1).lower()
            continue
        if current:
            item_match = ITEM_RE.search(line)
            if item_match:
                name, ts = item_match.group(1).strip(), int(item_match.group(2))
                sections[current].append({"name": name, "ts": ts})
    return sections


def apply_last_seen(sections: dict):
    now_iso = datetime.now(timezone.utc).isoformat()
    state["last_seen_snapshot"] = {
        "updated_at": now_iso,
        "sections": sections,
    }

    all_items = []
    for rarity in ("divine", "eternal", "secret"):
        items = sections.get(rarity, [])
        if not items:
            continue

        timestamps = sorted(item["ts"] for item in items)
        if len(state["gaps_by_rarity"][rarity]) == 0 and len(timestamps) >= 2:
            for prev_ts, next_ts in zip(timestamps, timestamps[1:]):
                gap = next_ts - prev_ts
                if gap > 0:
                    state["gaps_by_rarity"][rarity].append(gap)
                    state["gaps_overall"].append(gap)
            if state["last_drop_ts_by_rarity"][rarity] is None:
                state["last_drop_ts_by_rarity"][rarity] = timestamps[-1]
            if state["last_drop_ts_overall"] is None or timestamps[-1] > state["last_drop_ts_overall"]:
                state["last_drop_ts_overall"] = timestamps[-1]

        most_recent_ts = timestamps[-1]
        most_recent_iso = datetime.fromtimestamp(most_recent_ts, tz=timezone.utc).isoformat()
        existing = state["since_rarity"].get(rarity)
        if not existing or most_recent_iso > existing:
            state["since_rarity"][rarity] = most_recent_iso

        for item in items:
            all_items.append({
                "name": item["name"],
                "ts": item["ts"],
                "rarity": rarity,
            })

    # If recent_drops is empty or new snapshot has data, update state
    if all_items:
        all_items.sort(key=lambda x: x["ts"], reverse=True)
        latest = all_items[0]
        latest_iso = datetime.fromtimestamp(latest["ts"], tz=timezone.utc).isoformat()

        # Update last_drop if we have no last_drop or this snapshot has a newer/equal drop
        if state["last_drop_time"] is None or latest_iso >= state["last_drop_time"]:
            state["last_drop_time"] = latest_iso
            state["last_drop"] = {
                "rarity": latest["rarity"],
                "egg": latest["name"],
                "location": PET_WORLD_MAP.get(latest["name"], "Active World"),
            }

        # Seed recent_drops if empty
        if len(state["recent_drops"]) == 0:
            for item in all_items[:50]:
                iso_time = datetime.fromtimestamp(item["ts"], tz=timezone.utc).isoformat()
                loc = PET_WORLD_MAP.get(item["name"], "Active World")
                state["recent_drops"].append({
                    "time": iso_time,
                    "rarity": item["rarity"],
                    "egg": item["name"],
                    "location": loc,
                })

        if state["session_drops"] < len(all_items):
            state["session_drops"] = len(all_items)
        state["rarity_counts"]["secret"] = max(state["rarity_counts"]["secret"], len(sections.get("secret", [])))
        state["rarity_counts"]["eternal"] = max(state["rarity_counts"]["eternal"], len(sections.get("eternal", [])))
        state["rarity_counts"]["divine"] = max(state["rarity_counts"]["divine"], len(sections.get("divine", [])))

    log.info(f"Applied last-seen snapshot: divine={len(sections['divine'])} "
              f"eternal={len(sections['eternal'])} secret={len(sections['secret'])} | "
              f"seeded recent_drops={len(state['recent_drops'])}")


def _median(values):
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def get_wave_estimate(rarity: str = None):
    gaps = state["gaps_by_rarity"][rarity] if rarity else state["gaps_overall"]
    clean_gaps = [g for g in gaps if g >= MIN_WAVE_GAP_SECONDS]
    n = len(clean_gaps)

    if n == 0:
        return {
            "seconds": FALLBACK_INTERVAL_SECONDS,
            "sample_size": 0,
            "confidence": "none",
            "basis": "fallback",
        }

    seconds = _median(clean_gaps)
    if n < 3:
        confidence = "low"
    elif n < 8:
        confidence = "medium"
    else:
        confidence = "good"

    return {
        "seconds": round(seconds),
        "sample_size": n,
        "confidence": confidence,
        "basis": "observed",
    }


def record_drop(parsed: dict):
    now = datetime.now(timezone.utc)
    now_ts = now.timestamp()

    # Dedup guard: if we've seen this exact (rarity, egg, location) combo
    # very recently, treat it as a duplicate post/retry, not a new spawn.
    signature = (parsed["rarity"], parsed["egg"], parsed["location"])
    sigs = state["_recent_signatures"]
    last_seen_ts = sigs.get(signature)
    if last_seen_ts is not None and (now_ts - last_seen_ts) < DEDUP_WINDOW_SECONDS:
        log.info(f"Ignored duplicate drop within {DEDUP_WINDOW_SECONDS}s window: {parsed}")
        return
    sigs[signature] = now_ts
    # Keep this dict from growing forever: drop entries older than the window
    stale_cutoff = now_ts - DEDUP_WINDOW_SECONDS
    for sig, ts in list(sigs.items()):
        if ts < stale_cutoff:
            del sigs[sig]

    state["session_drops"] += 1
    state["last_drop_time"] = now.isoformat()
    state["last_drop"] = parsed
    state["recent_drops"].appendleft({**parsed, "time": now.isoformat()})
    state["last_drop_ts_overall"] = now_ts

    # --- Wave Clustering: cluster drops arriving in the same spawn wave ---
    last_wave = state.get("last_wave_ts_overall")
    if last_wave is None or (now_ts - last_wave) > WAVE_CLUSTER_WINDOW_SECONDS:
        # Start of a new spawn wave!
        if last_wave is not None:
            gap = now_ts - last_wave
            if gap >= MIN_WAVE_GAP_SECONDS:
                state["gaps_overall"].append(gap)
        state["last_wave_ts_overall"] = now_ts

    rarity = parsed["rarity"]
    if rarity in state["rarity_counts"]:
        state["rarity_counts"][rarity] += 1
        state["since_rarity"][rarity] = now.isoformat()
        state["last_drop_ts_by_rarity"][rarity] = now_ts

        last_wave_r = state.get("last_wave_ts_by_rarity", {}).get(rarity)
        if last_wave_r is None or (now_ts - last_wave_r) > WAVE_CLUSTER_WINDOW_SECONDS:
            if last_wave_r is not None:
                gap_r = now_ts - last_wave_r
                if gap_r >= MIN_WAVE_GAP_SECONDS:
                    state["gaps_by_rarity"][rarity].append(gap_r)
            if "last_wave_ts_by_rarity" not in state:
                state["last_wave_ts_by_rarity"] = {}
            state["last_wave_ts_by_rarity"][rarity] = now_ts

    log.info(
        f"Recorded drop: {parsed} | session_drops={state['session_drops']} | "
        f"overall_estimate={get_wave_estimate()}"
    )


# ---------- Roblox live player count ----------
import aiohttp as _aiohttp_client  # aiohttp is already a dependency (used for the web server)

_roblox_universe_id = None


async def _resolve_universe_id(session):
    """Resolve the Roblox universe ID."""
    global _roblox_universe_id
    if _roblox_universe_id is not None:
        return _roblox_universe_id
    if ROBLOX_UNIVERSE_ID:
        _roblox_universe_id = ROBLOX_UNIVERSE_ID
        log.info(f"Using configured Roblox universe id {_roblox_universe_id}")
        return _roblox_universe_id

    # Try the newer public endpoint first, fall back to the legacy one.
    urls_to_try = [
        f"https://apis.roblox.com/universes/v1/places/{ROBLOX_PLACE_ID}/universe",
        f"https://api.roblox.com/universes/get-universe-containing-place?placeId={ROBLOX_PLACE_ID}",
    ]
    last_exc = None
    for url in urls_to_try:
        try:
            async with session.get(url, timeout=_aiohttp_client.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                data = await resp.json()
                log.debug(f"Universe lookup raw response from {url}: {data}")
                # The newer endpoint returns {"universeId": 12345}
                # The legacy endpoint returns {"UniverseId": 12345}
                uid = data.get("universeId") or data.get("UniverseId")
                if uid is None:
                    log.warning(
                        f"Universe ID endpoint returned no universeId key. "
                        f"URL={url}  full response={data}"
                    )
                    continue  # try next URL
                _roblox_universe_id = uid
                log.info(
                    f"Resolved Roblox universe id {_roblox_universe_id} "
                    f"from place id {ROBLOX_PLACE_ID} via {url}"
                )
                return _roblox_universe_id
        except Exception as exc:
            log.warning(f"Universe ID lookup failed ({url}): {exc}")
            last_exc = exc

    # All attempts failed — keep _roblox_universe_id as None so we retry next poll.
    log.warning(
        f"Could not resolve universe ID for place {ROBLOX_PLACE_ID}. "
        f"Will retry in {ROBLOX_POLL_SECONDS}s. Last error: {last_exc}"
    )
    return None


async def _poll_roblox_players():
    async with _aiohttp_client.ClientSession() as session:
        while True:
            try:
                universe_id = await _resolve_universe_id(session)
                if universe_id is None:
                    # Resolution failed; warning already logged inside _resolve_universe_id.
                    pass
                else:
                    url = f"https://games.roblox.com/v1/games?universeIds={universe_id}"
                    async with session.get(url, timeout=_aiohttp_client.ClientTimeout(total=10)) as resp:
                        resp.raise_for_status()
                        payload = await resp.json()
                        games = payload.get("data") or []
                        if games:
                            count = games[0].get("playing")
                            state["playing_now"] = count
                            state["playing_now_updated_at"] = datetime.now(timezone.utc).isoformat()
                            log.info(f"Roblox playing_now = {count}")
            except Exception as exc:
                log.warning(f"Failed to fetch Roblox player count: {exc}")
                # Reset so _resolve_universe_id retries on the next cycle
                # (guards against a cached bad universe ID after a transient error).
                _roblox_universe_id = None
            await asyncio.sleep(ROBLOX_POLL_SECONDS)
            

async def _poll_discord_stats():
    """Poll official Discord invite API for real approximate member and online presence counts."""
    async with _aiohttp_client.ClientSession() as session:
        while True:
            try:
                invite_code = "Jmvam6Ktgm"
                url = f"https://discord.com/api/v10/invites/{invite_code}?with_counts=true"
                headers = {"User-Agent": "Mozilla/5.0"}
                async with session.get(url, headers=headers, timeout=_aiohttp_client.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        payload = await resp.json()
                        state["discord_members"] = payload.get("approximate_member_count")
                        state["discord_online"] = payload.get("approximate_presence_count")
                        log.info(f"Discord live stats: {state['discord_members']} members, {state['discord_online']} online")
            except Exception as exc:
                log.warning(f"Failed to fetch Discord stats from invite: {exc}")
            await asyncio.sleep(60)


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Required to detect member joins and auto-assign roles

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def get_auto_role(guild: discord.Guild) -> discord.Role | None:
    """Find the auto-assign role by ID or by common names (Member, Members, Verified, etc.)."""
    if not guild:
        return None
    global AUTO_ASSIGN_ROLE_ID
    if AUTO_ASSIGN_ROLE_ID:
        role = guild.get_role(AUTO_ASSIGN_ROLE_ID)
        if role:
            return role

    target_keywords = [
        AUTO_ASSIGN_ROLE_NAME.lower(),
        "member",
        "members",
        "egg hunter",
        "verified",
        "community",
    ]
    for r in guild.roles:
        if r.is_default():
            continue
        clean_name = re.sub(r"[^\w\s]", "", r.name).strip().lower()
        for target in target_keywords:
            if target == clean_name or target in clean_name.split():
                return r
    return None


# ── Ping & Onboarding Roles Config ──
PING_ROLES_CONFIG = [
    {"name": "Member", "color": discord.Color.from_rgb(46, 204, 113), "mentionable": False, "hoist": False},
    {"name": "Announcements", "color": discord.Color.from_rgb(233, 30, 99), "mentionable": True, "hoist": False},
    {"name": "Updates", "color": discord.Color.from_rgb(244, 123, 103), "mentionable": True, "hoist": False},
    {"name": "Giveaways", "color": discord.Color.from_rgb(153, 170, 181), "mentionable": True, "hoist": False},
    {"name": "Leaks", "color": discord.Color.from_rgb(149, 165, 166), "mentionable": True, "hoist": False},
    {"name": "Events", "color": discord.Color.from_rgb(155, 89, 182), "mentionable": True, "hoist": False},
    {"name": "Polls", "color": discord.Color.from_rgb(176, 190, 197), "mentionable": True, "hoist": False},
]


async def setup_ping_roles(guild: discord.Guild) -> tuple[list[str], list[str], list[str]]:
    """Create or verify the 7 ping/onboarding roles matching the EggStock community setup."""
    created = []
    existed = []
    failed = []

    existing_roles = {r.name.lower(): r for r in guild.roles}

    for cfg in PING_ROLES_CONFIG:
        role_name = cfg["name"]
        role_lower = role_name.lower()

        if role_lower in existing_roles:
            role = existing_roles[role_lower]
            existed.append(f"@{role.name}")
            # If not mentionable and it's a ping role, make it mentionable
            if cfg["mentionable"] and not role.mentionable:
                try:
                    await role.edit(mentionable=True)
                except Exception:
                    pass
        else:
            try:
                new_role = await guild.create_role(
                    name=role_name,
                    color=cfg["color"],
                    mentionable=cfg["mentionable"],
                    hoist=cfg["hoist"],
                    reason="EggStock ping & onboarding role setup"
                )
                created.append(f"@{new_role.name}")
            except Exception as e:
                failed.append(f"{role_name} ({e})")

    return created, existed, failed


async def _background_sync_members(guild: discord.Guild, role: discord.Role):
    """Gently backfill existing members who joined before the auto-role was active."""
    try:
        log.info(f"[auto-role] Starting background backfill check for guild '{guild.name}'...")
        members = [m async for m in guild.fetch_members(limit=None)]
        missing = [m for m in members if not m.bot and role not in m.roles]
        if not missing:
            log.info(f"[auto-role] All {len(members)} members in '{guild.name}' already have '@{role.name}'.")
            return

        log.info(f"[auto-role] Found {len(missing)} member(s) missing '@{role.name}'. Backfilling...")
        assigned = 0
        for m in missing:
            try:
                await m.add_roles(role, reason="EggStock automatic startup backfill")
                assigned += 1
                await asyncio.sleep(0.12)
            except Exception as exc:
                log.warning(f"[auto-role] Could not assign role to {m}: {exc}")
        log.info(f"[auto-role] Background backfill complete: {assigned}/{len(missing)} members granted '@{role.name}' in '{guild.name}'.")
    except Exception as exc:
        log.warning(f"[auto-role] Background backfill failed: {exc}")


@client.event
async def on_member_join(member: discord.Member):
    """Automatically assign the basic member role to anyone who joins the server."""
    if member.bot:
        return

    guild = member.guild
    role = get_auto_role(guild)

    if not role:
        log.warning(
            f"[auto-role] No auto-assign role found in '{guild.name}' (id={guild.id}). "
            f"Create a role named '{AUTO_ASSIGN_ROLE_NAME}' or run /setrole."
        )
        return

    try:
        await member.add_roles(role, reason="EggStock auto-assign role on server join")
        log.info(f"[auto-role] Assigned role '@{role.name}' to new member {member} (id={member.id}) in '{guild.name}'")
    except discord.Forbidden:
        log.error(
            f"[auto-role] Permission denied: Cannot assign '@{role.name}' to {member}. "
            f"Make sure the bot has 'Manage Roles' permission and its role is positioned ABOVE '@{role.name}' in Server Settings -> Roles!"
        )
    except Exception as exc:
        log.error(f"[auto-role] Failed to assign '@{role.name}' to {member}: {exc}")


# ── Slash Commands ──
@tree.command(name="autorole", description="Check the status of the auto-assign role system and permissions.")
async def slash_autorole(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a Discord server.", ephemeral=True)
        return

    role = get_auto_role(interaction.guild)
    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)
    can_manage = bot_member.guild_permissions.manage_roles if bot_member else False
    hierarchy_ok = (getattr(bot_member.top_role, "position", 0) > getattr(role, "position", 0)) if (bot_member and role and bot_member.top_role) else False

    total_human = sum(1 for m in interaction.guild.members if not m.bot)
    with_role = sum(1 for m in interaction.guild.members if not m.bot and (role in m.roles if role else False))

    embed = discord.Embed(
        title="⚙️ EggStock Auto-Role System",
        color=0x00F0FF,
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(
        name="Target Role",
        value=f"**@{role.name}** (`ID: {role.id}`)" if role else f"❌ Role not found! Run `/setrole` or create `{AUTO_ASSIGN_ROLE_NAME}` in Server Settings.",
        inline=False
    )
    embed.add_field(
        name="Bot 'Manage Roles'",
        value="✅ Granted" if can_manage else "❌ Missing!",
        inline=True
    )
    embed.add_field(
        name="Role Hierarchy",
        value="✅ Bot is higher" if hierarchy_ok else f"❌ Bot role must be dragged ABOVE @{role.name if role else 'Member'}!",
        inline=True
    )
    embed.add_field(
        name="Member Coverage",
        value=f"**{with_role}/{total_human}** human members have role" if role else "N/A",
        inline=True
    )
    embed.add_field(
        name="Available Commands",
        value="• `/syncmembers` — Give the role to all existing members.\n• `/setrole [role]` — Change the auto-assign role.",
        inline=False
    )
    embed.set_footer(text="EggStock.xyz Discord System")
    await interaction.response.send_message(embed=embed)


@tree.command(name="syncmembers", description="Give the member role to all existing server members who don't have it.")
async def slash_syncmembers(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a Discord server.", ephemeral=True)
        return

    is_admin = (
        interaction.user.id == interaction.guild.owner_id
        or interaction.user.guild_permissions.administrator
        or interaction.user.guild_permissions.manage_roles
    )
    if not is_admin:
        await interaction.response.send_message("❌ You need the **Manage Roles** or **Administrator** permission to run this command.", ephemeral=True)
        return

    role = get_auto_role(interaction.guild)
    if not role:
        await interaction.response.send_message(
            f"❌ Could not find an auto-assign role.\n"
            f"Please create a role named **{AUTO_ASSIGN_ROLE_NAME}** or use `/setrole` to pick one!",
            ephemeral=True
        )
        return

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)
    can_manage = bot_member.guild_permissions.manage_roles if bot_member else False
    hierarchy_ok = (getattr(bot_member.top_role, "position", 0) > getattr(role, "position", 0)) if (bot_member and role and bot_member.top_role) else False

    if not can_manage:
        await interaction.response.send_message(
            "❌ The bot is missing the **Manage Roles** permission!\n"
            "Go to **Server Settings → Roles → EggStock Bot**, enable **Manage Roles**, and try again.",
            ephemeral=True
        )
        return

    if not hierarchy_ok:
        await interaction.response.send_message(
            f"❌ **Role Hierarchy Error:** The bot's role is below **@{role.name}**!\n"
            f"Go to **Server Settings → Roles**, drag the **EggStock Bot** role **ABOVE** **@{role.name}**, and try again.",
            ephemeral=True
        )
        return

    await interaction.response.defer(thinking=True)

    assigned_count = 0
    already_had = 0
    failed_count = 0

    try:
        members = [m async for m in interaction.guild.fetch_members(limit=None)]
    except Exception as exc:
        members = interaction.guild.members

    for m in members:
        if m.bot:
            continue
        if role in m.roles:
            already_had += 1
            continue
        try:
            await m.add_roles(role, reason="EggStock admin /syncmembers role backfill")
            assigned_count += 1
            await asyncio.sleep(0.12)
        except Exception as exc:
            log.warning(f"Failed to add role to {m}: {exc}")
            failed_count += 1

    embed = discord.Embed(
        title="✅ Auto-Role Sync Complete!",
        color=0x4EDEA3,
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(name="Target Role", value=f"**@{role.name}**", inline=True)
    embed.add_field(name="Newly Assigned", value=f"**{assigned_count}** members", inline=True)
    embed.add_field(name="Already Had Role", value=f"**{already_had}** members", inline=True)
    if failed_count:
        embed.add_field(name="Failed", value=f"**{failed_count}** members", inline=True)
    embed.set_footer(text="EggStock.xyz Discord System")
    await interaction.followup.send(embed=embed)


@tree.command(name="setrole", description="Set which role is automatically assigned to new and existing members.")
@app_commands.describe(role="Select the role to auto-assign to members")
async def slash_setrole(interaction: discord.Interaction, role: discord.Role):
    global AUTO_ASSIGN_ROLE_ID
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a Discord server.", ephemeral=True)
        return

    is_admin = (
        interaction.user.id == interaction.guild.owner_id
        or interaction.user.guild_permissions.administrator
        or interaction.user.guild_permissions.manage_roles
    )
    if not is_admin:
        await interaction.response.send_message("❌ You need **Manage Roles** or **Administrator** permission to change the auto-role.", ephemeral=True)
        return

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)
    if bot_member and bot_member.top_role.position <= role.position:
        await interaction.response.send_message(
            f"⚠️ **Role Hierarchy Warning:** The bot's role is below or equal to **@{role.name}**.\n"
            f"Please drag the bot's role **ABOVE** **@{role.name}** in Server Settings → Roles so it can assign it.",
            ephemeral=True
        )
        return

    AUTO_ASSIGN_ROLE_ID = role.id
    embed = discord.Embed(
        title="✅ Auto-Assign Role Updated",
        description=f"New members will now automatically receive **@{role.name}** (`ID: {role.id}`) when joining.\n\nRun `/syncmembers` to backfill existing members with this role now!",
        color=0x4EDEA3,
        timestamp=datetime.now(timezone.utc)
    )
    await interaction.response.send_message(embed=embed)


@tree.command(name="oauthstats", description="View authorized Discord OAuth2 member backup counts (Admin Only, Ephemeral).")
async def slash_oauthstats(interaction: discord.Interaction):
    """View authorized Discord OAuth2 member backup counts (Admin Only, Ephemeral)."""
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a Discord server.", ephemeral=True)
        return

    is_admin = (
        interaction.user.id == interaction.guild.owner_id
        or interaction.user.guild_permissions.administrator
        or interaction.user.guild_permissions.manage_guild
    )
    if not is_admin:
        await interaction.response.send_message("❌ You must be a Server Administrator to view OAuth stats.", ephemeral=True)
        return

    stats = oauth_db.get_oauth_stats()
    embed = discord.Embed(
        title="📊 EggStock OAuth2 Member Stats",
        description="🔒 *Confidential • Only you can see this*",
        color=0x00F0FF,
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(name="Total Authorized Users", value=f"**{stats['total_authorized']}** members", inline=True)
    embed.add_field(name="Auto-Joined to Server", value=f"**{stats['joined_guild']}** members", inline=True)
    embed.set_footer(text="EggStock 1-Click Discord Connect • eggstock.xyz")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="oauthcount", description="View authorized Discord OAuth2 member backup counts (Admin Only, Ephemeral).")
async def slash_oauthcount(interaction: discord.Interaction):
    """Alias for /oauthstats with ephemeral=True."""
    await slash_oauthstats(interaction)


@tree.command(name="setuproles", description="Create the 7 ping & onboarding roles (Announcements, Updates, Leaks, etc.)")
async def slash_setuproles(interaction: discord.Interaction):
    """Create the 7 ping & onboarding roles (Announcements, Updates, Leaks, Events, Polls, Giveaways, Member)."""
    if not interaction.guild:
        await interaction.response.send_message("❌ This command can only be used in a Discord server.", ephemeral=True)
        return

    is_admin = (
        interaction.user.id == interaction.guild.owner_id
        or interaction.user.guild_permissions.administrator
        or interaction.user.guild_permissions.manage_roles
    )
    if not is_admin:
        await interaction.response.send_message("❌ You must have **Manage Roles** or **Administrator** permission to set up roles.", ephemeral=True)
        return

    bot_member = interaction.guild.me or interaction.guild.get_member(client.user.id)
    if not bot_member or not bot_member.guild_permissions.manage_roles:
        await interaction.response.send_message(
            "❌ Bot requires the **Manage Roles** permission to create server roles.\n"
            "Go to **Server Settings → Roles → EggStock Bot**, enable **Manage Roles**, and try again!",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)
    created, existed, failed = await setup_ping_roles(interaction.guild)

    embed = discord.Embed(
        title="🎭 Ping & Onboarding Roles Setup",
        description="The 7 official community notification roles have been configured:",
        color=0x4EDEA3,
        timestamp=datetime.now(timezone.utc)
    )
    if created:
        embed.add_field(name="✅ Newly Created Roles", value="\n".join(created), inline=False)
    if existed:
        embed.add_field(name="ℹ️ Already Existed & Verified", value="\n".join(existed), inline=False)
    if failed:
        embed.add_field(name="⚠️ Failed to Create", value="\n".join(failed), inline=False)

    embed.add_field(
        name="📌 Next Step: Discord Onboarding",
        value="Go to **Server Settings → Onboarding → Questions** and add a question like:\n*\"Which notifications do you want?\"*\nAssign these roles as selectable answers!",
        inline=False
    )
    embed.set_footer(text="EggStock Role Manager • eggstock.xyz")
    await interaction.followup.send(embed=embed, ephemeral=True)


@tree.command(name="radar", description="Quick live spawn radar stats for Steal An Egg.")
async def slash_radar(interaction: discord.Interaction):
    last_drop = state.get("last_drop")
    players = state.get("playing_now")
    embed = discord.Embed(
        title="📡 EggStock Live Spawn Radar",
        url="https://eggstock.xyz",
        color=0x00F0FF,
        timestamp=datetime.now(timezone.utc)
    )
    if last_drop:
        embed.add_field(
            name="Last Observed Drop",
            value=f"**{last_drop.get('egg', 'Unknown')}** ({last_drop.get('rarity', 'Secret').capitalize()})\n📍 {last_drop.get('location', 'Unknown')}",
            inline=True
        )
    if players:
        embed.add_field(name="Roblox Players", value=f"🎮 {players:,}", inline=True)
    embed.add_field(name="Session Drops", value=f"{state.get('session_drops', 0)}", inline=True)
    embed.add_field(name="Live Website", value="[eggstock.xyz](https://eggstock.xyz)", inline=False)
    embed.set_footer(text="EggStock.xyz Live Radar")
    await interaction.response.send_message(embed=embed)


@client.event
async def on_ready():
    log.info(f"Logged in as {client.user} (id={client.user.id})")
    log.info(f"Watching channel id {STOCK_NOTIFY_CHANNEL_ID}")

    # Check auto-role status in connected guilds and trigger background backfill
    for g in client.guilds:
        role = get_auto_role(g)
        if role:
            bot_member = g.me or g.get_member(client.user.id)
            can_manage = bot_member.guild_permissions.manage_roles if bot_member else False
            hierarchy_ok = (getattr(bot_member.top_role, "position", 0) > getattr(role, "position", 0)) if (bot_member and bot_member.top_role) else False
            log.info(
                f"[auto-role] Guild '{g.name}': Target role '@{role.name}' (id={role.id}) | "
                f"manage_roles={can_manage} | hierarchy_ok={hierarchy_ok}"
            )
            if can_manage and hierarchy_ok:
                asyncio.create_task(_background_sync_members(g, role))
        else:
            log.warning(
                f"[auto-role] Guild '{g.name}': No role named '{AUTO_ASSIGN_ROLE_NAME}' found. "
                f"Create a role named '{AUTO_ASSIGN_ROLE_NAME}' in Discord or run /setrole."
            )

    # Sync slash commands immediately to all guilds and globally
    for g in client.guilds:
        try:
            tree.copy_global_to(guild=g)
            synced = await tree.sync(guild=g)
            log.info(f"[slash-commands] Synced {len(synced)} slash commands to guild '{g.name}' (id={g.id})")
        except Exception as exc:
            log.warning(f"[slash-commands] Failed to sync to guild '{g.name}': {exc}")
    try:
        global_synced = await tree.sync()
        log.info(f"[slash-commands] Synced {len(global_synced)} global slash commands")
    except Exception as exc:
        log.warning(f"[slash-commands] Failed to sync global slash commands: {exc}")

    # ── 1. Bootstrap from #last-seen-eggs (snapshot with real Unix timestamps) ──
    if LAST_SEEN_CHANNEL_ID:
        try:
            bootstrapped = False
            # 1a. Try via discord.py channel history
            try:
                ch = client.get_channel(LAST_SEEN_CHANNEL_ID) or await client.fetch_channel(LAST_SEEN_CHANNEL_ID)
                async for message in ch.history(limit=20):
                    if not _is_from_senz(message):
                        continue
                    content = extract_message_text(message)
                    if not content:
                        raw_data = await fetch_message_raw(message.channel.id, message.id)
                        if raw_data:
                            content = extract_text_from_raw(raw_data)
                    if not content:
                        continue

                    sections = parse_last_seen(content)
                    if any(sections.values()):
                        apply_last_seen(sections)
                        log.info(
                            f"[bootstrap] State bootstrapped from #last-seen-eggs via history: "
                            f"divine={len(sections['divine'])} eternal={len(sections['eternal'])} secret={len(sections['secret'])}"
                        )
                        bootstrapped = True
                        break
            except Exception as hist_err:
                log.warning(f"[bootstrap] discord.py history read failed: {hist_err}")

            # 1b. Fallback: Direct REST API fetch (guarantees reading Discord v10 container components)
            if not bootstrapped:
                log.info("[bootstrap] Attempting direct REST fetch for #last-seen-eggs...")
                raw_msgs = await fetch_channel_messages_raw(LAST_SEEN_CHANNEL_ID, limit=10)
                for raw_msg in raw_msgs:
                    author = raw_msg.get("author", {})
                    if not author.get("bot"):
                        continue
                    if SENZ_BOT_USER_ID and str(author.get("id")) != SENZ_BOT_USER_ID:
                        continue
                    content = extract_text_from_raw(raw_msg)
                    if not content:
                        continue
                    sections = parse_last_seen(content)
                    if any(sections.values()):
                        apply_last_seen(sections)
                        log.info(
                            f"[bootstrap] State bootstrapped from #last-seen-eggs via REST: "
                            f"divine={len(sections['divine'])} eternal={len(sections['eternal'])} secret={len(sections['secret'])}"
                        )
                        bootstrapped = True
                        break

            if not bootstrapped:
                log.warning("[bootstrap] #last-seen-eggs scan found no parseable sections.")
        except Exception as exc:
            log.warning(f"[bootstrap] Could not read from #last-seen-eggs: {exc}")

    # ── 2. Bootstrap from #stock-notify channel history ──
    # Scan recent spawn messages to fill recent_drops and compute real gap history.
    try:
        ch = client.get_channel(STOCK_NOTIFY_CHANNEL_ID) or await client.fetch_channel(STOCK_NOTIFY_CHANNEL_ID)
        history_drops = []
        async for message in ch.history(limit=STOCK_HISTORY_LIMIT):
            if not _is_from_senz(message):
                continue
            parsed = parse_drop_message(message)
            if not parsed:
                raw = await fetch_message_raw(message.channel.id, message.id)
                if raw:
                    parsed = parse_drop_message(message, raw_text=extract_text_from_raw(raw))
            if parsed:
                history_drops.append((message.created_at, parsed))

        # Process oldest-first so gaps are computed in chronological order.
        history_drops.sort(key=lambda x: x[0])
        last_wave_ts = None
        last_wave_by_r = {"secret": None, "eternal": None, "divine": None}

        for created_at, parsed in history_drops:
            now_ts = created_at.timestamp()

            # Record overall wave gap with clustering
            if last_wave_ts is None or (now_ts - last_wave_ts) > WAVE_CLUSTER_WINDOW_SECONDS:
                if last_wave_ts is not None:
                    gap = now_ts - last_wave_ts
                    if gap >= MIN_WAVE_GAP_SECONDS:
                        state["gaps_overall"].append(gap)
                last_wave_ts = now_ts
                state["last_wave_ts_overall"] = now_ts
            state["last_drop_ts_overall"] = now_ts

            rarity = parsed["rarity"]
            if rarity in state["rarity_counts"]:
                last_r = last_wave_by_r.get(rarity)
                if last_r is None or (now_ts - last_r) > WAVE_CLUSTER_WINDOW_SECONDS:
                    if last_r is not None:
                        gap_r = now_ts - last_r
                        if gap_r >= MIN_WAVE_GAP_SECONDS:
                            state["gaps_by_rarity"][rarity].append(gap_r)
                    last_wave_by_r[rarity] = now_ts
                    if "last_wave_ts_by_rarity" not in state:
                        state["last_wave_ts_by_rarity"] = {}
                    state["last_wave_ts_by_rarity"][rarity] = now_ts
                state["last_drop_ts_by_rarity"][rarity] = now_ts

                # Update since_rarity with the most recent timestamp for each rarity
                since_iso = created_at.isoformat()
                existing = state["since_rarity"].get(rarity)
                if not existing or since_iso > existing:
                    state["since_rarity"][rarity] = since_iso
                    state["rarity_counts"][rarity] += 1

            # Add to recent_drops (appendleft = newest first, matching live behavior)
            state["recent_drops"].appendleft({**parsed, "time": created_at.isoformat()})
            if state["last_drop_time"] is None or created_at.isoformat() > state["last_drop_time"]:
                state["last_drop_time"] = created_at.isoformat()
                state["last_drop"] = parsed

        log.info(
            f"[bootstrap] #stock-notify: scanned {len(history_drops)} historical drops. "
            f"gaps_overall={len(state['gaps_overall'])} "
            f"secret_gaps={len(state['gaps_by_rarity']['secret'])} "
            f"eternal_gaps={len(state['gaps_by_rarity']['eternal'])} "
            f"divine_gaps={len(state['gaps_by_rarity']['divine'])}"
        )
    except Exception as exc:
        log.warning(f"[bootstrap] Could not read from #stock-notify history: {exc}")


def _is_from_senz(message: discord.Message) -> bool:
    # Security: discard any messages from non-bot users
    if not getattr(message.author, "bot", False):
        return False
    if SENZ_BOT_USER_ID and str(message.author.id) != SENZ_BOT_USER_ID:
        return False
    return True


async def _handle_last_seen_message(message: discord.Message):
    content = extract_message_text(message)
    if not content:
        raw_data = await fetch_message_raw(message.channel.id, message.id)
        if raw_data:
            content = extract_text_from_raw(raw_data)
    if not content:
        return
    sections = parse_last_seen(content)
    if any(sections.values()):
        apply_last_seen(sections)


@client.event
async def on_message(message: discord.Message):
    # ── User & Admin Commands ──
    if not message.author.bot and message.guild:
        cmd = message.content.strip().lower()

        # Admin: Check auto-role configuration & permissions
        if cmd == "!autorole":
            role = get_auto_role(message.guild)
            bot_member = message.guild.me or message.guild.get_member(client.user.id)
            can_manage = bot_member.guild_permissions.manage_roles if bot_member else False
            hierarchy_ok = (getattr(bot_member.top_role, "position", 0) > getattr(role, "position", 0)) if (bot_member and role and bot_member.top_role) else False

            embed = discord.Embed(
                title="⚙️ EggStock Auto-Role System",
                color=0x00F0FF,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(
                name="Target Role",
                value=f"**@{role.name}** (`ID: {role.id}`)" if role else f"❌ Role `{AUTO_ASSIGN_ROLE_NAME}` not found! Create it in Server Settings.",
                inline=False
            )
            embed.add_field(
                name="Bot 'Manage Roles' Permission",
                value="✅ Granted" if can_manage else "❌ Missing!",
                inline=True
            )
            embed.add_field(
                name="Role Hierarchy",
                value="✅ Bot is higher" if hierarchy_ok else "❌ Bot role must be dragged ABOVE the target role!",
                inline=True
            )
            embed.add_field(
                name="How It Works",
                value="• New members receive this role automatically upon joining so they can view channels.\n• Run **`!syncmembers`** to backfill existing members who joined earlier.",
                inline=False
            )
            embed.set_footer(text="EggStock.xyz Discord System")
            await message.reply(embed=embed)
            return

        # Admin: Check Discord OAuth2 member backup counts (Private / DM / Self-destruct only)
        if cmd in ("!oauthcount", "!oauthstats"):
            is_admin = (
                message.author.id == message.guild.owner_id
                or message.author.guild_permissions.administrator
                or message.author.guild_permissions.manage_guild
            )
            # Instantly delete the triggering message so chat stays clean
            try:
                await message.delete()
            except Exception:
                pass

            if not is_admin:
                return

            stats = oauth_db.get_oauth_stats()
            embed = discord.Embed(
                title="📊 EggStock OAuth2 Member Stats",
                description="🔒 *Confidential • Only you can see this*",
                color=0x00F0FF,
                timestamp=datetime.now(timezone.utc)
            )
            embed.add_field(name="Total Authorized Users", value=f"**{stats['total_authorized']}** members", inline=True)
            embed.add_field(name="Auto-Joined to Server", value=f"**{stats['joined_guild']}** members", inline=True)
            embed.set_footer(text="EggStock 1-Click Discord Connect • eggstock.xyz")

            # Deliver privately via Direct Message (DM)
            dm_sent = False
            try:
                await message.author.send(embed=embed)
                dm_sent = True
            except discord.Forbidden:
                dm_sent = False

            if not dm_sent:
                # Fallback: if user has DMs disabled, send temporary self-destructing message (8 seconds)
                try:
                    await message.channel.send(
                        content=f"🔒 {message.author.mention} *(Sent here because your DMs are closed. Self-destructing in 8s)*",
                        embed=embed,
                        delete_after=8
                    )
                except Exception:
                    pass
            return

        # Admin: Set up the 7 ping & onboarding roles
        if cmd in ("!setuproles", "!createroles", "!pingroles"):
            is_admin = (
                message.author.id == message.guild.owner_id
                or message.author.guild_permissions.administrator
                or message.author.guild_permissions.manage_roles
            )
            try:
                await message.delete()
            except Exception:
                pass
            if not is_admin:
                return

            bot_member = message.guild.me or message.guild.get_member(client.user.id)
            if not bot_member or not bot_member.guild_permissions.manage_roles:
                try:
                    await message.author.send("❌ Bot is missing the **Manage Roles** permission. Please enable it in Server Settings → Roles → EggStock Bot!")
                except Exception:
                    pass
                return

            created, existed, failed = await setup_ping_roles(message.guild)
            embed = discord.Embed(
                title="🎭 Ping & Onboarding Roles Setup",
                description="The 7 official community notification roles have been configured:",
                color=0x4EDEA3,
                timestamp=datetime.now(timezone.utc)
            )
            if created:
                embed.add_field(name="✅ Newly Created Roles", value="\n".join(created), inline=False)
            if existed:
                embed.add_field(name="ℹ️ Already Existed & Verified", value="\n".join(existed), inline=False)
            if failed:
                embed.add_field(name="⚠️ Failed to Create", value="\n".join(failed), inline=False)

            embed.add_field(
                name="📌 Next Step: Discord Onboarding",
                value="Go to **Server Settings → Onboarding → Questions** and add a question like:\n*\"Which notifications do you want?\"*\nAssign these roles as selectable answers!",
                inline=False
            )
            embed.set_footer(text="EggStock Role Manager • eggstock.xyz")

            try:
                await message.author.send(embed=embed)
            except discord.Forbidden:
                await message.channel.send(content=f"🔒 {message.author.mention}", embed=embed, delete_after=15)
            return

        # Admin: Backfill role to all existing members
        if cmd in ("!syncmembers", "!assignroles"):
            is_admin = (
                message.author.id == message.guild.owner_id
                or message.author.guild_permissions.administrator
                or message.author.guild_permissions.manage_roles
            )
            if not is_admin:
                await message.reply("❌ You need the **Manage Roles** or **Administrator** permission to run this command.")
                return

            role = get_auto_role(message.guild)
            if not role:
                await message.reply(
                    f"❌ Could not find a role named `{AUTO_ASSIGN_ROLE_NAME}`.\n"
                    f"Please create a role named **{AUTO_ASSIGN_ROLE_NAME}** in **Server Settings → Roles**, then run `!syncmembers` again!"
                )
                return

            bot_member = message.guild.me or message.guild.get_member(client.user.id)
            can_manage = bot_member.guild_permissions.manage_roles if bot_member else False
            hierarchy_ok = (getattr(bot_member.top_role, "position", 0) > getattr(role, "position", 0)) if (bot_member and role and bot_member.top_role) else False

            if not can_manage:
                await message.reply(
                    "❌ The bot is missing the **Manage Roles** permission!\n"
                    "Go to **Server Settings → Roles → EggStock Bot**, enable **Manage Roles**, and try again."
                )
                return

            if not hierarchy_ok:
                await message.reply(
                    f"❌ **Role Hierarchy Error:** The bot's role is below **@{role.name}**!\n"
                    f"Go to **Server Settings → Roles**, drag the **EggStock Bot** role **ABOVE** **@{role.name}**, and try again."
                )
                return

            status_msg = await message.reply(f"⏳ Checking members in **{message.guild.name}** for **@{role.name}**...")
            assigned_count = 0
            already_had = 0

            try:
                # Fetch members to ensure cache is populated
                members = message.guild.members if message.guild.chunked else [m async for m in message.guild.fetch_members(limit=None)]
            except Exception as exc:
                members = message.guild.members

            for m in members:
                if m.bot:
                    continue
                if role in m.roles:
                    already_had += 1
                    continue
                try:
                    await m.add_roles(role, reason="EggStock admin !syncmembers role backfill")
                    assigned_count += 1
                    await asyncio.sleep(0.15)
                except Exception as exc:
                    log.warning(f"Failed to add role to {m}: {exc}")

            await status_msg.edit(content=(
                f"✅ **Auto-Role Sync Complete!**\n"
                f"• Assigned **@{role.name}** to **{assigned_count}** member(s).\n"
                f"• **{already_had}** member(s) already had the role."
            ))
            return

        # User: Quick !radar status
        if cmd == "!radar":
            last_drop = state.get("last_drop")
            players = state.get("playing_now")
            embed = discord.Embed(
                title="📡 EggStock Live Spawn Radar",
                url="https://eggstock.xyz",
                color=0x00F0FF,
                timestamp=datetime.now(timezone.utc)
            )
            if last_drop:
                embed.add_field(
                    name="Last Observed Drop",
                    value=f"**{last_drop.get('egg', 'Unknown')}** ({last_drop.get('rarity', 'Secret').capitalize()})\n📍 {last_drop.get('location', 'Unknown')}",
                    inline=True
                )
            embed.add_field(
                name="Roblox Players",
                value=f"👥 **{players:,}** online" if players else "Active",
                inline=True
            )
            embed.add_field(
                name="Live Radar Website",
                value="[eggstock.xyz](https://eggstock.xyz)",
                inline=True
            )
            embed.set_footer(text="Steal An Egg 24/7 Radar • eggstock.xyz")
            await message.reply(embed=embed)
            return

    # ── SenZ V2 Channel Parsers ──
    if message.channel.id == LAST_SEEN_CHANNEL_ID and _is_from_senz(message):
        await _handle_last_seen_message(message)
        return

    if message.channel.id != STOCK_NOTIFY_CHANNEL_ID:
        return
    if not _is_from_senz(message):
        return

    parsed = parse_drop_message(message)
    if not parsed:
        raw = await fetch_message_raw(message.channel.id, message.id)
        if raw:
            parsed = parse_drop_message(message, raw_text=extract_text_from_raw(raw))
    if parsed:
        record_drop(parsed)


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if after.channel.id == LAST_SEEN_CHANNEL_ID and _is_from_senz(after):
        await _handle_last_seen_message(after)
        return

    if after.channel.id == STOCK_NOTIFY_CHANNEL_ID and _is_from_senz(after):
        parsed = parse_drop_message(after)
        if not parsed:
            raw = await fetch_message_raw(after.channel.id, after.id)
            if raw:
                parsed = parse_drop_message(after, raw_text=extract_text_from_raw(raw))
        if parsed:
            record_drop(parsed)


# ---------- Security: Rate Limiter ----------
# ---------- Security: IP Guard & Anti-Abuse ----------
import time as _time
from urllib.parse import unquote as _unquote


class IPGuard:
    """
    Production-grade in-memory rate limiter and anti-abuse defense.
    - Sliding-window rate limiter (general + API routes).
    - Security offense tracking (malicious probes, path traversal, exploit attempts).
    - Automated temporary IP Jail / Banning (default 30 minutes) on repeated offenses or severe flood.
    - Self-pruning and bounded capacity to prevent memory exhaustion DoS.
    """

    def __init__(self, ban_duration: int = 1800, max_offenses: int = 3, max_tracked_ips: int = 10000):
        self._hits = {}         # ip -> list of float timestamps
        self._offenses = {}     # ip -> int count of security violations
        self._banned = {}       # ip -> float expiration_timestamp
        self._ban_duration = ban_duration
        self._max_offenses = max_offenses
        self._max_tracked_ips = max_tracked_ips
        self._last_cleanup = _time.monotonic()

    def _cleanup(self, now: float):
        """Purge expired bans, hits outside window, and stale offenses."""
        if now - self._last_cleanup < 120:
            return
        self._last_cleanup = now
        cutoff = now - RATE_LIMIT_WINDOW

        # 1. Purge expired bans
        expired_bans = [ip for ip, exp in self._banned.items() if exp <= now]
        for ip in expired_bans:
            del self._banned[ip]

        # 2. Purge stale rate limit hits
        stale_hits = [ip for ip, hits in self._hits.items() if not hits or hits[-1] < cutoff]
        for ip in stale_hits:
            del self._hits[ip]

        # 3. Purge offenses for inactive IPs
        stale_offenses = [ip for ip in self._offenses if ip not in self._hits and ip not in self._banned]
        for ip in stale_offenses:
            del self._offenses[ip]

        # 4. Hard cap to prevent memory exhaustion attack
        if len(self._hits) > self._max_tracked_ips:
            sorted_ips = sorted(self._hits.items(), key=lambda item: item[1][-1] if item[1] else 0)
            for ip, _ in sorted_ips[:len(sorted_ips) // 3]:
                self._hits.pop(ip, None)

    def is_banned(self, ip: str) -> bool:
        """Check if an IP is actively banned in the jail."""
        now = _time.monotonic()
        ban_exp = self._banned.get(ip)
        if ban_exp:
            if ban_exp > now:
                return True
            del self._banned[ip]
        return False

    def record_offense(self, ip: str, reason: str = "") -> bool:
        """
        Record a security violation (malicious probe, path traversal, exploit attempt).
        Returns True if the IP has now been banned.
        """
        now = _time.monotonic()
        self._cleanup(now)
        count = self._offenses.get(ip, 0) + 1
        self._offenses[ip] = count
        log.warning(f"[SECURITY] Offense {count}/{self._max_offenses} for {ip}: {reason}")
        if count >= self._max_offenses:
            self.ban_ip(ip, reason=f"Accumulated {count} security offenses: {reason}")
            return True
        return False

    def ban_ip(self, ip: str, reason: str = ""):
        """Immediately ban an IP for the configured jail duration."""
        now = _time.monotonic()
        self._banned[ip] = now + self._ban_duration
        log.error(f"[SECURITY BAN] IP {ip} banned for {self._ban_duration}s. Reason: {reason}")

    def is_rate_limited(self, ip: str, is_api: bool = False) -> bool:
        """Check if the IP exceeds the sliding window request limit."""
        now = _time.monotonic()
        self._cleanup(now)

        if self.is_banned(ip):
            return True

        limit = RATE_LIMIT_API_MAX if is_api else RATE_LIMIT_MAX
        hits = self._hits.setdefault(ip, [])
        cutoff = now - RATE_LIMIT_WINDOW

        while hits and hits[0] < cutoff:
            hits.pop(0)

        if len(hits) >= limit:
            if len(hits) >= limit * 2:
                self.record_offense(ip, reason=f"Excessive rate limit flooding ({len(hits)} hits)")
            return True

        hits.append(now)
        return False


_ip_guard = IPGuard()


def _get_client_ip(request) -> str:
    """
    Extract real client IP safely.
    Validates CF-Connecting-IP against presence of CF-Ray to prevent origin spoofing.
    Falls back to X-Forwarded-For or transport peername.
    """
    cf_ray = request.headers.get("CF-Ray")
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ray and cf_ip:
        return cf_ip.strip()
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    peername = request.transport.get_extra_info("peername")
    return peername[0] if peername else "unknown"


def is_overlay_allowed(request) -> bool:
    """
    Overlay is private for OBS streaming and only allowed on the Railway domain
    or local development. Public visitors on eggstock.xyz receive a 404.
    """
    candidates = [
        request.headers.get("X-Forwarded-Host", ""),
        request.headers.get("Host", ""),
        getattr(request, "host", "") or "",
    ]
    # Block immediately if any candidate mentions eggstock.xyz
    for c in candidates:
        h = c.split(":")[0].lower().strip()
        if "eggstock.xyz" in h:
            return False

    # Allow if accessed directly via Railway or localhost
    for c in candidates:
        h = c.split(":")[0].lower().strip()
        if "railway.app" in h or h in ("localhost", "127.0.0.1"):
            return True

    return False


# Enterprise Content-Security-Policy (Allowing ad networks and dynamic ad bid partners)
CSP_POLICY = "; ".join([
    "default-src 'self' https:",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:",
    "style-src 'self' 'unsafe-inline' https:",
    "font-src 'self' https: data:",
    "img-src 'self' data: blob: https:",
    "connect-src 'self' https: wss:",
    "media-src 'self' data: https:",
    "frame-src 'self' https:",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'self'",
    "upgrade-insecure-requests",
])


# ---------- Security: Middleware ----------
@web.middleware
async def security_middleware(request, handler):
    """Adds security headers, IP banning, rate limiting, and request validation."""
    ip = _get_client_ip(request)
    path = request.path

    # 1. Reject banned IPs immediately
    if _ip_guard.is_banned(ip):
        return web.Response(
            status=403,
            text="Forbidden: IP temporarily banned for repeated security violations.\n",
            content_type="text/plain"
        )

    # 2. Block unsupported methods
    if request.method not in ("GET", "HEAD", "OPTIONS", "POST"):
        log.warning(f"BLOCKED {request.method} from {ip}: {path}")
        return web.Response(status=405, text="Method Not Allowed\n", content_type="text/plain")

    # 3. Comprehensive malicious probe detection (URL decoded to catch evasion like %2e%2e)
    try:
        decoded_path = _unquote(_unquote(path)).lower()
    except Exception:
        decoded_path = path.lower()

    blocked_patterns = [
        "..", ".env", ".git", ".sql", ".bak", ".conf", ".ini", ".yml",
        ".php", "wp-admin", "wp-login", "cgi-bin", ".asp", "xmlrpc",
        "eval(", "<script", "passwd", "win.ini", ".aws", ".ds_store",
        "select+", "union+", "exec(", "cmd.exe", "/bin/sh", "/bin/bash"
    ]
    for pattern in blocked_patterns:
        if pattern in decoded_path or pattern in path.lower():
            _ip_guard.record_offense(ip, reason=f"Probe pattern '{pattern}' in '{path}'")
            return web.Response(status=403, text="Forbidden\n", content_type="text/plain")

    # 4. Rate limiting: static files (images, assets) are exempt from rate limit counters
    is_static = path.startswith("/images/") or path.startswith("/website/") or path.startswith("/promo/")
    if not is_static:
        is_api = path.startswith("/api/")
        if _ip_guard.is_rate_limited(ip, is_api):
            log.warning(f"RATE LIMITED {ip}: {path}")
            return web.Response(
                status=429,
                text="Too Many Requests: Rate limit exceeded.\n",
                headers={"Retry-After": str(RATE_LIMIT_WINDOW)},
                content_type="text/plain"
            )

    # 5. Normalize double-slash URLs (e.g. //sitemap.xml from Google Search Console)
    clean_path = re.sub(r"/+", "/", path)
    if clean_path != path:
        if clean_path == "/sitemap.xml":
            return await handle_sitemap(request)
        if clean_path == "/robots.txt":
            return await handle_robots(request)
        if clean_path == "/ads.txt":
            return await handle_ads_txt(request)

    # 6. Restrict overlay: OBS overlay is ONLY available on Railway domain, not on eggstock.xyz
    if path == "/overlay" or path.startswith("/overlay/"):
        if not is_overlay_allowed(request):
            log.info(f"BLOCKED overlay request from {ip} on host {request.headers.get('Host') or request.host}: {path}")
            raise web.HTTPNotFound()

    # 7. Call the actual handler
    try:
        response = await handler(request)
    except web.HTTPRedirection as redir:
        response = redir
    except web.HTTPNotFound:
        response = web.Response(status=404, text="Not Found\n", content_type="text/plain")
    except Exception as exc:
        log.error(f"Unhandled error from {ip} on {path}: {exc}")
        response = web.Response(status=500, text="Internal Server Error\n", content_type="text/plain")

    # 8. Add complete enterprise security headers to every response
    response.headers["Content-Security-Policy"] = CSP_POLICY
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

    # Remove server banner if present
    response.headers.pop("Server", None)

    return response


def compute_prediction_model():
    """
    Computes empirical and Markov-adjusted spawn predictions
    based on 588+ real historical spawn alerts and live session state.
    """
    now = datetime.now(timezone.utc)
    base_rarities = {"Secret": 81.6, "Eternal": 17.5, "Divine": 0.9}

    top_candidates = [
        {"egg": "Pure Jellyfish", "rarity": "Secret", "location": "Angels", "prob_pct": 16.0},
        {"egg": "Gargoyle", "rarity": "Secret", "location": "Demons", "prob_pct": 15.0},
        {"egg": "Tralaledon", "rarity": "Secret", "location": "Prehistoric", "prob_pct": 5.8},
        {"egg": "Cerberus", "rarity": "Secret", "location": "Volcano", "prob_pct": 5.8},
        {"egg": "Kraken", "rarity": "Secret", "location": "Abyss Ocean", "prob_pct": 5.8},
        {"egg": "Mutant Shark", "rarity": "Secret", "location": "Titan Temple", "prob_pct": 5.4},
        {"egg": "T-Rex", "rarity": "Secret", "location": "Prehistoric", "prob_pct": 5.3},
        {"egg": "Cosmic Dragon", "rarity": "Secret", "location": "Cosmic", "prob_pct": 5.3},
        {"egg": "Stag", "rarity": "Secret", "location": "Forest", "prob_pct": 4.9},
        {"egg": "Cosmic Skeleton Boss", "rarity": "Secret", "location": "Cosmic", "prob_pct": 4.4},
    ]

    last_drop = state.get("last_drop") or {}
    last_rarity = (last_drop.get("rarity") or "secret").capitalize()
    last_location = last_drop.get("location") or "Angels"

    def get_elapsed(iso_t):
        if not iso_t:
            return 999999
        try:
            return (now - datetime.fromisoformat(iso_t)).total_seconds()
        except Exception:
            return 999999

    sec_since_eternal = get_elapsed(state["since_rarity"].get("eternal"))
    sec_since_divine = get_elapsed(state["since_rarity"].get("divine"))

    adjusted_rarity = dict(base_rarities)
    if sec_since_eternal > 1800:
        boost = min(15.0, (sec_since_eternal - 1800) / 120.0)
        adjusted_rarity["Eternal"] = round(base_rarities["Eternal"] + boost, 1)
        adjusted_rarity["Secret"] = round(100.0 - adjusted_rarity["Eternal"] - adjusted_rarity["Divine"], 1)

    divine_status = "NORMAL"
    if sec_since_divine > 14400:
        divine_status = "CRITICAL_SURGE"
        adjusted_rarity["Divine"] = 5.2
        adjusted_rarity["Secret"] = round(max(50.0, adjusted_rarity["Secret"] - 4.3), 1)
    elif sec_since_divine > 10800:
        divine_status = "HIGH_SURGE"
        adjusted_rarity["Divine"] = 2.8
        adjusted_rarity["Secret"] = round(max(50.0, adjusted_rarity["Secret"] - 1.9), 1)

    markov_next_biomes = {
        "Angels": [("Demons", 23), ("Angels", 17), ("Prehistoric", 14), ("Cosmic", 12)],
        "Demons": [("Angels", 21), ("Prehistoric", 18), ("Demons", 15), ("Volcano", 13)],
        "Prehistoric": [("Angels", 21), ("Cosmic", 17), ("Demons", 15), ("Volcano", 12)],
        "Cosmic": [("Angels", 27), ("Demons", 21), ("Prehistoric", 12), ("Titan Temple", 10)],
        "Volcano": [("Demons", 19), ("Angels", 17), ("Titan Temple", 16), ("Prehistoric", 13)],
    }

    curr_biome_key = None
    for b in markov_next_biomes:
        if b.lower() in last_location.lower():
            curr_biome_key = b
            break

    next_biome_forecast = markov_next_biomes.get(curr_biome_key, [("Angels", 21), ("Demons", 19), ("Prehistoric", 15)])

    cur_min = now.minute
    peaks = [0, 20, 40, 45, 55]
    next_peak = next((p for p in peaks if p > cur_min), peaks[0])
    mins_to_peak = (next_peak - cur_min) if next_peak > cur_min else (60 - cur_min + next_peak)

    return {
        "calibrated_cadence_seconds": 456,
        "calibrated_cadence_minutes": 7.6,
        "last_drop": {
            "egg": last_drop.get("egg", "Unknown"),
            "rarity": last_rarity,
            "location": last_location,
        },
        "adjusted_rarity_odds": adjusted_rarity,
        "divine_surge_status": divine_status,
        "seconds_since_divine": sec_since_divine if sec_since_divine < 900000 else None,
        "seconds_since_eternal": sec_since_eternal if sec_since_eternal < 900000 else None,
        "top_candidates": top_candidates[:5],
        "markov_next_biomes": [{"biome": b, "prob_pct": p} for b, p in next_biome_forecast],
        "multi_spawn_odds": {"single_egg": 72.9, "double_egg": 20.3, "triple_egg_surge": 6.8},
        "next_hourly_peak": {
            "target_minute": next_peak,
            "minutes_remaining": mins_to_peak
        },
        "total_analyzed_sample": 588,
    }


# ---------- HTTP API for the overlay & public live status ----------
async def handle_cors_preflight(request):
    """Universal CORS preflight handler for API endpoints."""
    return web.Response(
        status=204,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept, Origin, X-Requested-With, X-EggStock-Token",
            "Access-Control-Max-Age": "86400",
        }
    )


async def handle_status(request):
    # Public live drop telemetry and radar status.
    # Protected against abuse via _ip_guard rate limiting middleware.
    now = datetime.now(timezone.utc)

    def seconds_since(iso_ts):
        if not iso_ts:
            return None
        dt = datetime.fromisoformat(iso_ts)
        return int((now - dt).total_seconds())

    def compute_wave_block(rarity=None):
        est = get_wave_estimate(rarity)
        last_wave = (
            state.get("last_wave_ts_by_rarity", {}).get(rarity)
            if rarity
            else state.get("last_wave_ts_overall")
        )
        if last_wave is None:
            last_wave = (
                state["last_drop_ts_by_rarity"][rarity]
                if rarity
                else state["last_drop_ts_overall"]
            )

        if last_wave is None or est["seconds"] is None or est["seconds"] <= 0:
            eta_seconds = None
        else:
            elapsed = now.timestamp() - last_wave
            interval = est["seconds"]
            if elapsed <= interval:
                # Within the current cycle — countdown to wave
                eta_seconds = round(interval - elapsed)
            elif (elapsed - interval) <= 60:
                # Wave is due right now (within 60s window)!
                # Keep at 0 so client shows SPAWNING NOW instead of instantly jumping to 5m
                eta_seconds = 0
            else:
                # Wave window passed without rare drop detected; project next wave
                cycles_missed = int(elapsed // interval)
                next_expected_ts = last_wave + (cycles_missed + 1) * interval
                eta_seconds = max(0, round(next_expected_ts - now.timestamp()))

        return {
            "eta_seconds": eta_seconds,
            "interval_seconds": est["seconds"],
            "sample_size": est["sample_size"],
            "confidence": est["confidence"],
            "basis": est["basis"],
        }


    # Aggregate live drops and last drops by world
    known_worlds = [
        "Forest", "Desert", "Jungle", "Snow", "Volcano",
        "Prehistoric", "Abyss Ocean", "Cherry Blossom", "Titan Temple", "Cosmic",
        "Angels", "Demons", "Angels & Demons", "Enchanted Forest"
    ]
    world_telemetry = {}
    for w in known_worlds:
        world_telemetry[w] = {
            "drops_count": 0,
            "last_egg": None,
            "last_rarity": None,
            "last_time": None,
            "seconds_ago": None,
            "is_recent": False,
        }

    for d in state["recent_drops"]:
        egg_name = d.get("egg") or ""
        loc = d.get("location") or PET_WORLD_MAP.get(egg_name, "")
        matched_world = None
        for w in known_worlds:
            if w.lower() in loc.lower():
                matched_world = w
                break
        if matched_world:
            w_entry = world_telemetry[matched_world]
            w_entry["drops_count"] += 1
            if w_entry["last_egg"] is None:
                w_entry["last_egg"] = egg_name
                w_entry["last_rarity"] = d.get("rarity")
                w_entry["last_time"] = d.get("time")
                sec = seconds_since(d.get("time"))
                w_entry["seconds_ago"] = sec
                w_entry["is_recent"] = (sec is not None and sec < 900)

    # Incorporate last_seen_snapshot if a world has no recent drop recorded
    snap = state.get("last_seen_snapshot")
    if isinstance(snap, dict):
        sections = snap.get("sections", {})
        if isinstance(sections, dict):
            for rarity, items in sections.items():
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            egg_name = item.get("name")
                            world_for_egg = PET_WORLD_MAP.get(egg_name)
                            if world_for_egg and world_for_egg in world_telemetry:
                                w_entry = world_telemetry[world_for_egg]
                                if w_entry["last_egg"] is None:
                                    w_entry["last_egg"] = egg_name
                                    w_entry["last_rarity"] = rarity
                                    ts = item.get("ts")
                                    if ts:
                                        iso_t = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
                                        w_entry["last_time"] = iso_t
                                        w_entry["seconds_ago"] = seconds_since(iso_t)

    payload = {
        "session_drops": state["session_drops"],
        "last_drop": state["last_drop"],
        "last_drop_time": state["last_drop_time"],
        "since_last_drop_seconds": seconds_since(state["last_drop_time"]),
        "rarity_counts": state["rarity_counts"],
        "since_secret_seconds": seconds_since(state["since_rarity"]["secret"]),
        "since_eternal_seconds": seconds_since(state["since_rarity"]["eternal"]),
        "since_divine_seconds": seconds_since(state["since_rarity"]["divine"]),
        "next_wave_estimate": {
            "overall": compute_wave_block(),
            "secret": compute_wave_block("secret"),
            "eternal": compute_wave_block("eternal"),
            "divine": compute_wave_block("divine"),
        },
        "recent_drops": list(state["recent_drops"]),
        "world_telemetry": world_telemetry,
        "last_seen_snapshot": state["last_seen_snapshot"],
        "playing_now": state["playing_now"],
        "discord_members": state.get("discord_members"),
        "discord_online": state.get("discord_online"),
        "prediction_model": compute_prediction_model(),
        "server_time": now.isoformat(),
        "status_heartbeat": "healthy",
    }
    # CORS & Cache-Control: allow direct access from frontend without proxy overhead
    cors_headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Accept, Origin, X-Requested-With, X-EggStock-Token",
    }
    return web.json_response(payload, headers=cors_headers)


async def handle_prediction(request):
    """Direct JSON API endpoint returning empirical spawn predictions."""
    model_data = compute_prediction_model()
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
    }
    return web.json_response(model_data, headers=cors_headers)


async def handle_root(request):
    """Serve index.html with the API token injected at runtime (never stored on disk)."""
    html = (WEBSITE_DIR / "index.html").read_text(encoding="utf-8")
    # Inject the token as a JS variable right after <head> so the polling
    # code can read window.__ES_TOKEN and send it as X-EggStock-Token header.
    token_script = f'<script>window.__ES_TOKEN="{API_TOKEN}";</script>'
    html = html.replace("<head>", f"<head>\n{token_script}", 1)
    return web.Response(
        text=html,
        content_type="text/html",
        charset="utf-8",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    )


async def handle_ads_txt(request):
    ads_file = WEBSITE_DIR / "ads.txt"
    if ads_file.exists():
        content = ads_file.read_text(encoding="utf-8").strip()
    else:
        content = "google.com, pub-3496166469031307, DIRECT, f08c47fec0942fa0"
    return web.Response(
        text=content + "\n",
        content_type="text/plain",
        charset="utf-8",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600",
        }
    )


async def handle_overlay(request):
    if not is_overlay_allowed(request):
        raise web.HTTPNotFound()
    return web.FileResponse(
        OVERLAY_DIR / "index.html",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    )


async def handle_privacy(request):
    return web.FileResponse(WEBSITE_DIR / "privacy.html")


async def handle_terms(request):
    return web.FileResponse(WEBSITE_DIR / "terms.html")


async def handle_about(request):
    about_file = WEBSITE_DIR / "about.html"
    if about_file.exists():
        return web.FileResponse(about_file)
    return web.Response(status=404, text="About page not found\n", content_type="text/plain")


async def handle_contact(request):
    contact_file = WEBSITE_DIR / "contact.html"
    if contact_file.exists():
        return web.FileResponse(contact_file)
    return web.Response(status=404, text="Contact page not found\n", content_type="text/plain")


async def handle_faq(request):
    return web.FileResponse(WEBSITE_DIR / "faq.html")


async def handle_codes(request):
    codes_file = WEBSITE_DIR / "codes.html"
    if codes_file.exists():
        return web.FileResponse(codes_file)
    return web.Response(status=404, text="Codes page not found\n", content_type="text/plain")


async def handle_tier_list(request):
    tier_file = WEBSITE_DIR / "tier_list.html"
    if tier_file.exists():
        return web.FileResponse(tier_file)
    return web.Response(status=404, text="Tier list page not found\n", content_type="text/plain")


async def handle_event(request):
    event_file = WEBSITE_DIR / "event.html"
    if event_file.exists():
        return web.FileResponse(event_file)
    return web.Response(status=404, text="Event page not found\n", content_type="text/plain")


async def handle_script_gateway(request):
    index_file = WEBSITE_DIR / "index.html"
    if index_file.exists():
        return web.FileResponse(index_file)
    return web.Response(status=404, text="Gateway page not found\n", content_type="text/plain")


async def handle_blog_index(request):
    blog_file = WEBSITE_DIR / "blog.html"
    if blog_file.exists():
        return web.FileResponse(blog_file)
    return web.Response(status=404, text="Blog index not found\n", content_type="text/plain")


async def handle_blog_article(request):
    slug = request.match_info.get("slug", "").strip()
    if not slug or not re.match(r'^[a-zA-Z0-9_\-]+$', slug):
        return web.Response(status=400, text="Invalid article slug\n", content_type="text/plain")
    article_file = WEBSITE_DIR / "blog" / f"{slug}.html"
    if article_file.exists():
        return web.FileResponse(article_file)
    return web.Response(status=404, text="Article not found\n", content_type="text/plain")


async def handle_robots(request):
    return web.FileResponse(WEBSITE_DIR / "robots.txt")


async def handle_sitemap(request):
    sitemap_file = WEBSITE_DIR / "sitemap.xml"
    if sitemap_file.exists():
        return web.FileResponse(sitemap_file, headers={"Content-Type": "application/xml; charset=utf-8"})
    return web.Response(status=404, text="Sitemap not found")


async def handle_logo(request):
    f = WEBSITE_DIR / "logo.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Logo not found")


async def handle_favicon(request):
    f = WEBSITE_DIR / "favicon.ico"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/x-icon", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_favicon_48(request):
    f = WEBSITE_DIR / "favicon-48x48.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_favicon_96(request):
    f = WEBSITE_DIR / "favicon-96x96.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_favicon_144(request):
    f = WEBSITE_DIR / "favicon-144x144.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_favicon_192(request):
    f = WEBSITE_DIR / "favicon-192x192.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_favicon_512(request):
    f = WEBSITE_DIR / "favicon-512x512.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Favicon not found")


async def handle_apple_touch_icon(request):
    f = WEBSITE_DIR / "apple-touch-icon.png"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "image/png", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Icon not found")


async def handle_manifest(request):
    f = WEBSITE_DIR / "site.webmanifest"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "application/manifest+json; charset=utf-8", "Cache-Control": "public, max-age=86400"})
    return web.Response(status=404, text="Manifest not found")


async def handle_google_verify(request):
    return web.Response(text="google-site-verification: google2dcf6b5ce2c3be8e.html\n", content_type="text/html")


async def handle_discord_modal_js(request):
    f = WEBSITE_DIR / "discord_modal.js"
    if f.exists():
        return web.FileResponse(f, headers={"Content-Type": "application/javascript; charset=utf-8", "Cache-Control": "public, max-age=60, stale-while-revalidate=300"})
    return web.Response(status=404, text="Script not found")


# ---------- Discord OAuth2 & Account Linking Handlers ----------
from urllib.parse import quote as _urlquote
import hashlib as _hashlib

async def handle_discord_login(request):
    """Initiates Discord OAuth2 flow with identify and guilds.join scopes."""
    state = _secrets.token_urlsafe(16)
    now = _time.time()
    _oauth_states[state] = now
    
    # Prune states older than 15 minutes
    stale = [s for s, ts in _oauth_states.items() if now - ts > 900]
    for s in stale:
        _oauth_states.pop(s, None)
        
    auth_url = (
        f"https://discord.com/oauth2/authorize?"
        f"client_id={DISCORD_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={_urlquote(DISCORD_REDIRECT_URI)}&"
        f"scope={_urlquote(OAUTH_SCOPES)}&"
        f"state={state}&"
        f"prompt=consent"
    )
    return web.HTTPFound(auth_url)


async def handle_discord_callback(request):
    """Exchanges code for tokens, fetches profile, executes guilds.join, and sets session."""
    code = request.query.get("code")
    state = request.query.get("state")
    error = request.query.get("error")

    if error or not code:
        log.warning(f"[oauth] Auth cancelled or failed: error={error}")
        return web.HTTPFound("/?auth=error&reason=cancelled")

    # Anti-CSRF state check (lenient fallback)
    _oauth_states.pop(state, None)

    # 1. Exchange authorization code for access token
    token_url = "https://discord.com/api/v10/oauth2/token"
    token_payload = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        async with _aiohttp_client.ClientSession() as session:
            async with session.post(token_url, data=token_payload, headers=headers, timeout=_aiohttp_client.ClientTimeout(total=12)) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    log.error(f"[oauth] Token exchange failed HTTP {resp.status}: {body}")
                    return web.HTTPFound("/?auth=error&reason=token_failed")
                token_data = await resp.json()
    except Exception as exc:
        log.error(f"[oauth] Token exchange error: {exc}")
        return web.HTTPFound("/?auth=error&reason=exchange_error")

    access_token = token_data.get("access_token")
    if not access_token:
        return web.HTTPFound("/?auth=error&reason=no_access_token")

    # 2. Fetch authenticated user profile
    user_url = "https://discord.com/api/v10/users/@me"
    try:
        async with _aiohttp_client.ClientSession() as session:
            async with session.get(user_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=_aiohttp_client.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    log.error(f"[oauth] User fetch failed HTTP {resp.status}")
                    return web.HTTPFound("/?auth=error&reason=user_failed")
                user_data = await resp.json()
    except Exception as exc:
        log.error(f"[oauth] User fetch error: {exc}")
        return web.HTTPFound("/?auth=error&reason=user_error")

    user_id = str(user_data["id"])

    # 3. Automatic guilds.join (Add user directly to server)
    target_guild_id = None
    if DISCORD_GUILD_ID:
        try:
            target_guild_id = int(DISCORD_GUILD_ID)
        except Exception:
            pass
    if not target_guild_id and client.guilds:
        target_guild_id = client.guilds[0].id
    if not target_guild_id and STOCK_NOTIFY_CHANNEL_ID:
        ch = client.get_channel(STOCK_NOTIFY_CHANNEL_ID)
        if ch and ch.guild:
            target_guild_id = ch.guild.id

    joined_guild = False
    if target_guild_id:
        join_url = f"https://discord.com/api/v10/guilds/{target_guild_id}/members/{user_id}"
        join_payload = {
            "access_token": access_token,
            "roles": [str(AUTO_ASSIGN_ROLE_ID)] if AUTO_ASSIGN_ROLE_ID else []
        }
        join_headers = {
            "Authorization": f"Bot {DISCORD_TOKEN}",
            "Content-Type": "application/json"
        }
        try:
            async with _aiohttp_client.ClientSession() as session:
                async with session.put(join_url, json=join_payload, headers=join_headers, timeout=_aiohttp_client.ClientTimeout(total=10)) as resp:
                    if resp.status in (201, 204):
                        joined_guild = True
                        log.info(f"[oauth] guilds.join success for {user_data.get('username')} ({user_id}) in guild {target_guild_id} (HTTP {resp.status})")
                    else:
                        resp_txt = await resp.text()
                        log.warning(f"[oauth] guilds.join returned HTTP {resp.status} for {user_id}: {resp_txt}")
        except Exception as exc:
            log.error(f"[oauth] guilds.join error for {user_id}: {exc}")

    # 4. Save to persistent SQLite backup database
    ip = _get_client_ip(request)
    ip_hash = _hashlib.sha256(ip.encode()).hexdigest()[:16]
    oauth_db.save_oauth_user(user_data, token_data, joined_guild=joined_guild, ip_hash=ip_hash)

    # 5. Create active session
    session_token = _secrets.token_hex(32)
    avatar_hash = user_data.get("avatar")
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else "https://cdn.discordapp.com/embed/avatars/0.png"
    user_session_info = {
        "user_id": user_id,
        "username": user_data.get("global_name") or user_data.get("username", "Member"),
        "raw_username": user_data.get("username", ""),
        "avatar_url": avatar_url,
        "joined_guild": joined_guild,
        "created_at": _time.time(),
    }
    _active_user_sessions[session_token] = user_session_info
    oauth_db.save_session(session_token, user_session_info)

    # 6. Redirect back with session cookie
    response = web.HTTPFound("/?auth=success")
    response.set_cookie(
        "es_session",
        session_token,
        max_age=30 * 86400,
        httponly=True,
        samesite="Lax",
        secure=True,
        path="/"
    )
    return response


async def handle_auth_me(request):
    """Returns the current logged-in user profile or authenticated: false."""
    cookie = request.cookies.get("es_session")
    if not cookie:
        return web.json_response({"authenticated": False})
    user_info = _active_user_sessions.get(cookie)
    if not user_info:
        user_info = oauth_db.get_session(cookie)
        if user_info:
            _active_user_sessions[cookie] = user_info
    if user_info:
        return web.json_response({
            "authenticated": True,
            "user": user_info
        })
    return web.json_response({"authenticated": False})


async def handle_auth_logout(request):
    """Logs out the user and clears the session cookie."""
    cookie = request.cookies.get("es_session")
    if cookie:
        _active_user_sessions.pop(cookie, None)
        oauth_db.delete_session(cookie)
    response = web.HTTPFound("/")
    response.del_cookie("es_session", path="/")
    return response


async def handle_auth_stats(request):
    """Returns aggregate OAuth counts."""
    stats = oauth_db.get_oauth_stats()
    return web.json_response(stats)


async def start_web_app():
    app = web.Application(
        middlewares=[security_middleware],
        client_max_size=MAX_REQUEST_SIZE,
    )
    routes = [
        web.get("/", handle_root),
        web.get("/api/auth/discord/login", handle_discord_login),
        web.get("/api/auth/discord/callback", handle_discord_callback),
        web.get("/api/auth/me", handle_auth_me),
        web.get("/api/auth/logout", handle_auth_logout),
        web.post("/api/auth/logout", handle_auth_logout),
        web.get("/api/auth/stats", handle_auth_stats),
        web.get("/discord_modal.js", handle_discord_modal_js),
        web.get("/logo.png", handle_logo),
        web.get("/favicon.ico", handle_favicon),
        web.get("/favicon-48x48.png", handle_favicon_48),
        web.get("/favicon-96x96.png", handle_favicon_96),
        web.get("/favicon-144x144.png", handle_favicon_144),
        web.get("/favicon-192x192.png", handle_favicon_192),
        web.get("/favicon-512x512.png", handle_favicon_512),
        web.get("/apple-touch-icon.png", handle_apple_touch_icon),
        web.get("/apple-touch-icon-precomposed.png", handle_apple_touch_icon),
        web.get("/site.webmanifest", handle_manifest),
        web.get("/google2dcf6b5ce2c3be8e.html", handle_google_verify),
        web.get("/ads.txt", handle_ads_txt),
        web.get("/robots.txt", handle_robots),
        web.get("/sitemap.xml", handle_sitemap),
        web.get("/privacy", handle_privacy),
        web.get("/privacy/", handle_privacy),
        web.get("/terms", handle_terms),
        web.get("/terms/", handle_terms),
        web.get("/about", handle_about),
        web.get("/about/", handle_about),
        web.get("/contact", handle_contact),
        web.get("/contact/", handle_contact),
        web.get("/faq", handle_faq),
        web.get("/faq/", handle_faq),
        web.get("/codes", handle_codes),
        web.get("/codes/", handle_codes),
        web.get("/tier-list", handle_tier_list),
        web.get("/tier-list/", handle_tier_list),
        # High-Intent SEO Landing Routes (Google Search optimization)
        web.get("/stock", handle_root),
        web.get("/stock/", handle_root),
        web.get("/prediction", handle_root),
        web.get("/prediction/", handle_root),
        web.get("/predictions", handle_root),
        web.get("/predictions/", handle_root),
        web.get("/notifier", handle_root),
        web.get("/notifier/", handle_root),
        web.get("/values", handle_tier_list),
        web.get("/values/", handle_tier_list),
        web.get("/trading", handle_tier_list),
        web.get("/trading/", handle_tier_list),
        web.get("/event", handle_event),
        web.get("/event/", handle_event),
        web.get("/script", handle_script_gateway),
        web.get("/script/", handle_script_gateway),
        web.get("/scripts", handle_script_gateway),
        web.get("/scripts/", handle_script_gateway),
        web.get("/blog", handle_blog_index),
        web.get("/blog/", handle_blog_index),
        web.get("/guides", handle_blog_index),
        web.get("/guides/", handle_blog_index),
        web.get("/blog/{slug}", handle_blog_article),
        web.get("/blog/{slug}/", handle_blog_article),
        web.get("/guides/{slug}", handle_blog_article),
        web.get("/guides/{slug}/", handle_blog_article),
        web.route("OPTIONS", "/api/status", handle_cors_preflight),
        web.route("OPTIONS", "/api/prediction", handle_cors_preflight),
        web.route("OPTIONS", "/api/predictions", handle_cors_preflight),
        web.get("/api/status", handle_status),
        web.get("/api/prediction", handle_prediction),
        web.get("/api/predictions", handle_prediction),
        web.get("/overlay", handle_overlay),
        web.get("/overlay/", handle_overlay),
        web.get("/overlay/overlay.css", lambda req: web.FileResponse(OVERLAY_DIR / "overlay.css")),
        web.get("/overlay/overlay.js", lambda req: web.FileResponse(OVERLAY_DIR / "overlay.js")),
        web.get("/overlay.css", lambda req: web.FileResponse(OVERLAY_DIR / "overlay.css")),
        web.get("/overlay.js", lambda req: web.FileResponse(OVERLAY_DIR / "overlay.js")),
        web.static("/overlay/assets", OVERLAY_DIR),
        web.static("/website/assets", WEBSITE_DIR),
        web.static("/images", WEBSITE_DIR / "images"),
    ]
    promo_dir = WEBSITE_DIR / "promo"
    if promo_dir.exists():
        routes.append(web.static("/promo", promo_dir))
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()
    log.info(f"HTTP API listening on port {PORT}")


async def run_discord_bot():
    backoff = 10
    while True:
        try:
            log.info("Connecting Discord client...")
            await client.start(DISCORD_TOKEN)
        except discord.errors.PrivilegedIntentsRequired:
            log.critical(
                "\n" + "=" * 65 +
                "\n[PRIVILEGED INTENTS REQUIRED]\n"
                "To auto-assign roles when members join:\n"
                "1. Open https://discord.com/developers/applications\n"
                "2. Select your Bot -> Click 'Bot' tab on the left\n"
                "3. Scroll to 'Privileged Gateway Intents'\n"
                "4. Enable 'SERVER MEMBERS INTENT' and click 'Save Changes'!\n" +
                "=" * 65 + "\n"
            )
            log.warning("[fallback] Restarting bot without Server Members intent so radar & web app stay online...")
            intents.members = False
            try:
                await client.start(DISCORD_TOKEN)
            except Exception as e:
                log.error(f"Fallback Discord start error: {e}")
                await asyncio.sleep(15)
        except discord.errors.HTTPException as exc:
            log.warning(f"Discord API HTTP/Cloudflare rate limit: {exc}. Web server remains 100% online! Retrying in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 120)
        except Exception as exc:
            log.error(f"Discord client error: {exc}. Web server remains 100% online. Retrying in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 120)


async def main():
    # 1. Start Web Server FIRST so website is immediately available
    await start_web_app()
    # 2. Launch background pollers
    asyncio.create_task(_poll_roblox_players())
    asyncio.create_task(_poll_discord_stats())
    # 3. Launch Discord client in background task so errors NEVER crash the web server
    asyncio.create_task(run_discord_bot())

    # 4. Keep main event loop alive forever
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

