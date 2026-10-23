# Project: Steal An Egg — Live Stock Radar Overlay

## Goal
Build our own version of a "stock radar" style stream overlay (like the
"N2F" one seen on a competitor's YouTube live stream) for the Roblox game
**Steal An Egg**. The overlay shows live stats: session drops, last drop
time, rarity counts (Secret/Eternal/Divine), estimated next spawn timing,
etc. — meant to run as an OBS browser-source overlay during a 24/7 live
stream.

**Important constraint (copyright):** we are NOT copying N2F's exact
visual design/graphics. We're building our own overlay with our own
layout/branding that shows the *same category* of information (facts
about game stock aren't copyrightable; a cloned visual design would be).

## Why we're doing it this way
There is no official public API for Steal An Egg stock/spawn data. A
third-party Discord bot called **SenZ V2** already tracks spawns for this
game (and Blox Fruits, Grow a Garden 2) and posts alerts into Discord
channels. Since SenZ V2 doesn't expose a public API/key, our plan is:

1. Add SenZ V2 to our own Discord server.
2. Build our OWN separate Discord bot that sits in the same server and
   reads the messages SenZ V2 posts (this is our own data now, since it's
   posted in our own server — not scraping someone else's private data).
3. Parse those messages into structured data (egg name, rarity, location,
   timestamps).
4. Serve that data as JSON via a small HTTP API.
5. (Not built yet) Build an HTML/OBS overlay that polls that API and
   displays it live, styled in our own design.
6. Host the whole thing on **Railway**.

## Data sources identified
- **`#stock-notify` channel**: SenZ V2 posts a NEW message per spawn event,
  as an embed. Title format like `"Secret Egg Spawned!! - 8:39 AM"`, with
  fields/description containing `Egg:`, `Location:`, `Spawned:`, `Money:`,
  `Recommended Speed:`.
- **`#last-stock-notify` channel**: SenZ V2 posts ONE message and EDITS it
  in place. Contains three sections (Divine / Eternal / Secret), each
  listing recent items with real Discord timestamp tags, e.g.:
  ```
  ### <:Secret:123>  Secret — Last Seen
  <:Tralaledon:123> Tralaledon — <t:1788579339:R>
  ```
  This gives us exact Unix timestamps (`<t:UNIXTIME:R>`), which is more
  reliable than parsing "X minutes ago" text.

## Key design decision: "Next Egg Wave" timer
Initially considered a fixed 5-minute countdown (based on an old official
Roblox game description that mentioned "rare eggs every 5 minutes" — since
removed from the listing, and explicitly called "unverified" by a fan wiki
at steal-an-egg.github.io). We rejected the fixed-5-min approach because
real observed data showed gaps ranging from ~5 minutes to 36+ hours between
drops — a fixed countdown would desync badly from reality on stream.

**Decision: reverse-engineer the real interval from data.**
The bot now:
- Tracks a rolling window (last 20) of REAL gaps between observed drops,
  both overall and separately per rarity (secret/eternal/divine).
- Uses the **median** gap (not average) as the estimate, since median
  resists being skewed by rare huge outliers (e.g. one 36-hour gap).
- Bootstraps this gap history immediately from the `#last-stock-notify`
  snapshot's real timestamps (so we're not starting from zero data).


## What N2F's panel shows (the reference / target feature list)
| Element | Status for our version |
|---|---|
| Next Egg Wave countdown | ✅ solved via reverse-engineered median gap estimator |
| Session Drops (counter) | ✅ our bot increments this on every parsed drop |
| Last Egg Time / Since Last Drop | ✅ tracked from parsed drop timestamps |
| Secret / Eternal / Divine counts | ✅ tracked per rarity |
| Since Eternal / Since Divine | ✅ tracked per rarity |
| Playing Now (live player count) | ✅ built — polls Roblox universe games API every 60s |
| Next Admin Abuse countdown | ✅ solved — Admin Abuse has run every Saturday 15:00 UTC so far |
| Scrolling drop feed (name/rarity/time/biome) | ✅ our bot stores last 15 drops for this |
| The actual visual overlay/panel design | ✅ updated — redesigned to match the arcade game HUD reference design at `/overlay` |

## What's built so far
A Python bot (`bot.py`, using `discord.py` + `aiohttp`) that:
- Connects to Discord with our own bot token
- Listens to `#stock-notify` for new spawn messages (embeds)
- Listens to `#last-stock-notify` for edits to the aggregated last-seen
  message (via `on_message` + `on_message_edit`)
- Parses both formats into structured data
- Tracks session stats, per-rarity counts, and gap-based wave estimates
- Serves everything as JSON at `GET /api/status`
- Serves the redesigned OBS stream overlay at `GET /overlay`

Supporting files:
- `requirements.txt` — `discord.py`, `aiohttp`, `audioop-lts`
- `Procfile` — `web: python bot.py` (for Railway; exposes the API and overlay)

## Environment variables needed (set in Railway, not committed to git)
- `DISCORD_TOKEN` — token for OUR bot (created at discord.com/developers/applications, NOT SenZ V2's token)
- `STOCK_NOTIFY_CHANNEL_ID` — real value: `1545634273367695390`
- `LAST_SEEN_CHANNEL_ID` — real value: `1545635171296870531`
- `SENZ_BOT_USER_ID` — optional, tightens matching to only SenZ V2's messages
- `GAP_WINDOW_SIZE` — optional, default 20 (how many recent gaps to average over)
- `FALLBACK_INTERVAL_SECONDS` — optional, default 300 (only used before any real data exists)
- `PORT` — Railway sets this automatically

## Deployment status (as of last update)
- Local project folder: `C:\Users\jyoti\OneDrive\Discord Bots\steal_an_egg`
- Using Railway CLI (not GitHub-connected deploy)
- Railway project name: `alluring-solace`, service name: `ideal-trust`
- Had to troubleshoot: wrong Railway account logged into CLI (fixed via
  `railway logout` / `railway login`), then an empty/unlinked service
  causing `railway up` to fail with 404 (fixed via `railway add` to
  create a service, then linking it)
- Own Discord bot has been created and added to the server
- Real channel IDs have been obtained and set as Railway variables
- **Bug found and fixed:** first real deploy crashed with
  `ModuleNotFoundError: No module named 'audioop'` — Python 3.13 removed
  the built-in `audioop` module, and `discord.py`'s voice-support code
  still imports it even though this bot never uses voice. Fixed by adding
  `audioop-lts==0.2.1` to `requirements.txt`. Not yet re-deployed/confirmed
  after this fix.
- **Security note:** the real bot token was accidentally pasted into chat
  during a terminal log dump. It should be regenerated in the Discord
  Developer Portal (Bot tab -> Reset Token) and re-set in Railway before
  going further, since it was exposed.
- **Not yet confirmed:** a successful `railway up` deploy (post-audioop-fix)
  with logs showing the bot connected and successfully parsing a real
  live spawn message — this is the next thing to verify

## API response shape (for building the UI against)
`GET /api/status` currently returns (see `bot.py` `handle_status()`):
```json
{
  "session_drops": 0,
  "last_drop": null,
  "since_last_drop_seconds": null,
  "rarity_counts": {"secret": 0, "eternal": 0, "divine": 0},
  "since_secret_seconds": null,
  "since_eternal_seconds": null,
  "since_divine_seconds": null,
  "next_wave_estimate": {
    "overall": {"eta_seconds": null, "interval_seconds": 300, "sample_size": 0, "confidence": "none", "basis": "fallback"},
    "secret": {...}, "eternal": {...}, "divine": {...}
  },
  "recent_drops": [],
  "last_seen_snapshot": null
}
```
Once real data flows in, `last_drop` becomes e.g.
`{"rarity": "secret", "egg": "Kraken", "location": "Abyss Ocean"}`,
`recent_drops` becomes a list of those plus a `time` ISO timestamp (newest
first, max 15 kept), and `next_wave_estimate.*` fields fill in with real
numbers as gaps are observed (see "Key design decision" section above for
why this is a live-computed estimate, not a fixed constant).

## UI/overlay
The original HTML/CSS/JS OBS overlay is now built in `overlay/` and served
by the bot at `GET /overlay`. It polls the same-origin `/api/status` endpoint
every two seconds and shows wave confidence, session and rarity data, elapsed
timers, an expected Saturday 15:00 UTC admin-event countdown, and the recent
drop feed. Its midnight-glass/radar design is original and does not reuse the
reference stream's graphics, colours, branding, or layout.

Use the Railway URL plus `/overlay` as the OBS Browser Source URL. Start at a
width of 540 px; it remains responsive at narrower widths. The panel visibly
marks live player count as pending until the independent Roblox API integration
adds that field to `/api/status`.

## Immediate next steps (pick up here)
1. Regenerate the Discord bot token (it was exposed in a terminal log
   pasted into chat) and update it in Railway
2. Confirm `railway variables` shows correct real values (not placeholders)
   for `DISCORD_TOKEN`, `STOCK_NOTIFY_CHANNEL_ID`, `LAST_SEEN_CHANNEL_ID`
3. Run `railway up` from the project folder (now includes the audioop fix)
4. Run `railway logs` and confirm:
   - `Logged in as <BotName> (id=...)`
   - `Watching channel id ...`
   - Eventually: `Applied last-seen snapshot: ...` or `Recorded drop: ...`
     once real Discord messages come through
5. If the regex parser in `parse_embed()` doesn't match real `#stock-notify`
   messages correctly (we've only inferred this format from a screenshot,
   not confirmed against raw message content like we did for last-seen),
   capture a real raw message and adjust the regex — same process we used
   to fix the last-seen parser earlier.
6. Once confirmed working end-to-end: build the Roblox "Playing Now" API
   integration (simple, independent, no dependency on SenZ V2).
7. Add the Roblox "Playing Now" API integration so the existing overlay's
   player card can switch from its pending state to live data.

## Files (all in the project folder, and also produced in this chat)
- `bot.py` — main bot (latest version has the reverse-engineered
  median-based wave estimator, NOT the old fixed-5-minute version)
- `requirements.txt` — now includes `audioop-lts` fix
- `Procfile`
- `.env.example`
- `README.md`
- `overlay/index.html`, `overlay/overlay.css`, `overlay/overlay.js` — the
  OBS overlay, served as `/overlay` and `/overlay/assets/*`

---
*Update this file after each meaningful step (new feature built, bug
fixed, deployment milestone reached) so the project can be picked up by
any AI assistant or by a human without losing context.*
