(() => {
  const pollMs = 2000;
  let lastData = null;
  let currentFilter = "all";
  let currentSearch = "";
  let soundEnabled = localStorage.getItem("egg_sound_alerts") === "true";
  let lastNotifiedDropTime = null;

  const $ = (id) => document.getElementById(id);

  // ---------- Web Audio API Synthesizer for Alerts ----------
  let audioCtx = null;
  function playAlertSound(isDivine = false) {
    if (!soundEnabled) return;
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === "suspended") {
        audioCtx.resume();
      }

      const now = audioCtx.currentTime;
      // Frequency chords: Golden chord for Divine, cosmic chord for Eternal
      const notes = isDivine ? [523.25, 659.25, 783.99, 1046.50] : [440, 554.37, 659.25, 880];

      notes.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = isDivine ? "triangle" : "sine";
        osc.frequency.setValueAtTime(freq, now + idx * 0.12);

        gain.gain.setValueAtTime(0.3, now + idx * 0.12);
        gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.12 + 0.6);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start(now + idx * 0.12);
        osc.stop(now + idx * 0.12 + 0.65);
      });
    } catch (e) {
      console.warn("Audio play blocked or unavailable:", e);
    }
  }

  // Sound Toggle button
  const soundBtn = $("btn-sound");
  const soundText = $("sound-text");
  const soundIcon = $("sound-icon");

  function updateSoundUI() {
    if (soundBtn) {
      if (soundEnabled) {
        soundBtn.classList.add("sound-active");
        if (soundText) soundText.textContent = "ALERTS: ON 🔔";
      } else {
        soundBtn.classList.remove("sound-active");
        if (soundText) soundText.textContent = "ALERTS: OFF 🔕";
      }
    }
  }
  updateSoundUI();

  if (soundBtn) {
    soundBtn.addEventListener("click", () => {
      soundEnabled = !soundEnabled;
      localStorage.setItem("egg_sound_alerts", soundEnabled ? "true" : "false");
      updateSoundUI();
      if (soundEnabled) {
        playAlertSound(true); // Play preview sound so user knows it's active!
      }
    });
  }

  // ---------- Wave & Duration Formatters ----------
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

  function formatHms(value) {
    if (value === null || value === undefined || Number.isNaN(Number(value))) return "--:--:--";
    let seconds = Math.max(0, Math.floor(Number(value)));
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return [hours, minutes, secs].map((u) => u.toString().padStart(2, "0")).join(":");
  }

  function format12hTime(iso) {
    if (!iso) return "--:--";
    const date = new Date(iso);
    if (Number.isNaN(date.valueOf())) return "--:--";
    return date.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", hour12: true });
  }

  // ---------- Live Clocks ----------
  function updateClocks() {
    const now = new Date();
    // Roblox New York (EST) Time
    if ($("roblox-ny-clock")) {
      $("roblox-ny-clock").textContent = now.toLocaleTimeString("en-US", {
        timeZone: "America/New_York",
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
        hour12: true
      });
    }

    // Admin Event Countdown
    const target = new Date(now);
    const daysUntilSaturday = (6 - now.getUTCDay() + 7) % 7;
    target.setUTCDate(now.getUTCDate() + daysUntilSaturday);
    target.setUTCHours(15, 0, 0, 0);
    if (target <= now) target.setUTCDate(target.getUTCDate() + 7);

    const diff = Math.max(0, Math.floor((target - now) / 1000));
    const d = Math.floor(diff / 86400);
    const h = Math.floor((diff % 86400) / 3600);
    const m = Math.floor((diff % 3600) / 60);
    const s = diff % 60;
    if ($("admin-countdown")) {
      $("admin-countdown").textContent = `${d}D ${h.toString().padStart(2,"0")}:${m.toString().padStart(2,"0")}:${s.toString().padStart(2,"0")}`;
    }

    // Rift Boss Timer
    updateRift();
  }

  function updateRift() {
    const now = new Date();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const secsIntoSlot = (minutes % 30) * 60 + seconds;
    const RIFT_OPEN_DURATION = 120;
    const SLOT_SECONDS = 1800;

    const riftEl = $("rift-time");
    const riftDetail = $("rift-detail");
    const riftAt = $("rift-opens-at");

    if (secsIntoSlot < RIFT_OPEN_DURATION) {
      if (riftEl) riftEl.textContent = "OPEN NOW!";
      if (riftDetail) riftDetail.textContent = "⚡ RIFT PORTAL IS OPEN — DEFEAT THE OVERLORD!";
      if (riftAt) riftAt.textContent = `CLOSES IN ${RIFT_OPEN_DURATION - secsIntoSlot}s`;
    } else {
      const secsUntil = SLOT_SECONDS - secsIntoSlot;
      const mm = Math.floor(secsUntil / 60);
      const ss = secsUntil % 60;
      if (riftEl) riftEl.textContent = `${mm.toString().padStart(2,"0")}:${ss.toString().padStart(2,"0")}`;
      if (riftDetail) riftDetail.textContent = "EVERY 30 MIN · SERVER-WIDE";

      if (riftAt) {
        const nextOpen = new Date(now.getTime() + secsUntil * 1000);
        const atStr = nextOpen.toLocaleTimeString("en-US", {
          hour: "numeric", minute: "2-digit", hour12: true, timeZone: "America/New_York"
        });
        riftAt.textContent = `OPENS AT ${atStr} EST`;
      }
    }
  }

  // ---------- Render Drops Feed ----------
  function renderFeed(drops) {
    const feed = $("web-drop-feed");
    if (!feed) return;

    if (!Array.isArray(drops) || drops.length === 0) {
      feed.innerHTML = '<div class="feed-loading">LISTENING FOR LIVE EGG DROPS...</div>';
      return;
    }

    // Filter drops
    const filtered = drops.filter((drop) => {
      const rarity = (drop.rarity || "").toLowerCase();
      if (currentFilter !== "all" && rarity !== currentFilter) return false;

      if (currentSearch.trim() !== "") {
        const q = currentSearch.toLowerCase();
        const eggName = (drop.egg || "").toLowerCase();
        const loc = (drop.location || "").toLowerCase();
        if (!eggName.includes(q) && !loc.includes(q)) return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      feed.innerHTML = '<div class="feed-loading">NO DROPS MATCH CURRENT FILTER</div>';
      return;
    }

    feed.replaceChildren(...filtered.map((drop, idx) => {
      const isNewest = (idx === 0);
      const row = document.createElement("div");
      row.className = `web-drop-row ${isNewest ? "row--newest" : ""}`;

      const rarity = (drop.rarity || "secret").toLowerCase();

      row.innerHTML = `
        <div><span class="badge-tag ${isNewest ? "tag-newest" : "tag-past"}">${isNewest ? "NEWEST" : "PAST"}</span></div>
        <div class="time-col">${format12hTime(drop.time)}</div>
        <div><span class="badge-rarity rarity--${rarity}">${rarity.toUpperCase()}</span></div>
        <div class="egg-col">🥚 <span>${drop.egg || "Unknown"}</span></div>
        <div class="biome-col">📍 ${drop.location || "Unknown"}</div>
      `;
      return row;
    }));
  }

  // ---------- Render Full State ----------
  function render(data) {
    lastData = data;

    // Player Count
    const players = data.playing_now;
    if ($("player-count")) {
      $("player-count").textContent = Number.isFinite(Number(players)) && Number(players) > 0
        ? Number(players).toLocaleString("en-US")
        : (players === 0 ? "0" : "2,400,000+");
    }

    // Counters
    if ($("count-divine")) $("count-divine").textContent = data.rarity_counts?.divine ?? 0;
    if ($("count-eternal")) $("count-eternal").textContent = data.rarity_counts?.eternal ?? 0;
    if ($("count-secret")) $("count-secret").textContent = data.rarity_counts?.secret ?? 0;
    if ($("count-total")) $("count-total").textContent = data.session_drops ?? 0;

    // Secondary Timers
    if ($("since-divine")) $("since-divine").textContent = formatHms(data.since_divine_seconds);
    if ($("since-eternal")) $("since-eternal").textContent = formatHms(data.since_eternal_seconds);
    if ($("since-last-drop")) $("since-last-drop").textContent = formatHms(data.since_last_drop_seconds);

    // Wave HUD
    const wave = data.next_wave_estimate?.overall;
    if ($("wave-time")) $("wave-time").textContent = formatWaveTimer(wave?.eta_seconds);
    if ($("wave-detail")) {
      $("wave-detail").textContent = wave?.interval_seconds
        ? `MEDIAN GAP: ${formatWaveTimer(wave.interval_seconds)}`
        : "CALIBRATING FROM LIVE DROPS";
    }
    if ($("wave-samples")) $("wave-samples").textContent = `${wave?.sample_size || 0} SAMPLES`;
    if ($("confidence-fill")) {
      const widths = { none: "8%", low: "32%", medium: "66%", good: "100%" };
      $("confidence-fill").style.width = widths[wave?.confidence] || "8%";
    }

    // Audio Alert Trigger
    if (data.recent_drops && data.recent_drops.length > 0) {
      const newest = data.recent_drops[0];
      if (newest && newest.time && newest.time !== lastNotifiedDropTime) {
        if (lastNotifiedDropTime !== null) { // don't sound on first boot
          const r = (newest.rarity || "").toLowerCase();
          if (r === "divine") {
            playAlertSound(true);
          } else if (r === "eternal") {
            playAlertSound(false);
          }
        }
        lastNotifiedDropTime = newest.time;
      }
    }

    // Feed
    renderFeed(data.recent_drops || []);
  }

  // ---------- Filter & Search Listeners ----------
  const filterGroup = $("filter-rarity-group");
  if (filterGroup) {
    filterGroup.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;
      filterGroup.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter") || "all";
      if (lastData) renderFeed(lastData.recent_drops || []);
    });
  }

  const searchInput = $("filter-search");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      currentSearch = e.target.value || "";
      if (lastData) renderFeed(lastData.recent_drops || []);
    });
  }

  // ---------- Polling & Ticks ----------
  async function refresh() {
    try {
      const res = await fetch("/api/status", { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(data);
      if ($("footer-status-dot")) $("footer-status-dot").style.background = "#22c55e";
      if ($("footer-status-text")) $("footer-status-text").textContent = "CONNECTED TO LIVE STOCK RADAR";
    } catch (e) {
      if ($("footer-status-dot")) $("footer-status-dot").style.background = "#ef4444";
      if ($("footer-status-text")) $("footer-status-text").textContent = "RECONNECTING TO SERVER...";
    }
  }

  function tick() {
    updateClocks();
    if (lastData) {
      ["since_last_drop_seconds", "since_secret_seconds", "since_eternal_seconds", "since_divine_seconds"].forEach((k) => {
        if (typeof lastData[k] === "number") lastData[k] += 1;
      });
      if (typeof lastData.next_wave_estimate?.overall?.eta_seconds === "number") {
        lastData.next_wave_estimate.overall.eta_seconds = Math.max(0, lastData.next_wave_estimate.overall.eta_seconds - 1);
        if ($("wave-time")) $("wave-time").textContent = formatWaveTimer(lastData.next_wave_estimate.overall.eta_seconds);
      }
      if ($("since-divine")) $("since-divine").textContent = formatHms(lastData.since_divine_seconds);
      if ($("since-eternal")) $("since-eternal").textContent = formatHms(lastData.since_eternal_seconds);
      if ($("since-last-drop")) $("since-last-drop").textContent = formatHms(lastData.since_last_drop_seconds);
    }
  }

  // Start
  updateClocks();
  refresh();
  setInterval(refresh, pollMs);
  setInterval(tick, 1000);
})();
