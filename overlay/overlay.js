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
    "king snake": imgBase + "snake_king.png"
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

  // ── Audio & Speech Alert Engine (OBS Local & Stream Audio) ──
  let alarmEnabled = true;
  let audioContext = null;
  let lastSpokenWaveSecond = null;

  function initAudio() {
    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioContext && audioContext.state === "suspended") {
      audioContext.resume();
    }
  }

  function playTone(freq = 660, duration = 0.2, type = "sine", delay = 0) {
    if (!alarmEnabled) return;
    try {
      initAudio();
      if (!audioContext) return;
      const osc = audioContext.createOscillator();
      const gain = audioContext.createGain();
      const startTime = audioContext.currentTime + delay;
      osc.type = type;
      osc.frequency.setValueAtTime(freq, startTime);
      gain.gain.setValueAtTime(0.3, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
      osc.connect(gain);
      gain.connect(audioContext.destination);
      osc.start(startTime);
      osc.stop(startTime + duration);
    } catch (e) {}
  }

  function speakAlert(text) {
    if (!alarmEnabled) return;
    try {
      initAudio();
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 1.15;
        utter.pitch = 1.05;
        utter.volume = 0.9;
        window.speechSynthesis.speak(utter);
      }
    } catch (e) {}
  }

  function checkWaveAlarms(s) {
    if (!alarmEnabled || s === null || s === undefined) return;
    const sec = Math.round(Number(s));

    // 30 seconds warning
    if (sec === 30 && lastSpokenWaveSecond !== 30) {
      lastSpokenWaveSecond = 30;
      playTone(660, 0.18, "sine", 0);
      playTone(880, 0.25, "sine", 0.18);
      speakAlert("Warning: 30 seconds until next egg wave!");
    }
    // 10 seconds urgent warning
    else if (sec === 10 && lastSpokenWaveSecond !== 10) {
      lastSpokenWaveSecond = 10;
      playTone(880, 0.12, "triangle", 0);
      playTone(1100, 0.12, "triangle", 0.14);
      playTone(880, 0.12, "triangle", 0.28);
      playTone(1100, 0.22, "triangle", 0.42);
      speakAlert("10 seconds until egg wave! Get ready!");
    }
    // 0 seconds - Wave spawned!
    else if (sec === 0 && lastSpokenWaveSecond !== 0) {
      lastSpokenWaveSecond = 0;
      const freqs = [440, 554.37, 659.25, 880];
      freqs.forEach((f, i) => playTone(f, 0.2 + i * 0.08, "sine", i * 0.14));
      speakAlert("Egg wave is here!");
    }
    else if (sec > 35) {
      if (lastSpokenWaveSecond !== null && lastSpokenWaveSecond <= 10) {
        lastSpokenWaveSecond = null;
      }
    }
  }

  // Unlock audio on any click/interaction (essential for OBS browser source)
  document.addEventListener("click", () => initAudio(), { once: true });

  // ── Synchronized In-Game Timers (Aligned with live Roblox server schedule) ──

  // 1. Pumpkin King: Spawns twice an hour at exactly :15 and :45
  function getPumpkinKingData() {
    const now = new Date();
    const m = now.getMinutes();
    const s = now.getSeconds();
    // Portal open window: 5 minutes (:15-:20 and :45-:50)
    if ((m >= 15 && m < 20) || (m >= 45 && m < 50)) {
      const rem = (m < 20 ? 20 - m : 50 - m) * 60 - s;
      return { active: true, text: "OPEN NOW", remainingSec: rem };
    }
    const targetMin = m < 15 ? 15 : (m < 45 ? 45 : 75);
    const rem = (targetMin - m) * 60 - s;
    const pm = Math.floor(rem / 60);
    return { active: false, text: `${pm}m`, remainingSec: rem };
  }

  // 2. Train / Phantom Express: Arrives at :00 and :30
  function getTrainData() {
    const now = new Date();
    const m = now.getMinutes();
    const s = now.getSeconds();
    // In station / boarding: 5 minutes (:00-:05 and :30-:35)
    if ((m >= 0 && m < 5) || (m >= 30 && m < 35)) {
      const rem = (m < 5 ? 5 - m : 35 - m) * 60 - s;
      return { inStation: true, text: "NOW", remainingSec: rem };
    }
    const targetMin = m < 30 ? 30 : 60;
    const rem = (targetMin - m) * 60 - s;
    return { inStation: false, text: formatMmSs(rem), remainingSec: rem };
  }

  // 3. New Eggs / Night Cycle (5-minute rotation: 4m 50s day, 10s night refresh)
  function getNewEggsRemaining() {
    const now = new Date();
    const secInCycle = (now.getMinutes() * 60 + now.getSeconds()) % 300;
    let rem = 300 - secInCycle + 6;
    if (rem > 300) rem -= 300;
    if (rem <= 0) rem = 300;
    return rem;
  }

  // 4. Weekly Update Countdown (Saturdays at 14:00 UTC)
  function getWeeklyUpdateRemaining() {
    const now = new Date();
    const target = new Date(now);
    target.setUTCHours(14, 0, 0, 0);
    const day = now.getUTCDay();
    let diffDays = (6 - day + 7) % 7;
    if (diffDays === 0 && now.getUTCHours() >= 14) {
      diffDays = 7;
    }
    target.setUTCDate(now.getUTCDate() + diffDays);
    return Math.max(0, Math.floor((target - now) / 1000));
  }

  function tickCountdowns() {
    // 1. New Eggs timer (Synchronized 5-min cycle)
    const eggsRem = getNewEggsRemaining();
    const elNewEggs = document.getElementById("timer-new-eggs");
    if (elNewEggs) elNewEggs.textContent = formatMmSs(eggsRem);
    checkWaveAlarms(eggsRem);

    // 2. Train & Event Pill (Synchronized 30-min schedule: :00 and :30)
    const train = getTrainData();
    const elTrain = document.getElementById("timer-train");
    if (elTrain) {
      elTrain.textContent = train.text;
      if (train.inStation) {
        elTrain.classList.add("pulse-now");
      } else {
        elTrain.classList.remove("pulse-now");
      }
    }

    const elEventTime = document.getElementById("event-timer-val");
    if (elEventTime) {
      elEventTime.textContent = train.inStation ? "BOARDING" : formatMmSs(train.remainingSec);
    }
    const elProgressBar = document.getElementById("event-progress-bar");
    if (elProgressBar) {
      const pct = Math.max(5, Math.min(100, ((1800 - train.remainingSec) / 1800) * 100));
      elProgressBar.style.width = `${pct}%`;
    }

    // 3. Pumpkin King timer (Synchronized twice per hour: :15 and :45)
    const pk = getPumpkinKingData();
    const elPumpkin = document.getElementById("timer-pumpkin-king");
    if (elPumpkin) {
      elPumpkin.textContent = pk.text;
      if (pk.active) elPumpkin.classList.add("pulse-now");
      else elPumpkin.classList.remove("pulse-now");
    }

    // 4. Update timer (Weekly Saturday update)
    const updSec = getWeeklyUpdateRemaining();
    const elUpdate = document.getElementById("timer-update");
    if (elUpdate) elUpdate.textContent = formatDhm(updSec);
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

  // =========================================================
  // Web Audio API Sound Alerts Engine (Synthesized loud gaming pings)
  // =========================================================
  let audioCtx = null;
  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === "suspended") {
      audioCtx.resume().catch(() => {});
    }
    return audioCtx;
  }

  function playAlertSound(rarity = "secret") {
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const now = ctx.currentTime;
      const r = (rarity || "").toLowerCase();

      if (r === "divine") {
        // Triumphant 4-tone ascending fanfare (C5 -> E5 -> G5 -> C6)
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "triangle";
          osc.frequency.setValueAtTime(freq, now + idx * 0.12);
          gain.gain.setValueAtTime(0.35, now + idx * 0.12);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.12 + 0.35);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.12);
          osc.stop(now + idx * 0.12 + 0.35);
        });
      } else if (r === "eternal") {
        // High-pitch 2-tone melodic chime
        const notes = [659.25, 987.77];
        notes.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(freq, now + idx * 0.14);
          gain.gain.setValueAtTime(0.3, now + idx * 0.14);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.14 + 0.4);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.14);
          osc.stop(now + idx * 0.14 + 0.4);
        });
      } else {
        // Crisp drop radar ping
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(1320, now + 0.18);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.45);
      }
    } catch (e) {
      console.warn("Audio alert failed", e);
    }
  }

  // Periodic API Sync with bot's /api/status if reachable
  let lastSeenDropTime = null;

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

      // Check recent drops to flash updates and trigger loud sound alerts
      if (Array.isArray(data.recent_drops) && data.recent_drops.length > 0) {
        const lastDrop = data.recent_drops[0];
        
        // Detect if this is a newly arrived drop
        if (lastDrop.time && lastDrop.time !== lastSeenDropTime) {
          if (lastSeenDropTime !== null) {
            // Play alert sound for stream!
            playAlertSound(lastDrop.rarity || "secret");
          }
          lastSeenDropTime = lastDrop.time;
        }

        const biomeKey = getRosterBiomeKey(lastDrop.location || "");
        if (ROSTER_DATA[biomeKey]) {
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
