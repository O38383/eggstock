(() => {
  // Query params for customization (?preview=true to test OBS cutout alignment)
  const params = new URLSearchParams(window.location.search);
  const showPreview = params.get("preview") === "true";
  const token = params.get("token") || window.__ES_TOKEN || "";
  const apiUrl = params.get("api") || (window.location.origin.includes("railway") ? "/api/status" : "https://eggstock-web-production.up.railway.app/api/status");

  // Pre-mapped pet images (serves from /images/pets/ everywhere on Railway and Cloudflare)
  const PET_IMG_MAP = {
    "winged lamb": "/images/pets/winged_lamb.png",
    "toro": "/images/pets/toro.png",
    "archangel": "/images/pets/archangel.png",
    "kitsune": "/images/pets/kitsune.png",
    "nightflame": "/images/pets/nightflame.png",
    "unicorn": "/images/pets/unicorn.png",
    "kraken": "/images/pets/kraken.png",
    "gorilla king": "/images/pets/gorilla_king.png",
    "mosasaurus": "/images/pets/mosasaurus.png",
    "ice dragon": "/images/pets/ice_dragon.png",
    "lava dragon": "/images/pets/lava_dragon.png",
    "el maja": "/images/pets/el_maja.png",
    "cerberus": "/images/pets/cerberus.png",
    "pure jellyfish": "/images/pets/pure_jellyfish.png",
    "gargoyle": "/images/pets/gargoyle.png",
    "yeti": "/images/pets/yeti.png",
    "trex": "/images/pets/trex.png",
    "tralaledon": "/images/pets/tralaledon.png",
    "oni tiger": "/images/pets/oni_tiger.png",
    "phoenix": "/images/pets/phoenix.png",
    "pegasus": "/images/pets/pegasus.png",
    "centaur": "/images/pets/centaur.png",
    "holy peacock": "/images/pets/holy_peacock.png",
    "light dove": "/images/pets/light_dove.png",
    "sacred moth": "/images/pets/sacred_moth.png",
    "demon hound": "/images/pets/demon_hound.png",
    "imp": "/images/pets/imp.png",
    "flame sprite": "/images/pets/flame_sprite.png",
    "razorfang": "/images/pets/razorfang.png",
    "skeleton horse": "/images/pets/skeleton_horse.png",
    "world burner": "/images/pets/world_burner.png",
    "eternal lunar": "/images/pets/eternal_lunar_dragon.png",
    "cosmic dragon": "/images/pets/cosmic_dragon.png",
    "cosmic skeleton": "/images/pets/cosmic_skeleton_boss.png",
    "stag": "/images/pets/stag.png",
    "mutant shark": "/images/pets/mutant_shark.png",
    "king snake": "/images/pets/snake_king.png"
  };

  // Default emojis for standard animals without local PNGs
  const EMOJI_MAP = {
    chicken: "🐔", dog: "🐶", bird: "🐦", owl: "🦉", raccoon: "🦝", fox: "🦊", bear: "🐻",
    frog: "🐸", duck: "🦆", fish: "🐟", turtle: "🐢", swan: "🦢", axolotl: "🦎", leviathan: "🐉",
    jerboa: "🐭", fennec: "🦊", camel: "🐫", snake: "🐍", spider: "🕷️", scorpion: "🦂", sphinx: "🦁",
    chimp: "🐵", toucan: "🦜", croc: "🐊", gorilla: "🦍", tiger: "🐯",
    penguin: "🐧", walrus: "🦭", polar: "🐻‍❄️", mammoth: "🦣",
    gecko: "🦎", bull: "🐂", chili: "🌶️", iguana: "🦎",
    shark: "🦈", orca: "🐋", whale: "🐳",
    dodo: "🦤", pterodactyl: "🦕", ankylosaurus: "🦖", bronto: "🦕", triceratops: "🦏",
    centapede: "🐛", crane: "🦩", salamander: "🦎", panda: "🐼", koi: "🐟",
    crustacia: "🦀", beetle: "🪲", jackalope: "🐇", sunbird: "🦅",
    moon: "🌕", pumpkin: "🎃", butterfly: "🦋", cat: "🐱", clown: "🤡", candle: "🕯️", ghost: "👻",
    gerbil: "🐹", toadstool: "🍄", chest: "📦", crow: "🦅", wolf: "🐺"
  };

  function getPetIconHtml(name) {
    const lower = name.toLowerCase();
    for (const [key, path] of Object.entries(PET_IMG_MAP)) {
      if (lower.includes(key)) {
        return `<img class="item-icon" src="${path}" alt="${name}" onerror="this.outerHTML='<span class=\\'item-emoji\\'>🥚</span>'">`;
      }
    }
    for (const [key, em] of Object.entries(EMOJI_MAP)) {
      if (lower.includes(key)) {
        return `<span class="item-emoji">${em}</span>`;
      }
    }
    return `<span class="item-emoji">🥚</span>`;
  }

  // Initial Full Roster (Exact match to YouTuber's footage)
  const ROSTER_DATA = {
    forest: [
      { name: "Chicken", status: "x3", inStock: true },
      { name: "Dog", status: "5m ago", inStock: false },
      { name: "Bird", status: "x1", inStock: true },
      { name: "Burrowing Owl", status: "5m ago", inStock: false },
      { name: "Raccoon", status: "10m ago", inStock: false },
      { name: "Fox", status: "1h ago", inStock: false },
      { name: "Bear", status: "15m ago", inStock: false },
      { name: "Brr Brr Patapim", status: "x1", inStock: true }
    ],
    snow: [
      { name: "Penguin", status: "x1", inStock: true },
      { name: "Walrus", status: "x2", inStock: true },
      { name: "Polar Bear", status: "x2", inStock: true },
      { name: "Sabertooth Tiger", status: "5m ago", inStock: false },
      { name: "Mammoth", status: "10m ago", inStock: false },
      { name: "King Mammoth", status: "25m ago", inStock: false },
      { name: "Yeti", status: "1h ago", inStock: false },
      { name: "Ice Dragon", status: "30m ago", inStock: false }
    ],
    cosmic: [
      { name: "Centapede", status: "x3", inStock: true },
      { name: "Cosmic Gecko", status: "5m ago", inStock: false },
      { name: "Cosmic Gorilla", status: "x1", inStock: true },
      { name: "La Vacca Saturno", status: "Saturn", inStock: true, color: "blue" },
      { name: "Cosmic Dragon", status: "1h ago", inStock: false },
      { name: "Cosmic Skeleton", status: "2h ago", inStock: false },
      { name: "Eternal Lunar", status: "40m ago", inStock: false },
      { name: "Unicorn", status: "5d ago", inStock: false }
    ],
    lake: [
      { name: "Frog", status: "x4", inStock: true },
      { name: "Duckling", status: "5m ago", inStock: false },
      { name: "Catfish", status: "x1", inStock: true, color: "yellow" },
      { name: "Turtle", status: "5m ago", inStock: false },
      { name: "Trulimero Trulicina", status: "15m ago", inStock: false },
      { name: "Swan", status: "10m ago", inStock: false },
      { name: "Axolotl", status: "1h ago", inStock: false },
      { name: "Leviathan", status: "1h ago", inStock: false }
    ],
    volcano: [
      { name: "Lava Gecko", status: "x3", inStock: true },
      { name: "Lava Frog", status: "5m ago", inStock: false },
      { name: "Flaming Bull", status: "x1", inStock: true },
      { name: "Chillin Chilli", status: "10m ago", inStock: false },
      { name: "Lava Iguana", status: "x1", inStock: true },
      { name: "Cerberus", status: "1h ago", inStock: false },
      { name: "Phoenix", status: "10h ago", inStock: false },
      { name: "Lava Dragon", status: "5h ago", inStock: false }
    ],
    cherry_blossom: [
      { name: "Crane", status: "x2", inStock: true },
      { name: "Salamander", status: "x1", inStock: true },
      { name: "Red Panda", status: "x1", inStock: true },
      { name: "Snowy Owl", status: "x1", inStock: true },
      { name: "Koi", status: "5m ago", inStock: false },
      { name: "Stag", status: "3h ago", inStock: false },
      { name: "Oni Tiger", status: "1h ago", inStock: false },
      { name: "Kitsune", status: "13h ago", inStock: false }
    ],
    desert: [
      { name: "Jerboa", status: "x3", inStock: true },
      { name: "Fennec", status: "5m ago", inStock: false },
      { name: "Camel", status: "x1", inStock: true },
      { name: "Tob Tobi Tob Tob", status: "10m ago", inStock: false },
      { name: "Snake", status: "x1", inStock: true },
      { name: "Sand Spider", status: "10m ago", inStock: false },
      { name: "Scorpion", status: "5m ago", inStock: false },
      { name: "Royal Sphinx", status: "2h ago", inStock: false }
    ],
    abyss_ocean: [
      { name: "Parrotfish", status: "x3", inStock: true },
      { name: "Swordfish", status: "x1", inStock: true },
      { name: "Shark", status: "5m ago", inStock: false },
      { name: "Orca", status: "x1", inStock: true },
      { name: "Whale Shark", status: "15m ago", inStock: false },
      { name: "Beluga Whale", status: "10m ago", inStock: false },
      { name: "Kraken", status: "3h ago", inStock: false },
      { name: "El Maja", status: "8h ago", inStock: false }
    ],
    titan_temple: [
      { name: "Spideron", status: "x3", inStock: true },
      { name: "Crustacia", status: "x1", inStock: true },
      { name: "Bladehide", status: "5m ago", inStock: false },
      { name: "Mantaris", status: "x1", inStock: true },
      { name: "Rhinotaur", status: "15m ago", inStock: false },
      { name: "Mutant Shark", status: "2h ago", inStock: false },
      { name: "Gorilla King", status: "1h ago", inStock: false },
      { name: "Nightflame", status: "1d ago", inStock: false }
    ],
    jungle: [
      { name: "Chimpanzee", status: "x1", inStock: true },
      { name: "Toucan", status: "x1", inStock: true },
      { name: "Crocodile", status: "x1", inStock: true },
      { name: "Gorilla", status: "15m ago", inStock: false },
      { name: "Orangutini Ananassini", status: "5m ago", inStock: false },
      { name: "Spider", status: "x1", inStock: true },
      { name: "Tiger", status: "x1", inStock: true },
      { name: "King Snake", status: "5h ago", inStock: false }
    ],
    prehistoric: [
      { name: "Dodo", status: "x1", inStock: true },
      { name: "Pterodactyl", status: "x1", inStock: true },
      { name: "Ankylosaurus", status: "x3", inStock: true },
      { name: "Bronto", status: "15m ago", inStock: false },
      { name: "Triceratops", status: "35m ago", inStock: false },
      { name: "TRex", status: "2h ago", inStock: false },
      { name: "Tralaledon", status: "1h ago", inStock: false },
      { name: "Mosasaurus", status: "1h ago", inStock: false }
    ],
    angels: [
      { name: "Light Dove", status: "10m ago", inStock: false },
      { name: "Winged Lamb", status: "15m ago", inStock: false },
      { name: "Sacred Moth", status: "10m ago", inStock: false },
      { name: "Holy Peacock", status: "30m ago", inStock: false },
      { name: "Pure Jellyfish", status: "25m ago", inStock: false },
      { name: "Centaur", status: "8h ago", inStock: false },
      { name: "Pegasus", status: "1h ago", inStock: false },
      { name: "ArchAngel", status: "4d ago", inStock: false }
    ],
    demons: [
      { name: "Flame Sprite", status: "x3", inStock: true },
      { name: "Toro", status: "x2", inStock: true },
      { name: "Imp", status: "35m ago", inStock: false },
      { name: "Demon Hound", status: "5m ago", inStock: false },
      { name: "Gargoyle", status: "35m ago", inStock: false },
      { name: "RazorFang", status: "2h ago", inStock: false },
      { name: "Skeleton Horse", status: "4h ago", inStock: false },
      { name: "World Burner", status: "3d ago", inStock: false }
    ],
    enchanted_forest: [
      { name: "Prism Gecko", status: "x2", inStock: true },
      { name: "Petal Beetle", status: "x2", inStock: true },
      { name: "Enchanted Bluejay", status: "20m ago", inStock: false },
      { name: "Astral Jackalope", status: "x1", inStock: true },
      { name: "Spirit Panda", status: "25m ago", inStock: false },
      { name: "Starry Fox", status: "2h ago", inStock: false },
      { name: "Celestial Sunlion", status: "9h ago", inStock: false },
      { name: "Royal Skywhale", status: "2d ago", inStock: false }
    ],
    events: [
      { name: "Blood Moon", status: "5m ago", inStock: false },
      { name: "Pumpkin Moon", status: "1h ago", inStock: false },
      { name: "Butterfly Bloom", status: "25m ago", inStock: false }
    ],
    graveyard: [
      { name: "Whiskers", status: "x1", inStock: true },
      { name: "Jesterpop", status: "x3", inStock: true },
      { name: "Candlefang", status: "x1", inStock: true },
      { name: "Spirit Knight", status: "30m ago", inStock: false },
      { name: "Graveyard Brute", status: "1h ago", inStock: false },
      { name: "Ghost Reaper", status: "45m ago", inStock: false }
    ],
    haunted_swamp: [
      { name: "Hooded Gerbil", status: "x3", inStock: true },
      { name: "Toadstool", status: "x1", inStock: true },
      { name: "Patchwork Imp", status: "5m ago", inStock: false },
      { name: "Haunted Scorpio", status: "x1", inStock: true },
      { name: "BloodBloom", status: "50m ago", inStock: false },
      { name: "Shelltide Voyager", status: "6h ago", inStock: false }
    ],
    abandoned_manor: [
      { name: "Mimic Chest", status: "x2", inStock: true },
      { name: "Crowshade", status: "x1", inStock: true },
      { name: "Hexed Pumpkin", status: "x2", inStock: true },
      { name: "Werewolf", status: "20m ago", inStock: false },
      { name: "Gorillastein", status: "3h ago", inStock: false },
      { name: "Voidseer Pumpkin", status: "50m ago", inStock: false }
    ]
  };

  // Render cards into DOM
  function renderAllCards() {
    for (const [biomeKey, items] of Object.entries(ROSTER_DATA)) {
      const container = document.getElementById(`list-${biomeKey}`);
      if (!container) continue;

      container.innerHTML = items.map((item) => {
        const iconHtml = getPetIconHtml(item.name);
        
        if (item.inStock) {
          let colorClass = "status-in-stock";
          if (item.color === "yellow") colorClass = "status-yellow";
          else if (item.color === "blue") colorClass = "status-blue";
          
          return `
            <div class="card-item">
              <div class="item-left">
                ${iconHtml}
                <span class="item-name ${colorClass}">${item.name} ${item.status}</span>
              </div>
            </div>
          `;
        } else {
          return `
            <div class="card-item">
              <div class="item-left">
                ${iconHtml}
                <span class="item-name">${item.name}</span>
              </div>
              <span class="item-status status-time-ago">— ${item.status}</span>
            </div>
          `;
        }
      }).join("");
    }
  }

  // Live Countdowns Engine
  let newEggsSecs = 227;      // 3m 47s
  let pumpkinKingSecs = 780;  // 13m
  let eventSecs = 227;        // 3m 47s
  let updateSecs = 131308;    // 1d 12h 28m

  function formatMmSs(sec) {
    if (sec <= 0) return "0m 00s";
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}m ${s < 10 ? "0" : ""}${s}s`;
  }

  function formatDhm(totalSec) {
    if (totalSec <= 0) return "0d 00h 00m";
    const d = Math.floor(totalSec / 86400);
    const rem = totalSec % 86400;
    const h = Math.floor(rem / 3600);
    const m = Math.floor((rem % 3600) / 60);
    return `${d}d ${h}h ${m}m`;
  }

  function tickCountdowns() {
    // 1. New Eggs timer
    if (newEggsSecs > 0) newEggsSecs--;
    else newEggsSecs = 300; // resets every 5 mins
    const elNewEggs = document.getElementById("timer-new-eggs");
    if (elNewEggs) elNewEggs.textContent = formatMmSs(newEggsSecs);

    // 2. Event timer & progress bar
    if (eventSecs > 0) eventSecs--;
    else eventSecs = 600;
    const elEventTime = document.getElementById("event-timer-val");
    if (elEventTime) elEventTime.textContent = formatMmSs(eventSecs);
    const elProgressBar = document.getElementById("event-progress-bar");
    if (elProgressBar) {
      const pct = Math.max(0, Math.min(100, (eventSecs / 600) * 100));
      elProgressBar.style.width = `${pct}%`;
    }

    // 3. Pumpkin King timer
    if (pumpkinKingSecs > 0) pumpkinKingSecs--;
    else pumpkinKingSecs = 1800;
    const elPumpkin = document.getElementById("timer-pumpkin-king");
    if (elPumpkin) {
      const pm = Math.floor(pumpkinKingSecs / 60);
      elPumpkin.textContent = `${pm}m`;
    }

    // 4. Train timer (dynamic: pulses "NOW" while Phantom Express is in station, otherwise counts down)
    const elTrain = document.getElementById("timer-train");
    if (elTrain) {
      if (eventSecs > 0) {
        elTrain.textContent = "NOW";
        elTrain.classList.add("pulse-now");
      } else {
        elTrain.classList.remove("pulse-now");
        elTrain.textContent = formatMmSs(newEggsSecs);
      }
    }

    // 5. Update timer
    if (updateSecs > 0) updateSecs--;
    const elUpdate = document.getElementById("timer-update");
    if (elUpdate) elUpdate.textContent = formatDhm(updateSecs);
  }

  function getRosterBiomeKey(loc) {
    if (!loc) return "";
    const l = loc.toLowerCase().trim();
    if (l === "angels") return "angels";
    if (l === "demons") return "demons";
    if (l.includes("angel") && l.includes("demon")) return "demons";
    if (l.includes("enchant")) return "enchanted_forest";
    if (l.includes("cherry")) return "cherry_blossom";
    if (l.includes("abyss") || l.includes("ocean")) return "abyss_ocean";
    if (l.includes("titan") || l.includes("temple")) return "titan_temple";
    if (l.includes("haunt") || l.includes("swamp")) return "haunted_swamp";
    if (l.includes("abandon") || l.includes("manor")) return "abandoned_manor";
    return l.replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  }

  // Periodic API Sync with bot's /api/status if reachable
  async function syncWithApi() {
    try {
      const reqHeaders = {};
      if (token) reqHeaders["X-EggStock-Token"] = token;
      const res = await fetch(apiUrl, { cache: "no-store", headers: reqHeaders });
      if (!res.ok) return;
      const data = await res.json();

      // If next wave estimate exists, sync the new eggs timer
      if (data.next_wave_estimate && data.next_wave_estimate.overall && data.next_wave_estimate.overall.eta_seconds) {
        newEggsSecs = Math.max(0, Math.floor(data.next_wave_estimate.overall.eta_seconds));
      }

      // Check recent drops to flash updates in corresponding biome
      if (Array.isArray(data.recent_drops) && data.recent_drops.length > 0) {
        const lastDrop = data.recent_drops[0];
        const biomeKey = getRosterBiomeKey(lastDrop.location || "");
        if (ROSTER_DATA[biomeKey]) {
          // If egg exists in biome, mark as fresh
          const match = ROSTER_DATA[biomeKey].find(p => p.name.toLowerCase().includes((lastDrop.egg || "").toLowerCase()));
          if (match) {
            match.status = "x1";
            match.inStock = true;
            renderAllCards();
          }
        }
      }
    } catch (e) {
      // Graceful offline fallback -- local simulation continues flawlessly
    }
  }

  // Keyboard shortcut for Streamer:
  // 'P' -> Toggle mock gameplay backdrop
  // 'F' -> Toggle Fullscreen
  window.addEventListener("keydown", (e) => {
    if (e.key === "p" || e.key === "P") {
      const backdrop = document.getElementById("gameplay-preview-backdrop");
      if (backdrop) backdrop.classList.toggle("active");
    }
    if (e.key === "f" || e.key === "F") {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }
  });

  if (showPreview) {
    const backdrop = document.getElementById("gameplay-preview-backdrop");
    if (backdrop) backdrop.classList.add("active");
  }

  // Initialization
  renderAllCards();
  setInterval(tickCountdowns, 1000);
  setInterval(syncWithApi, 3000);
})();
