(() => {
  // Query params for customization (?preview=true to test OBS cutout alignment)
  const params = new URLSearchParams(window.location.search);
  const showPreview = params.get("preview") === "true";
  const token = params.get("token") || window.__ES_TOKEN || "";
  
  // Connect to live production API by default when opened as a local file in OBS
  const isLocalFile = window.location.protocol === "file:";
  const defaultApi = isLocalFile ? "https://eggstock.xyz/api/status" : "/api/status";
  const apiUrl = params.get("api") || defaultApi;

  // Base path for pet images: relative for local file in OBS, absolute for web server
  const imgBase = isLocalFile ? "../website/images/pets/" : "/images/pets/";

  // Pre-mapped pet images
  const PET_IMG_MAP = {
    "winged lamb": imgBase + "winged_lamb.png",
    "toro": imgBase + "toro.png",
    "archangel": imgBase + "archangel.png",
    "kitsune": imgBase + "kitsune.png",
    "nightflame": imgBase + "nightflame.png",
    "unicorn": imgBase + "unicorn.png",
    "kraken": imgBase + "kraken.png",
    "gorilla king": imgBase + "gorilla_king.png",
    "mosasaurus": imgBase + "mosasaurus.png",
    "ice dragon": imgBase + "ice_dragon.png",
    "lava dragon": imgBase + "lava_dragon.png",
    "el maja": imgBase + "el_maja.png",
    "cerberus": imgBase + "cerberus.png",
    "pure jellyfish": imgBase + "pure_jellyfish.png",
    "gargoyle": imgBase + "gargoyle.png",
    "yeti": imgBase + "yeti.png",
    "trex": imgBase + "trex.png",
    "tralaledon": imgBase + "tralaledon.png",
    "oni tiger": imgBase + "oni_tiger.png",
    "phoenix": imgBase + "phoenix.png",
    "pegasus": imgBase + "pegasus.png",
    "centaur": imgBase + "centaur.png",
    "holy peacock": imgBase + "holy_peacock.png",
    "light dove": imgBase + "light_dove.png",
    "sacred moth": imgBase + "sacred_moth.png",
    "demon hound": imgBase + "demon_hound.png",
    "imp": imgBase + "imp.png",
    "flame sprite": imgBase + "flame_sprite.png",
    "razorfang": imgBase + "razorfang.png",
    "skeleton horse": imgBase + "skeleton_horse.png",
    "world burner": imgBase + "world_burner.png",
    "eternal lunar": imgBase + "eternal_lunar_dragon.png",
    "cosmic dragon": imgBase + "cosmic_dragon.png",
    "cosmic skeleton": imgBase + "cosmic_skeleton_boss.png",
    "stag": imgBase + "stag.png",
    "mutant shark": imgBase + "mutant_shark.png",
    "king snake": imgBase + "snake_king.png",
    "aetheron": imgBase + "aetheron.png",
    "equinox": imgBase + "equinox.png",
    "dr. scramble": imgBase + "dr_scramble.png"
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
    gerbil: "🐹", toadstool: "🍄", chest: "📦", crow: "🦅", wolf: "🐺",
    bloomfin: "🐠", vexlet: "👾", bloomspire: "🌸", glacigon: "🧊", redmaw: "👹", prowler: "🐆", rex: "🦖",
    jellynova: "🪼", flarefish: "🐡", tideler: "🌊", abyssjaw: "🦈", prismare: "🐴"
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
    alien_planet: [
      { name: "Bloomfin", status: "x1", inStock: true },
      { name: "Vexlet", status: "x1", inStock: true },
      { name: "Bloomspire", status: "24m ago", inStock: false },
      { name: "Glacigon", status: "x3", inStock: true },
      { name: "Redmaw", status: "24m ago", inStock: false },
      { name: "Aurora Stag", status: "4h ago", inStock: false },
      { name: "Viridian Prowler", status: "1h ago", inStock: false },
      { name: "Obsidian Rex", status: "Never", inStock: false }
    ],
    flooded_alien_planet: [
      { name: "Jellynova", status: "9m ago", inStock: false },
      { name: "Flarefish", status: "9m ago", inStock: false },
      { name: "Tideler", status: "2h ago", inStock: false },
      { name: "Abyssjaw", status: "49m ago", inStock: false },
      { name: "Prismare", status: "2d ago", inStock: false }
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


  // =========================================================
  // Render cards into DOM
  // =========================================================
  const JUST_DROPPED_WINDOW = 60; // seconds a fresh drop row keeps glowing
  const IN_STOCK_WINDOW = 240;    // seconds a drop counts as "in stock"

  function statusFromElapsed(elapsedSec) {
    if (elapsedSec < 60) return "just now";
    if (elapsedSec < 3600) return Math.floor(elapsedSec / 60) + "m ago";
    if (elapsedSec < 86400) return Math.floor(elapsedSec / 3600) + "h ago";
    return Math.floor(elapsedSec / 86400) + "d ago";
  }

  function renderAllCards() {
    const nowUnix = Math.floor(Date.now() / 1000);
    for (const [biomeKey, items] of Object.entries(ROSTER_DATA)) {
      const container = document.getElementById(`list-${biomeKey}`);
      if (!container) continue;

      container.innerHTML = items.map((item) => {
        const iconHtml = getPetIconHtml(item.name);
        const fresh = item.droppedAt && (nowUnix - item.droppedAt) < JUST_DROPPED_WINDOW;
        const rowClass = fresh ? "card-item just-dropped" : "card-item";

        if (item.inStock) {
          let colorClass = "status-in-stock";
          if (item.color === "yellow") colorClass = "status-yellow";
          else if (item.color === "blue") colorClass = "status-blue";
          return `
            <div class="${rowClass}">
              <div class="item-left">
                ${iconHtml}
                <span class="item-name ${colorClass}">${item.name} ${item.status}</span>
              </div>
            </div>`;
        }
        return `
          <div class="${rowClass}">
            <div class="item-left">
              ${iconHtml}
              <span class="item-name">${item.name}</span>
            </div>
            <span class="item-status status-time-ago">— ${item.status}</span>
          </div>`;
      }).join("");
    }
  }

  // =========================================================
  // Formatting helpers
  // =========================================================
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

  function formatAgoShort(sec) {
    if (sec < 60) return `${sec}s`;
    if (sec < 3600) return `${Math.floor(sec / 60)}m`;
    if (sec < 86400) return `${Math.floor(sec / 3600)}h`;
    return `${Math.floor(sec / 86400)}d`;
  }

  // =========================================================
  // Audio engine (native HTML5 WAV for OBS CEF)
  // =========================================================
  let alarmEnabled = params.get("mute") !== "true";
  const soundBase = isLocalFile ? "../website/sounds/" : "/sounds/";

  // Inaudible carrier keeps the OBS audio track alive so YouTube never sees 0 kbps
  function initAudioCarrier() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const carrierCtx = new AudioContext();
      const osc = carrierCtx.createOscillator();
      const gain = carrierCtx.createGain();
      gain.gain.value = 0.00001;
      osc.frequency.value = 440;
      osc.connect(gain);
      gain.connect(carrierCtx.destination);
      osc.start();
      setInterval(() => {
        if (carrierCtx.state === "suspended") carrierCtx.resume().catch(() => {});
      }, 3000);
    } catch (e) {}
  }
  initAudioCarrier();

  // Pre-create audio objects so the first alert plays without a fetch delay
  const SOUNDS = {};
  ["warning_30s.wav", "urgent_10s.wav", "drop_chime.wav", "divine_chord.wav", "train_bell.wav"].forEach((f) => {
    try {
      const a = new Audio(soundBase + f);
      a.preload = "auto";
      SOUNDS[f] = a;
    } catch (e) {}
  });

  function playSoundFile(filename) {
    if (!alarmEnabled) return;
    try {
      const base = SOUNDS[filename];
      const audio = base ? base.cloneNode() : new Audio(soundBase + filename);
      audio.volume = 1.0;
      const p = audio.play();
      if (p !== undefined) p.catch(() => {});
    } catch (e) {}
  }

  function playAlertSound(rarity = "secret") {
    const r = (rarity || "").toLowerCase();
    playSoundFile(r === "divine" ? "divine_chord.wav" : "drop_chime.wav");
  }

  let lastSpokenWaveSecond = null;
  function checkWaveAlarms(s) {
    if (!alarmEnabled || s === null || s === undefined) return;
    const sec = Math.round(Number(s));
    if (sec === 30 && lastSpokenWaveSecond !== 30) {
      lastSpokenWaveSecond = 30;
      playSoundFile("warning_30s.wav");
    } else if (sec === 10 && lastSpokenWaveSecond !== 10) {
      lastSpokenWaveSecond = 10;
      playSoundFile("urgent_10s.wav");
    } else if (sec === 0 && lastSpokenWaveSecond !== 0) {
      lastSpokenWaveSecond = 0;
      playSoundFile("drop_chime.wav");
    } else if (sec > 35 && lastSpokenWaveSecond !== null) {
      lastSpokenWaveSecond = null;
    }
  }

  let lastTrainBellMinute = -1;
  function checkTrainBell(train) {
    if (!alarmEnabled || !train.inStation) return;
    const m = new Date().getMinutes();
    if (m !== lastTrainBellMinute && (m === 0 || m === 30)) {
      lastTrainBellMinute = m;
      playSoundFile("train_bell.wav");
    }
  }

  // =========================================================
  // Synchronized in-game timers (Roblox server schedule)
  // =========================================================
  // Pumpkin King: :15 and :45, portal open 5 min
  function getPumpkinKingData() {
    const now = new Date();
    const m = now.getMinutes();
    const s = now.getSeconds();
    if ((m >= 15 && m < 20) || (m >= 45 && m < 50)) {
      const rem = (m < 20 ? 20 - m : 50 - m) * 60 - s;
      return { active: true, text: "OPEN NOW", remainingSec: rem };
    }
    const targetMin = m < 15 ? 15 : (m < 45 ? 45 : 75);
    const rem = (targetMin - m) * 60 - s;
    return { active: false, text: formatMmSs(rem), remainingSec: rem };
  }

  // Phantom Express: :00 and :30, boarding 5 min
  function getTrainData() {
    const now = new Date();
    const m = now.getMinutes();
    const s = now.getSeconds();
    if ((m >= 0 && m < 5) || (m >= 30 && m < 35)) {
      const rem = (m < 5 ? 5 - m : 35 - m) * 60 - s;
      return { inStation: true, text: "NOW", remainingSec: rem };
    }
    const targetMin = m < 30 ? 30 : 60;
    const rem = (targetMin - m) * 60 - s;
    return { inStation: false, text: formatMmSs(rem), remainingSec: rem };
  }

  // New Eggs: radar ETA when the API is fresh, otherwise the fixed 5-minute cycle
  let waveTargetMs = null;   // absolute time of the next wave from /api/status
  let waveSyncedAt = 0;      // when that ETA was received
  const WAVE_SYNC_MAX_AGE = 45000;

  function getNewEggsRemaining() {
    if (waveTargetMs && (Date.now() - waveSyncedAt) < WAVE_SYNC_MAX_AGE) {
      return Math.max(0, Math.round((waveTargetMs - Date.now()) / 1000));
    }
    const now = new Date();
    const secInCycle = (now.getMinutes() * 60 + now.getSeconds()) % 300;
    let rem = 300 - secInCycle + 6;
    if (rem > 300) rem -= 300;
    if (rem <= 0) rem = 300;
    return rem;
  }

  // Weekly update: Saturdays 14:00 UTC
  function getWeeklyUpdateRemaining() {
    const now = new Date();
    const target = new Date(now);
    target.setUTCHours(14, 0, 0, 0);
    const day = now.getUTCDay();
    let diffDays = (6 - day + 7) % 7;
    if (diffDays === 0 && now.getUTCHours() >= 14) diffDays = 7;
    target.setUTCDate(now.getUTCDate() + diffDays);
    return Math.max(0, Math.floor((target - now) / 1000));
  }

  function setUrgency(el, rem, spawningText) {
    el.classList.remove("warn", "urgent", "spawning", "pulse-now");
    if (rem <= 0) {
      el.textContent = spawningText;
      el.classList.add("spawning");
    } else if (rem <= 10) {
      el.classList.add("urgent");
    } else if (rem <= 30) {
      el.classList.add("warn");
    }
  }

  function tickCountdowns() {
    const eggsRem = getNewEggsRemaining();
    const elNewEggs = document.getElementById("timer-new-eggs");
    if (elNewEggs) {
      elNewEggs.textContent = formatMmSs(eggsRem);
      setUrgency(elNewEggs, eggsRem, "SPAWNING!");
    }
    checkWaveAlarms(eggsRem);

    const train = getTrainData();
    const elTrain = document.getElementById("timer-train");
    if (elTrain) {
      elTrain.textContent = train.text;
      elTrain.classList.toggle("pulse-now", train.inStation);
    }
    checkTrainBell(train);

    const pk = getPumpkinKingData();
    const elPumpkin = document.getElementById("timer-pumpkin-king");
    if (elPumpkin) {
      elPumpkin.textContent = pk.text;
      elPumpkin.classList.toggle("pulse-now", pk.active);
    }

    const elUpdate = document.getElementById("timer-update");
    if (elUpdate) elUpdate.textContent = formatDhm(getWeeklyUpdateRemaining());

    tickDropPill();
  }

  // =========================================================
  // Latest drop pill (top centre)
  // =========================================================
  let latestDrop = null; // { egg, rarity, location, ts }

  function tickDropPill() {
    const elTime = document.getElementById("drop-pill-time");
    const elBar = document.getElementById("drop-pill-bar");
    if (!latestDrop || !elTime || !elBar) return;
    const ago = Math.max(0, Math.floor(Date.now() / 1000) - latestDrop.ts);
    elTime.textContent = formatAgoShort(ago);
    const pct = Math.max(0, 100 - (ago / IN_STOCK_WINDOW) * 100);
    elBar.style.width = `${pct}%`;
  }

  function showDropPill(drop, isNew) {
    latestDrop = drop;
    const r = (drop.rarity || "secret").toLowerCase();
    const pill = document.getElementById("drop-pill");
    const elIcon = document.getElementById("drop-pill-icon");
    const elTag = document.getElementById("drop-pill-tag");
    const elTitle = document.getElementById("drop-pill-title");
    const elBar = document.getElementById("drop-pill-bar");
    if (elIcon) elIcon.innerHTML = getPetIconHtml(drop.egg);
    if (elTag) {
      elTag.textContent = `${(drop.location || "RADAR").toUpperCase()} • ${r.toUpperCase()}`;
      elTag.className = `event-tag-badge tag-${r}`;
    }
    if (elTitle) elTitle.textContent = drop.egg;
    if (elBar) elBar.className = `event-progress-bar bar-${r}`;
    tickDropPill();

    if (isNew && pill) {
      pill.classList.remove("flash", "flash-divine", "flash-eternal");
      void pill.offsetWidth; // restart animation
      pill.classList.add("flash");
      if (r === "divine") pill.classList.add("flash-divine");
      if (r === "eternal") pill.classList.add("flash-eternal");
      setTimeout(() => pill.classList.remove("flash", "flash-divine", "flash-eternal"), 3000);
    }
  }

  function setSyncState(online) {
    const dot = document.getElementById("sync-dot");
    if (!dot) return;
    dot.classList.toggle("online", online);
    dot.classList.toggle("offline", !online);
  }

  // =========================================================
  // Roster matching
  // =========================================================
  function getRosterBiomeKey(loc) {
    if (!loc) return "";
    const l = loc.toLowerCase().trim();
    if (l === "angels") return "angels";
    if (l === "demons") return "demons";
    if (l.includes("angel") && l.includes("demon")) return "demons";
    if (l.includes("flooded")) return "flooded_alien_planet";
    if (l.includes("alien")) return "alien_planet";
    if (l.includes("enchant")) return "enchanted_forest";
    if (l.includes("cherry")) return "cherry_blossom";
    if (l.includes("abyss") || l.includes("ocean")) return "abyss_ocean";
    if (l.includes("titan") || l.includes("temple")) return "titan_temple";
    if (l.includes("haunt") || l.includes("swamp")) return "haunted_swamp";
    if (l.includes("abandon") || l.includes("manor")) return "abandoned_manor";
    return l.replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
  }

  function findRosterPet(petName, preferredBiome) {
    const n = petName.toLowerCase().trim();
    if (!n) return null;
    const order = preferredBiome && ROSTER_DATA[preferredBiome]
      ? [preferredBiome, ...Object.keys(ROSTER_DATA).filter((k) => k !== preferredBiome)]
      : Object.keys(ROSTER_DATA);
    for (const key of order) {
      const exact = ROSTER_DATA[key].find((p) => p.name.toLowerCase().trim() === n);
      if (exact) return exact;
    }
    for (const key of order) {
      const loose = ROSTER_DATA[key].find((p) => {
        const pn = p.name.toLowerCase().trim();
        return pn.includes(n) || n.includes(pn);
      });
      if (loose) return loose;
    }
    return null;
  }

  function applyDropToRoster(pet, elapsedSec, dropTs) {
    if (elapsedSec < IN_STOCK_WINDOW) {
      pet.status = "x1";
      pet.inStock = true;
    } else {
      pet.inStock = false;
      pet.status = statusFromElapsed(elapsedSec);
    }
    if (dropTs && (!pet.droppedAt || dropTs > pet.droppedAt)) pet.droppedAt = dropTs;
  }

  // =========================================================
  // Live sync with /api/status
  // =========================================================
  let lastSeenDropTime = null;
  let consecutiveFailures = 0;

  async function syncWithApi() {
    try {
      const reqHeaders = {};
      if (token) reqHeaders["X-EggStock-Token"] = token;
      const res = await fetch(apiUrl, { cache: "no-store", headers: reqHeaders });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      consecutiveFailures = 0;
      setSyncState(true);

      const nowUnix = Math.floor(Date.now() / 1000);

      // Wave ETA from the radar
      const eta = data.next_wave_estimate && data.next_wave_estimate.overall
        ? data.next_wave_estimate.overall.eta_seconds
        : null;
      if (eta !== null && eta !== undefined) {
        waveTargetMs = Date.now() + Math.max(0, Math.floor(eta)) * 1000;
        waveSyncedAt = Date.now();
      }

      // Last-seen timestamps for every tracked pet
      if (data.last_seen_snapshot && data.last_seen_snapshot.sections) {
        for (const list of Object.values(data.last_seen_snapshot.sections)) {
          if (!Array.isArray(list)) continue;
          list.forEach((livePet) => {
            const pet = findRosterPet(livePet.name || "");
            if (!pet) return;
            const ts = livePet.ts || nowUnix;
            applyDropToRoster(pet, Math.max(0, nowUnix - ts), ts);
          });
        }
      }

      // Recent drops: newest first
      if (Array.isArray(data.recent_drops) && data.recent_drops.length > 0) {
        const lastDrop = data.recent_drops[0];
        const dropTs = lastDrop.time ? Math.floor(Date.parse(lastDrop.time) / 1000) : nowUnix;
        const isNew = !!lastDrop.time && lastDrop.time !== lastSeenDropTime;
        const firstSync = lastSeenDropTime === null;

        if (isNew) {
          if (!firstSync) playAlertSound(lastDrop.rarity || "secret");
          lastSeenDropTime = lastDrop.time;
        }

        showDropPill({
          egg: lastDrop.egg || "Unknown",
          rarity: lastDrop.rarity || "secret",
          location: lastDrop.location || "",
          ts: isNaN(dropTs) ? nowUnix : dropTs
        }, isNew && !firstSync);

        data.recent_drops.slice(0, 20).forEach((d) => {
          const ts = d.time ? Math.floor(Date.parse(d.time) / 1000) : nowUnix;
          const pet = findRosterPet(d.egg || "", getRosterBiomeKey(d.location || ""));
          if (pet) applyDropToRoster(pet, Math.max(0, nowUnix - (isNaN(ts) ? nowUnix : ts)), ts);
        });
      }

      renderAllCards();
    } catch (e) {
      consecutiveFailures++;
      if (consecutiveFailures >= 3) setSyncState(false);
    }
  }

  // =========================================================
  // Streamer hotkeys: P backdrop, F fullscreen, M mute, T test alert
  // =========================================================
  window.addEventListener("keydown", (e) => {
    const k = e.key.toLowerCase();
    if (k === "p") {
      const backdrop = document.getElementById("gameplay-preview-backdrop");
      if (backdrop) backdrop.classList.toggle("active");
    } else if (k === "f") {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {});
      else document.exitFullscreen().catch(() => {});
    } else if (k === "m") {
      alarmEnabled = !alarmEnabled;
    } else if (k === "t") {
      showDropPill({ egg: "Pure Jellyfish", rarity: "secret", location: "Angels", ts: Math.floor(Date.now() / 1000) }, true);
      playAlertSound("secret");
    }
  });

  if (showPreview) {
    const backdrop = document.getElementById("gameplay-preview-backdrop");
    if (backdrop) backdrop.classList.add("active");
  }

  // Initialization
  renderAllCards();
  tickCountdowns();
  setInterval(tickCountdowns, 1000);
  setInterval(renderAllCards, 30000); // keep "Xm ago" labels moving even if the API is quiet
  syncWithApi();
  setInterval(syncWithApi, 3000);
})();
