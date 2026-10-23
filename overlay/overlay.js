(() => {
  const params = new URLSearchParams(window.location.search);
  const apiUrl = params.get("api") || "/api/status";
  const panelParam = params.get("panel");
  if (panelParam) {
    document.body.classList.add("panel-mode", `panel-${panelParam.toLowerCase()}`);
  }
  const riftParam = params.get("rift");
  if (riftParam === "true" || riftParam === "1") {
    const riftEl = document.getElementById("rift-hud");
    if (riftEl) riftEl.style.display = "block";
  }
  const pollMs = 2000;
  let lastData = null;

  const $ = (id) => document.getElementById(id);

  // Tiny striped egg SVG for table rows
  const TINY_EGG_SVG = `
    <svg class="egg-tiny-icon" viewBox="0 0 100 125" aria-hidden="true">
      <defs>
        <radialGradient id="tEgg" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stop-color="#ffe770"/>
          <stop offset="40%" stop-color="#f59e0b"/>
          <stop offset="100%" stop-color="#92400e"/>
        </radialGradient>
        <clipPath id="tClip">
          <path d="M50 4 C24 4, 6 36, 6 78 C6 104, 26 122, 50 122 C74 122, 94 104, 94 78 C94 36, 76 4, 50 4 Z"/>
        </clipPath>
      </defs>
      <path d="M50 4 C24 4, 6 36, 6 78 C6 104, 26 122, 50 122 C74 122, 94 104, 94 78 C94 36, 76 4, 50 4 Z" fill="url(#tEgg)" stroke="#451a03" stroke-width="6"/>
      <g clip-path="url(#tClip)" stroke="#78350f" stroke-width="12" opacity="0.85">
        <line x1="-20" y1="30" x2="120" y2="90" />
        <line x1="-20" y1="65" x2="120" y2="125" />
      </g>
    </svg>
  `;

  // Biome icons mapping
  function getBiomeIconSvg(biome) {
    const b = (biome || "").toLowerCase();
    if (b.includes("snow") || b.includes("ice") || b.includes("winter") || b.includes("frost")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"><path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M19.07 4.93L4.93 19.07M8 4l4 4 4-4M8 20l4-4 4 4M4 8l4 4-4 4M20 8l-4 4 4 4"/></svg>`;
    }
    if (b.includes("prehistoric") || b.includes("dino") || b.includes("jurassic")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#4ade80"><path d="M19 4h-5l-2 3H8C5.2 7 4 9.5 4 12v3l2 2h2l1 4h3l-1-4h3l2-3h2v-4l2-2V6l-2-2z"/></svg>`;
    }
    if (b.includes("cosmic") || b.includes("space") || b.includes("galaxy") || b.includes("void")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2"><circle cx="12" cy="12" r="4.5" fill="#4f46e5"/><ellipse cx="12" cy="12" rx="10" ry="3.5" transform="rotate(-30 12 12)"/></svg>`;
    }
    if (b.includes("titan") || b.includes("temple") || b.includes("ancient") || b.includes("greek")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#94a3b8"><path d="M2 6l10-4 10 4v2H2V6zm2 4h3v9H4v-9zm6 0h4v9h-4v-9zm7 0h3v9h-3v-9zM2 21h20v2H2v-2z"/></svg>`;
    }
    if (b.includes("ocean") || b.includes("abyss") || b.includes("sea") || b.includes("water") || b.includes("kraken")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2.5" stroke-linecap="round"><path d="M2 11c2.5 0 2.5-2 5-2s2.5 2 5 2 2.5-2 5-2 2.5 2 5 2M2 16c2.5 0 2.5-2 5-2s2.5 2 5 2 2.5-2 5-2 2.5 2 5 2"/></svg>`;
    }
    if (b.includes("volcano") || b.includes("lava") || b.includes("fire") || b.includes("magma")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#f97316"><path d="M2 22h20L15 4l-3 4-3-4L2 22zm9-12l1 2 1-2 2 3-4 6-4-6 2-3h2z"/></svg>`;
    }
    if (b.includes("desert") || b.includes("sand") || b.includes("pyramid")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#eab308"><path d="M1 21h22L12 4 1 21zm11-12.8L17.5 19h-11L12 8.2z"/></svg>`;
    }
    if (b.includes("candy") || b.includes("sweet")) {
      return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#f472b6"><circle cx="12" cy="8" r="6"/><path d="M12 14v8" stroke="#f472b6" stroke-width="2.5"/></svg>`;
    }
    return `<svg class="biome-icon" viewBox="0 0 24 24" fill="#64748b"><circle cx="12" cy="12" r="6"/></svg>`;
  }

  // Wave timer: format as MM:SS normally, or HH:MM:SS if >59 minutes
  function formatWaveTimer(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return "--:--";
    const totalSec = Math.max(0, Math.floor(Number(value)));
    const hours = Math.floor(totalSec / 3600);
    const mins = Math.floor((totalSec % 3600) / 60);
    const secs = totalSec % 60;
    if (hours > 0) {
      return `${hours.toString().padStart(2,"0")}:${mins.toString().padStart(2,"0")}:${secs.toString().padStart(2,"0")}`;
    }
    return `${mins.toString().padStart(2,"0")}:${secs.toString().padStart(2,"0")}`;
  }


  // Standard elapsed duration format: HH:MM:SS (e.g. 00:01:01)
  function formatHms(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return "--:--:--";
    let seconds = Math.max(0, Math.floor(Number(value)));
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return [hours, minutes, secs].map((unit) => unit.toString().padStart(2, "0")).join(":");
  }

  // 12-hour clock time (e.g. 10:40 PM)
  function format12hTime(iso) {
    if (!iso) return "--:--";
    const date = new Date(iso);
    if (Number.isNaN(date.valueOf())) return "--:--";
    return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", hour12: true }).toUpperCase();
  }

  // Live New York time and date for the Roblox badge
  function updateRobloxClock() {
    const now = new Date();
    try {
      const timeStr = now.toLocaleTimeString("en-US", {
        timeZone: "America/New_York",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      }).toUpperCase();
      const monthStr = now.toLocaleDateString("en-US", {
        timeZone: "America/New_York",
        month: "short",
      }).toUpperCase();
      const dayStr = now.toLocaleDateString("en-US", {
        timeZone: "America/New_York",
        day: "2-digit",
      });
      if ($("roblox-time")) $("roblox-time").textContent = timeStr;
      if ($("roblox-date")) $("roblox-date").textContent = `NY · ${monthStr} ${dayStr}`;
    } catch {
      const timeStr = now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", hour12: true }).toUpperCase();
      if ($("roblox-time")) $("roblox-time").textContent = timeStr;
      if ($("roblox-date")) $("roblox-date").textContent = "NY · ROBLOX";
    }

    if ($("clock")) {
      $("clock").textContent = `UTC ${now.toISOString().slice(11, 19)}`;
    }
  }

  // Admin abuse event calculation (Saturday 15:00 UTC / 11 AM ET)
  function getNextAdminEvent() {
    const now = new Date();
    const target = new Date(now);
    const daysUntilSaturday = (6 - now.getUTCDay() + 7) % 7;
    target.setUTCDate(now.getUTCDate() + daysUntilSaturday);
    target.setUTCHours(15, 0, 0, 0);
    if (target <= now) target.setUTCDate(target.getUTCDate() + 7);

    const diffSeconds = Math.max(0, Math.floor((target - now) / 1000));
    const days = Math.floor(diffSeconds / 86400);
    const hours = Math.floor((diffSeconds % 86400) / 3600);
    const minutes = Math.floor((diffSeconds % 3600) / 60);
    const seconds = diffSeconds % 60;

    const countdown = days > 0
      ? `${days}D ${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
      : `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

    let subtext = "SATURDAY 11 AM ET";
    try {
      const monthStr = target.toLocaleDateString("en-US", { timeZone: "America/New_York", month: "short" }).toUpperCase();
      const dayStr = target.toLocaleDateString("en-US", { timeZone: "America/New_York", day: "2-digit" });
      subtext = `${monthStr} ${dayStr} · 11 AM ET`;
    } catch {
      // keep fallback
    }

    return { countdown, subtext };
  }

  // Rift Boss timer: opens every 30 minutes exactly at :00 and :30 past the hour.
  // Purely clock-based — no API needed.
  function updateRift() {
    const now = new Date();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();

    // Seconds elapsed since last :00 or :30 mark
    const secsIntoSlot = (minutes % 30) * 60 + seconds;
    // Rifts open at mark, last ~2 minutes for the fight
    const RIFT_OPEN_DURATION = 120; // 2 minutes
    const SLOT_SECONDS = 1800; // 30 minutes

    const riftEl = $("rift-time");
    const riftScreen = $("rift-screen");
    const riftAt = $("rift-at");
    const riftDetail = $("rift-detail");

    if (secsIntoSlot < RIFT_OPEN_DURATION) {
      // Rift is OPEN right now!
      if (riftEl) {
        riftEl.textContent = "OPEN!";
        riftEl.classList.remove("digits-imminent");
        riftEl.classList.add("rift-open");
      }
      if (riftScreen) {
        riftScreen.classList.remove("rift-imminent");
        riftScreen.classList.add("rift-active");
      }
      if (riftDetail) riftDetail.textContent = "⚡ RIFT IS OPEN — FIGHT NOW!";
      if (riftAt) riftAt.textContent = `CLOSES IN ${RIFT_OPEN_DURATION - secsIntoSlot}s`;
    } else {
      // Count down to next :00 or :30
      const secsUntilNext = SLOT_SECONDS - secsIntoSlot;
      const mm = Math.floor(secsUntilNext / 60);
      const ss = secsUntilNext % 60;
      if (riftEl) {
        riftEl.textContent = `${mm.toString().padStart(2,"0")}:${ss.toString().padStart(2,"0")}`;
        riftEl.classList.remove("rift-open");
      }

      if (secsUntilNext <= 60) {
        // Last 60s warning before opening
        if (riftScreen) {
          riftScreen.classList.remove("rift-active");
          riftScreen.classList.add("rift-imminent");
        }
        if (riftEl) riftEl.classList.add("digits-imminent");
        if (riftDetail) riftDetail.textContent = "⚠️ RIFT OPENING IMMINENT!";
      } else {
        if (riftScreen) riftScreen.classList.remove("rift-active", "rift-imminent");
        if (riftEl) riftEl.classList.remove("digits-imminent");
        if (riftDetail) riftDetail.textContent = "EVERY 30 MIN · SERVER-WIDE";
      }

      // Compute when next rift opens (next :00 or :30)
      if (riftAt) {
        const nextOpen = new Date(now.getTime() + secsUntilNext * 1000);
        const atStr = nextOpen.toLocaleTimeString("en-US", {
          hour: "numeric", minute: "2-digit", hour12: true, timeZone: "America/New_York"
        }).toUpperCase();
        riftAt.textContent = `OPENS AT ${atStr} ET`;
      }
    }
  }

  function setConnection(isOnline, label) {
    const indicator = $("status-indicator");
    const statusText = $("connection-status");
    if (indicator) {
      indicator.className = `status-indicator ${isOnline ? "" : "error"}`;
    }
    if (statusText) {
      statusText.textContent = label;
    }
  }

  // ── Audio & Speech Alert Engine (30s + 10s Voice Alerts) ──
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

  function playTone(freq = 600, duration = 0.2, type = "sine") {
    if (!alarmEnabled) return;
    try {
      initAudio();
      if (!audioContext) return;
      const osc = audioContext.createOscillator();
      const gain = audioContext.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioContext.currentTime);
      gain.gain.setValueAtTime(0.3, audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioContext.destination);
      osc.start();
      osc.stop(audioContext.currentTime + duration);
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
        utter.volume = 1.0;
        window.speechSynthesis.speak(utter);
      }
    } catch (e) {}
  }

  function flashAlarmBox() {
    const el = $("alarm-box");
    if (!el) return;
    el.classList.add("alarm-box-flashing");
    setTimeout(() => el.classList.remove("alarm-box-flashing"), 3200);
  }

  function checkWaveAlarms(seconds) {
    if (!alarmEnabled || seconds === null || seconds === undefined) return;
    const s = Math.round(Number(seconds));

    // 30 seconds warning
    if (s === 30 && lastSpokenWaveSecond !== 30) {
      lastSpokenWaveSecond = 30;
      playTone(660, 0.18, "sine");
      setTimeout(() => playTone(880, 0.22, "sine"), 180);
      speakAlert("Warning: 30 seconds until next egg wave!");
      flashAlarmBox();
    }
    // 10 seconds urgent warning
    else if (s === 10 && lastSpokenWaveSecond !== 10) {
      lastSpokenWaveSecond = 10;
      playTone(880, 0.15, "triangle");
      setTimeout(() => playTone(1100, 0.25, "triangle"), 150);
      speakAlert("10 seconds until egg wave! Get ready!");
      flashAlarmBox();
    }
    // 0 seconds - Wave spawned!
    else if (s === 0 && lastSpokenWaveSecond !== 0) {
      lastSpokenWaveSecond = 0;
      playTone(523.25, 0.12, "triangle");
      setTimeout(() => playTone(659.25, 0.12, "triangle"), 120);
      setTimeout(() => playTone(783.99, 0.12, "triangle"), 240);
      setTimeout(() => playTone(1046.50, 0.35, "triangle"), 360);
      speakAlert("Egg wave is here!");
      flashAlarmBox();
    }
    // Reset gate when countdown resets to a higher number
    else if (s > 35) {
      if (lastSpokenWaveSecond !== null && lastSpokenWaveSecond <= 10) {
        lastSpokenWaveSecond = null;
      }
    }
  }

  function toggleAlarm() {
    initAudio();
    alarmEnabled = !alarmEnabled;
    const statusText = $("alarm-status-text");
    const led = $("alarm-led");
    const box = $("alarm-box");
    if (alarmEnabled) {
      if (statusText) statusText.textContent = "ALARM ON";
      if (box) box.classList.remove("alarm-muted");
      if (led) led.classList.remove("led-off");
      playTone(750, 0.15);
      speakAlert("Alarm activated! 30 seconds and 10 seconds voice alerts on.");
    } else {
      if (statusText) statusText.textContent = "ALARM MUTED";
      if (box) box.classList.add("alarm-muted");
      if (led) led.classList.add("led-off");
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    }
  }

  function updateWave(wave) {
    const eta = wave?.eta_seconds;
    const samples = wave?.sample_size || 0;
    const confidence = wave?.confidence || "none";
    const colors = { none: "#ffc857", low: "#ff9f68", medium: "#4ce6ff", good: "#7be81a" };
    const widths = { none: "8%", low: "32%", medium: "66%", good: "100%" };

    const waveScreen = $("wave-screen");
    const waveEl = $("wave-time");

    if (waveEl) {
      waveEl.textContent = eta === null || eta === undefined ? "--:--" : formatWaveTimer(eta);
    }

    // Check voice & audio alarms at 30s, 10s, 0s
    checkWaveAlarms(eta);

    // Dynamic animations depending on remaining seconds
    if (typeof eta === "number") {
      if (eta <= 5) {
        // Wave arrived / spawning right now!
        if (waveScreen) {
          waveScreen.classList.remove("wave-imminent");
          waveScreen.classList.add("wave-arrived");
        }
        if (waveEl) {
          waveEl.classList.remove("digits-imminent");
          waveEl.classList.add("digits-arrived");
        }
      } else if (eta <= 30) {
        // Imminent countdown warning
        if (waveScreen) {
          waveScreen.classList.remove("wave-arrived");
          waveScreen.classList.add("wave-imminent");
        }
        if (waveEl) {
          waveEl.classList.remove("digits-arrived");
          waveEl.classList.add("digits-imminent");
        }
      } else {
        // Normal state
        if (waveScreen) waveScreen.classList.remove("wave-imminent", "wave-arrived");
        if (waveEl) waveEl.classList.remove("digits-imminent", "digits-arrived");
      }
    } else {
      if (waveScreen) waveScreen.classList.remove("wave-imminent", "wave-arrived");
      if (waveEl) waveEl.classList.remove("digits-imminent", "digits-arrived");
    }

    if ($("wave-detail")) {
      $("wave-detail").textContent = wave?.interval_seconds
        ? `MEDIAN GAP · ${formatWaveTimer(wave.interval_seconds)}`
        : "CALIBRATING FROM LIVE DROPS";
    }
    if ($("wave-basis")) {
      $("wave-basis").textContent = wave?.basis === "observed" ? "ESTIMATE: OBSERVED" : "ESTIMATE: FALLBACK";
    }
    if ($("wave-samples")) {
      $("wave-samples").textContent = `${samples} SAMPLE${samples === 1 ? "" : "S"}`;
    }
    const fill = $("confidence-fill");
    if (fill) {
      fill.style.width = widths[confidence] || "8%";
      fill.style.background = colors[confidence] || "#7be81a";
    }
  }


  // Render drops feed chronologically (oldest at top -> newest at bottom)
  function renderFeed(drops) {
    const feed = $("drop-feed");
    if (!feed) return;

    if (!Array.isArray(drops) || drops.length === 0) {
      feed.innerHTML = '<div class="empty-feed">LISTENING FOR LIVE DROPS...</div>';
      return;
    }

    // bot stores deque with appendleft (newest at index 0).
    // Take the 10 most recent drops and reverse them so newest is at the bottom, matching Image 1!
    const recent = drops.slice(0, 10).reverse();

    feed.replaceChildren(...recent.map((drop, idx) => {
      const isNewest = (idx === recent.length - 1);
      const row = document.createElement("article");
      row.className = `drop-row ${isNewest ? "drop-row--newest" : ""}`;

      // 1. Order badge: LAST DROP vs NEWEST
      const orderBadge = document.createElement("div");
      orderBadge.className = `badge-order ${isNewest ? "order--newest" : "order--last"}`;
      orderBadge.textContent = isNewest ? "NEWEST" : "LAST DROP";

      // 2. Time badge
      const timeBadge = document.createElement("div");
      timeBadge.className = "badge-time";
      timeBadge.textContent = format12hTime(drop.time);

      // 3. Rarity badge
      const rarity = (drop.rarity || "secret").toLowerCase();
      const rarityBadge = document.createElement("div");
      rarityBadge.className = `badge-rarity rarity-tag--${rarity}`;
      rarityBadge.textContent = rarity.toUpperCase();

      // 4. Egg detail (icon + name) + Biome detail (icon + name)
      const detail = document.createElement("div");
      detail.className = "egg-detail";

      detail.innerHTML = `
        ${TINY_EGG_SVG}
        <span class="egg-name">${drop.egg || "Unknown"}</span>
        <div class="biome-badge">
          ${getBiomeIconSvg(drop.location)}
          <span>${drop.location || "Unknown"}</span>
        </div>
      `;

      row.append(orderBadge, timeBadge, rarityBadge, detail);
      return row;
    }));
  }

  function formatTimeAgo(iso) {
    if (!iso) return "--";
    const date = new Date(iso);
    if (Number.isNaN(date.valueOf())) return "--";
    const diffSec = Math.max(0, Math.floor((Date.now() - date.getTime()) / 1000));
    if (diffSec < 60) return "JUST NOW";
    const mins = Math.floor(diffSec / 60);
    if (mins < 60) return `${mins} MIN`;
    const hours = Math.floor(mins / 60);
    const remMins = mins % 60;
    if (hours < 24) return `${hours}H ${remMins}M`;
    const days = Math.floor(hours / 24);
    const remHours = hours % 24;
    return `${days}D ${remHours}H`;
  }

  // Angels & Demons Update 4 dedicated feed & counters
  function renderAngelsDemons(data) {
    const angelsCount = data.world_telemetry?.["Angels"]?.drops_count || 0;
    const mergedCount = data.world_telemetry?.["Angels & Demons"]?.drops_count || 0;
    const demonsCount = data.world_telemetry?.["Demons"]?.drops_count || 0;

    if ($("ad-angels-count")) $("ad-angels-count").textContent = angelsCount;
    if ($("ad-merged-count")) $("ad-merged-count").textContent = mergedCount;
    if ($("ad-demons-count")) $("ad-demons-count").textContent = demonsCount;

    const feed = $("ad-drop-feed");
    if (!feed) return;

    const drops = Array.isArray(data.recent_drops) ? data.recent_drops : [];
    const adDrops = drops.filter(d => {
      const loc = (d.location || "").toLowerCase();
      const egg = (d.egg || "").toLowerCase();
      return loc.includes("angel") || loc.includes("demon") ||
             egg.includes("jellyfish") || egg.includes("centaur") || egg.includes("pegasus") ||
             egg.includes("archangel") || egg.includes("peacock") || egg.includes("moth") ||
             egg.includes("gargoyle") || egg.includes("razorfang") || egg.includes("skeleton horse") ||
             egg.includes("world burner") || egg.includes("imp") || egg.includes("toro") ||
             egg.includes("equinox") || egg.includes("aetheron");
    }).slice(0, 6);

    feed.replaceChildren(...adDrops.map((drop, idx) => {
      const row = document.createElement("div");
      const isDemon = (drop.location || "").toLowerCase().includes("demon") ||
                      ["gargoyle", "razorfang", "skeleton horse", "world burner", "demon hound", "imp", "flame sprite", "toro"].some(p => (drop.egg || "").toLowerCase().includes(p));
      const locName = isDemon ? "Demons" : "Angels";
      const isNewest = (idx === 0);
      row.className = `ad-drop-row ${isDemon ? 'ad-drop--demon' : 'ad-drop--angel'} ${isNewest ? 'ad-drop--newest' : ''}`;

      const timePill = document.createElement("div");
      timePill.className = "ad-time-pill";
      timePill.innerHTML = `
        <span class="ad-time-hour">${format12hTime(drop.time)}</span>
        <span class="ad-date-val">NY TIME</span>
      `;

      const infoEl = document.createElement("div");
      infoEl.className = "ad-pet-info";
      infoEl.innerHTML = `
        <span class="ad-pet-name">${drop.egg || "Unknown"}</span>
        <span class="ad-pet-world ${isDemon ? 'world-demon' : 'world-angel'}">${locName}</span>
      `;

      const rarity = (drop.rarity || "secret").toLowerCase();
      const rarityEl = document.createElement("span");
      rarityEl.className = `ad-rarity rarity-tag--${rarity}`;
      rarityEl.textContent = rarity.toUpperCase();

      const agoPill = document.createElement("div");
      agoPill.className = `ad-ago-pill ${isNewest ? 'ad-ago--newest' : ''}`;
      agoPill.innerHTML = `
        <span class="ad-ago-lbl">${isNewest ? 'NEWEST' : 'TIME AGO'}</span>
        <span class="ad-ago-val">${formatTimeAgo(drop.time)}</span>
      `;

      row.append(timePill, infoEl, rarityEl, agoPill);
      return row;
    }));
  }

  // Divine Eggs Dedicated HUD
  function renderDivine(data) {
    const divineCount = data.rarity_counts?.divine || 0;
    if ($("divine-found-count")) $("divine-found-count").textContent = divineCount;

    const feed = $("divine-drop-feed");
    if (!feed) return;

    const drops = Array.isArray(data.recent_drops) ? data.recent_drops : [];
    let divineDrops = drops.filter(d => (d.rarity || "").toLowerCase() === "divine");

    // Also check last_seen_snapshot if not enough recent divine drops in feed
    if (divineDrops.length < 5 && data.last_seen_snapshot?.sections?.divine) {
      const snapDivines = data.last_seen_snapshot.sections.divine;
      for (const item of snapDivines) {
        if (!divineDrops.some(d => d.egg === item.name)) {
          divineDrops.push({
            egg: item.name,
            location: item.location || "Active World",
            rarity: "divine",
            time: item.ts ? new Date(item.ts * 1000).toISOString() : null,
          });
        }
      }
    }

    divineDrops = divineDrops.slice(0, 5);

    if (divineDrops.length === 0) {
      feed.innerHTML = '<div class="divine-empty">NO DIVINE DROPS RECORDED YET</div>';
      return;
    }

    feed.replaceChildren(...divineDrops.map((drop, idx) => {
      const row = document.createElement("div");
      const isNewest = (idx === 0);
      row.className = `divine-drop-row ${isNewest ? 'divine-drop--newest' : ''}`;

      const timePill = document.createElement("div");
      timePill.className = `divine-time-pill ${isNewest ? 'divine-time--newest' : ''}`;
      timePill.innerHTML = `
        <span class="divine-type-lbl">${isNewest ? 'NEWEST' : 'DIVINE'}</span>
        <span class="divine-time-val">${format12hTime(drop.time)}</span>
      `;

      const infoEl = document.createElement("div");
      infoEl.className = "divine-pet-info";
      infoEl.innerHTML = `
        ${TINY_EGG_SVG}
        <div class="divine-name-group">
          <span class="divine-pet-name">${drop.egg || "Unknown"}</span>
          <span class="divine-pet-world">${drop.location || "Divine Zone"}</span>
        </div>
      `;

      const agoPill = document.createElement("div");
      agoPill.className = `divine-ago-pill ${isNewest ? 'divine-ago--newest' : ''}`;
      agoPill.innerHTML = `
        <span class="divine-ago-lbl">${isNewest ? 'NEWEST' : 'TIME AGO'}</span>
        <span class="divine-ago-val">${formatTimeAgo(drop.time)}</span>
      `;

      row.append(timePill, infoEl, agoPill);
      return row;
    }));
  }

  function render(data) {
    lastData = data;

    // Row 1: Pastel stats
    if ($("session-drops")) $("session-drops").textContent = data.session_drops ?? 0;

    // Last Egg Time
    const lastTime = data.last_drop_time || data.recent_drops?.[0]?.time || (data.last_drop ? data.last_drop.time : null);
    if ($("last-egg-time")) {
      $("last-egg-time").textContent = lastTime ? format12hTime(lastTime) : "--:--";
    }

    // Since Last Drop
    if ($("since-last-drop")) {
      $("since-last-drop").textContent = formatHms(data.since_last_drop_seconds);
    }

    // Row 2: Rarity & Players
    if ($("secret-count")) $("secret-count").textContent = data.rarity_counts?.secret ?? 0;
    if ($("eternal-count")) $("eternal-count").textContent = data.rarity_counts?.eternal ?? 0;
    if ($("divine-count")) $("divine-count").textContent = data.rarity_counts?.divine ?? 0;

    const players = data.playing_now;
    if ($("player-count")) {
      $("player-count").textContent = Number.isFinite(Number(players)) && Number(players) > 0
        ? Number(players).toLocaleString("en-US")
        : (players === 0 ? "0" : "—");
    }

    // Row 3: Secondary timers
    if ($("since-eternal")) {
      $("since-eternal").textContent = formatHms(data.since_eternal_seconds);
    }
    if ($("since-divine")) {
      $("since-divine").textContent = formatHms(data.since_divine_seconds);
    }

    // Admin Event countdown
    const adminEvent = getNextAdminEvent();
    if ($("admin-countdown")) $("admin-countdown").textContent = adminEvent.countdown;
    if ($("admin-subtext")) $("admin-subtext").textContent = adminEvent.subtext;

    // Left Wave HUD
    updateWave(data.next_wave_estimate?.overall);

    // Left Column Dedicated Panels
    renderAngelsDemons(data);
    renderDivine(data);

    // Live Drop Feed
    renderFeed(Array.isArray(data.recent_drops) ? data.recent_drops : []);

    // Live Clock & Status
    updateRobloxClock();
    setConnection(true, "LIVE DATA · AUTO-REFRESH 2S");
  }

  async function refresh() {
    try {
      const response = await fetch(apiUrl, { cache: "no-store" });
      if (!response.ok) throw new Error(`API returned ${response.status}`);
      render(await response.json());
    } catch (error) {
      console.warn("Egg Radar update failed:", error);
      setConnection(false, "RECONNECTING...");
      updateRobloxClock();
    }
  }

  function tick() {
    updateRobloxClock();
    updateRift();

    const adminEvent = getNextAdminEvent();
    if ($("admin-countdown")) $("admin-countdown").textContent = adminEvent.countdown;
    if ($("admin-subtext")) $("admin-subtext").textContent = adminEvent.subtext;

    if (lastData) {
      ["since_last_drop_seconds", "since_secret_seconds", "since_eternal_seconds", "since_divine_seconds"].forEach((key) => {
        if (typeof lastData[key] === "number") lastData[key] += 1;
      });

      if (typeof lastData.next_wave_estimate?.overall?.eta_seconds === "number") {
        lastData.next_wave_estimate.overall.eta_seconds = Math.max(0, lastData.next_wave_estimate.overall.eta_seconds - 1);
      }

      if ($("since-last-drop")) $("since-last-drop").textContent = formatHms(lastData.since_last_drop_seconds);
      if ($("since-eternal")) $("since-eternal").textContent = formatHms(lastData.since_eternal_seconds);
      if ($("since-divine")) $("since-divine").textContent = formatHms(lastData.since_divine_seconds);

      updateWave(lastData.next_wave_estimate?.overall);
    }
  }

  // Initial load & tick intervals
  updateRobloxClock();
  updateRift();
  const alarmBoxEl = $("alarm-box");
  if (alarmBoxEl) {
    alarmBoxEl.addEventListener("click", toggleAlarm);
  }

  // Also unlock audio on any general click within overlay (useful for OBS interaction)
  document.addEventListener("click", () => initAudio(), { once: true });

  // Auto-fit preview helper for any viewport / OBS resolution
  function handleCanvasScale() {
    const container = $("stream-container");
    if (!container) return;
    if (document.body.classList.contains("panel-mode")) {
      container.style.transform = "none";
      return;
    }
    const w = window.innerWidth;
    const h = window.innerHeight;
    if (w >= 1900 && h >= 1050) {
      container.style.transform = "none";
      return;
    }
    // Proportional scale to fit whatever source resolution OBS or browser provides
    const scale = Math.min(w / 1920, h / 1080);
    container.style.transform = `scale(${scale})`;
    container.style.transformOrigin = "top left";
  }

  window.addEventListener("resize", handleCanvasScale);
  window.addEventListener("DOMContentLoaded", handleCanvasScale);
  handleCanvasScale();

  refresh();
  setInterval(refresh, pollMs);
  setInterval(tick, 1000);
})();


