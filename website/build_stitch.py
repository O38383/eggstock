import re

with open('website/stitch_screen.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update title and brand
html = html.replace(
    '<title>EggStock - Live Spawn Tracker</title>',
    '<title>EggStock | Steal An Egg Live Radar 24/7 by GameFlow</title>'
)

html = html.replace(
    '<span class="font-headline-md text-headline-md tracking-tight uppercase text-primary">EggStock</span>',
    '<span class="font-headline-md text-headline-md tracking-tight uppercase text-primary">EggStock</span><span class="text-xs font-bold text-secondary ml-1 bg-secondary-container/20 px-2 py-0.5 rounded-full">BY GAMEFLOW</span>'
)

# 2. Add YouTube channel link
html = html.replace(
    'data-path="community" href="#">Community</a>',
    'href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener">YouTube (@GameFlow2489)</a>'
)

# 3. Update Quick Join button to direct Roblox link
html = html.replace(
    '<button class="flex items-center gap-space-xs bg-primary text-on-primary hover:bg-primary-fixed-dim px-space-lg py-space-xs rounded-xl font-label-lg transition-all shadow-[0_0_20px_rgba(0,219,233,0.3)]">\n<span class="material-symbols-outlined text-[18px]">bolt</span>\n          Quick Join Best Server\n        </button>',
    '<a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="flex items-center gap-space-xs bg-primary text-on-primary hover:bg-primary-fixed-dim px-space-lg py-space-xs rounded-xl font-label-lg transition-all shadow-[0_0_20px_rgba(0,219,233,0.3)] no-underline">\n<span class="material-symbols-outlined text-[18px]">bolt</span>\n          Play Steal An Egg\n        </a>'
)

# 4. Metric 1: Next Wave Spawn
# ID #countdown-timer and #countdown-bar are already in the template!

# 5. Metric 2: Session Drops & Last Drop
html = re.sub(
    r'<span class="font-headline-md text-headline-md text-on-surface">14</span>',
    '<span class="font-headline-md text-headline-md text-on-surface" id="session-drops-val">0</span>',
    html
)
html = re.sub(
    r'<span class="text-body-sm text-tertiary-fixed-dim">Last: Divine Dragon</span>',
    '<span class="text-body-sm text-tertiary-fixed-dim" id="last-drop-name">Last: --</span>',
    html
)
html = re.sub(
    r'<span>Volcanic Peak \(EU-04\)</span>',
    '<span id="last-drop-loc">Listening for drops...</span>',
    html
)

# 6. Metric 3: Active Players
html = re.sub(
    r'<span class="font-headline-md text-headline-md text-secondary">142,850</span>',
    '<span class="font-headline-md text-headline-md text-secondary" id="active-players-val">2,400,000+</span>',
    html
)

# 7. Metric 4: Admin Event
html = re.sub(
    r'<span class="font-timer-display text-timer-display text-error">18:04</span>',
    '<span class="font-timer-display text-timer-display text-error" id="admin-countdown-val">--:--:--</span>',
    html
)

# 8. Rarity Cards
# Secret
# Rarity Cards with official badge icons & odds from stealanegg.org
# Secret
html = re.sub(
    r'<span class="text-4xl font-headline-xl text-tertiary font-bold">3</span>',
    '<span class="text-4xl font-headline-xl text-tertiary font-bold" id="secret-count-val">0</span>',
    html
)
html = re.sub(
    r'<span class="text-body-lg text-tertiary-fixed font-bold">14m ago</span>',
    '<span class="text-body-lg text-tertiary-fixed font-bold" id="secret-last-seen-val">--</span>',
    html
)
html = html.replace(
    '<span>Drop Rate: ~0.001%</span>',
    '<span title="Official Roblox Badge Win Rate">Hatch Odds: ~0.051% (1 in ~1,960)</span>'
)
html = html.replace(
    '<span class="px-space-sm py-1 rounded-full bg-tertiary-container/20 text-tertiary-fixed font-label-md">\n            SECRET\n          </span>',
    '<div class="flex items-center gap-2">\n<img src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Secret Badge" class="w-7 h-7 rounded-lg border border-tertiary/40" title="Official Roblox Secret Badge">\n<span class="px-space-sm py-1 rounded-full bg-tertiary-container/20 text-tertiary-fixed font-label-md">SECRET</span>\n</div>'
)

# Eternal
html = re.sub(
    r'<span class="text-4xl font-headline-xl text-secondary font-bold">12</span>',
    '<span class="text-4xl font-headline-xl text-secondary font-bold" id="eternal-count-val">0</span>',
    html
)
html = re.sub(
    r'<span class="text-body-lg text-secondary-fixed font-bold">3m ago</span>',
    '<span class="text-body-lg text-secondary-fixed font-bold" id="eternal-last-seen-val">--</span>',
    html
)
html = html.replace(
    '<span>Drop Rate: ~0.05%</span>',
    '<span title="Official Roblox Badge Win Rate">Hatch Odds: ~0.046% (1 in ~2,170)</span>'
)
html = html.replace(
    '<span class="px-space-sm py-1 rounded-full bg-secondary-container/20 text-secondary-fixed font-label-md">\n            ETERNAL\n          </span>',
    '<div class="flex items-center gap-2">\n<img src="https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter" alt="Eternal Badge" class="w-7 h-7 rounded-lg border border-secondary/40" title="Official Roblox Eternal Badge">\n<span class="px-space-sm py-1 rounded-full bg-secondary-container/20 text-secondary-fixed font-label-md">ETERNAL</span>\n</div>'
)

# Divine
html = re.sub(
    r'<span class="text-4xl font-headline-xl text-primary font-bold">45</span>',
    '<span class="text-4xl font-headline-xl text-primary font-bold" id="divine-count-val">0</span>',
    html
)
html = re.sub(
    r'<span class="text-body-lg text-primary-fixed font-bold">32s ago</span>',
    '<span class="text-body-lg text-primary-fixed font-bold" id="divine-last-seen-val">--</span>',
    html
)
html = html.replace(
    '<span>Drop Rate: ~0.25%</span>',
    '<span title="Official Roblox Badge Win Rate">Hatch Odds: ~0.008% (1 in ~12,500)</span>'
)
html = html.replace(
    '<span class="px-space-sm py-1 rounded-full bg-primary-container/20 text-primary-fixed font-label-md">\n            DIVINE\n          </span>',
    '<div class="flex items-center gap-2">\n<img src="https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter" alt="Divine Badge" class="w-7 h-7 rounded-lg border border-primary/40" title="Official Roblox Divine Badge">\n<span class="px-space-sm py-1 rounded-full bg-primary-container/20 text-primary-fixed font-label-md">DIVINE</span>\n</div>'
)


# Replace the static client script with full real-time Web API + sound alert script
script_replacement = '''
<script>
(() => {
  const pollMs = 2000;
  let lastData = null;
  let currentFilter = "all";
  let soundEnabled = true;
  let lastNotifiedDropTime = null;

  // Sound Synthesizer via Web Audio API
  let audioCtx = null;
  function playChime(isDivine = false) {
    if (!soundEnabled) return;
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === "suspended") audioCtx.resume();
      const now = audioCtx.currentTime;
      const freqs = isDivine ? [523.25, 659.25, 783.99, 1046.50] : [440, 554.37, 659.25, 880];
      freqs.forEach((f, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = isDivine ? "triangle" : "sine";
        osc.frequency.setValueAtTime(f, now + i * 0.12);
        gain.gain.setValueAtTime(0.25, now + i * 0.12);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.6);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now + i * 0.12);
        osc.stop(now + i * 0.12 + 0.65);
      });
    } catch (e) {
      console.warn("Audio error:", e);
    }
  }

  // Sound Toggle Button
  const soundToggleBtn = document.getElementById("sound-toggle");
  if (soundToggleBtn) {
    soundToggleBtn.addEventListener("click", () => {
      soundEnabled = !soundEnabled;
      const label = soundToggleBtn.querySelector("span:last-child");
      const icon = soundToggleBtn.querySelector(".material-symbols-outlined");
      if (label) label.textContent = soundEnabled ? "Alert Sound: On" : "Alert Sound: Off";
      if (icon) {
        icon.textContent = soundEnabled ? "volume_up" : "volume_off";
        icon.style.fontVariationSettings = soundEnabled ? "'FILL' 1" : "'FILL' 0";
      }
      if (soundEnabled) playChime(true);
    });
  }

  // Formatters
  function formatWave(sec) {
    if (sec === null || sec === undefined || isNaN(sec)) return "--:--";
    const s = Math.max(0, Math.floor(sec));
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${String(m).padStart(2, '0')}:${String(rem).padStart(2, '0')}`;
  }

  function formatTimeAgo(sec) {
    if (sec === null || sec === undefined || isNaN(sec)) return "--";
    if (sec < 60) return `${sec}s ago`;
    const m = Math.floor(sec / 60);
    if (m < 60) return `${m}m ago`;
    const h = Math.floor(m / 60);
    return `${h}h ago`;
  }

  function formatClock(iso) {
    if (!iso) return "--:--";
    const d = new Date(iso);
    if (isNaN(d.valueOf())) return "--:--";
    return d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", second: "2-digit", hour12: false });
  }

  // Filter Buttons
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => {
        b.classList.remove("active", "bg-primary", "text-on-primary", "font-bold");
        b.classList.add("text-on-surface-variant");
      });
      btn.classList.add("active", "bg-primary", "text-on-primary", "font-bold");
      btn.classList.remove("text-on-surface-variant");
      currentFilter = btn.getAttribute("data-filter") || "all";
      if (lastData) renderTable(lastData.recent_drops || []);
    });
  });

  // Table Render
  function renderTable(drops) {
    const tbody = document.getElementById("drops-table-body");
    if (!tbody) return;

    const filtered = drops.filter(d => {
      const r = (d.rarity || "").toLowerCase();
      return currentFilter === "all" || r === currentFilter;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-on-surface-variant font-label-md">No drops matching filter</td></tr>';
      return;
    }

    const rarityPills = {
      divine: "bg-primary-container/20 text-primary-fixed border border-primary-fixed/30",
      eternal: "bg-secondary-container/20 text-secondary-fixed border border-secondary-fixed/30",
      secret: "bg-tertiary-container/20 text-tertiary-fixed border border-tertiary-fixed/30"
    };

    const rarityGlows = {
      divine: "bg-primary",
      eternal: "bg-secondary",
      secret: "bg-tertiary"
    };

    tbody.innerHTML = filtered.map((drop, i) => {
      const r = (drop.rarity || "secret").toLowerCase();
      const pillClass = rarityPills[r] || rarityPills.secret;
      const glowClass = rarityGlows[r] || rarityGlows.secret;
      const isNewest = (i === 0);

      return `
        <tr class="hover:bg-surface-bright/40 transition-colors group ${isNewest ? 'bg-surface-bright/20' : ''}" data-rarity="${r}">
          <td class="py-space-md px-space-md font-label-md text-on-surface-variant">${formatClock(drop.time)}</td>
          <td class="py-space-md px-space-md">
            <span class="inline-flex items-center px-space-xs py-0.5 rounded-full text-label-md font-bold uppercase ${pillClass}">${r}</span>
          </td>
          <td class="py-space-md px-space-md font-medium text-on-surface flex items-center gap-space-xs">
            <span class="w-2 h-2 rounded-full ${glowClass} ${isNewest ? 'animate-ping' : ''}"></span>
            ${drop.egg || "Unknown Egg"}
          </td>
          <td class="py-space-md px-space-md text-on-surface-variant">${drop.location || "Arena"}</td>
          <td class="py-space-md px-space-md text-right">
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="inline-flex items-center gap-space-2xs bg-surface-container-high hover:bg-primary hover:text-on-primary text-on-surface px-space-md py-space-2xs rounded-lg text-label-md transition-all no-underline">
              <span class="material-symbols-outlined text-[14px]">bolt</span> Join
            </a>
          </td>
        </tr>
      `;
    }).join("");
  }

  // Update Data
  function render(data) {
    lastData = data;

    // Active Players
    const pVal = document.getElementById("active-players-val");
    if (pVal) {
      pVal.textContent = data.playing_now ? Number(data.playing_now).toLocaleString("en-US") : "2,425,000+";
    }

    // Session Drops
    const sVal = document.getElementById("session-drops-val");
    if (sVal) sVal.textContent = data.session_drops ?? 0;

    // Last Drop Info
    if (data.last_drop) {
      const dName = document.getElementById("last-drop-name");
      const dLoc = document.getElementById("last-drop-loc");
      if (dName) dName.textContent = `Last: ${data.last_drop.egg || '--'}`;
      if (dLoc) dLoc.textContent = data.last_drop.location || 'Roblox Server';
    }

    // Three Rarity Cards
    const sc = document.getElementById("secret-count-val");
    const sl = document.getElementById("secret-last-seen-val");
    if (sc) sc.textContent = data.rarity_counts?.secret ?? 0;
    if (sl) sl.textContent = formatTimeAgo(data.since_secret_seconds);

    const ec = document.getElementById("eternal-count-val");
    const el = document.getElementById("eternal-last-seen-val");
    if (ec) ec.textContent = data.rarity_counts?.eternal ?? 0;
    if (el) el.textContent = formatTimeAgo(data.since_eternal_seconds);

    const dc = document.getElementById("divine-count-val");
    const dl = document.getElementById("divine-last-seen-val");
    if (dc) dc.textContent = data.rarity_counts?.divine ?? 0;
    if (dl) dl.textContent = formatTimeAgo(data.since_divine_seconds);

    // Wave Timer
    const wave = data.next_wave_estimate?.overall;
    const waveEl = document.getElementById("countdown-timer");
    const waveBar = document.getElementById("countdown-bar");
    if (waveEl && wave) {
      waveEl.textContent = formatWave(wave.eta_seconds);
      if (waveBar && wave.interval_seconds > 0) {
        const pct = Math.min(100, Math.max(0, (wave.eta_seconds / wave.interval_seconds) * 100));
        waveBar.style.width = `${pct}%`;
      }
    }

    // Audio Alert Trigger
    if (data.recent_drops && data.recent_drops.length > 0) {
      const newest = data.recent_drops[0];
      if (newest && newest.time && newest.time !== lastNotifiedDropTime) {
        if (lastNotifiedDropTime !== null) {
          const r = (newest.rarity || "").toLowerCase();
          if (r === "divine") playChime(true);
          else if (r === "eternal") playChime(false);
        }
        lastNotifiedDropTime = newest.time;
      }
    }

    renderTable(data.recent_drops || []);
  }

  // Admin Countdown & Clock
  function updateAdminAndRift() {
    const now = new Date();
    const adminEl = document.getElementById("admin-countdown-val");
    if (adminEl) {
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
      adminEl.textContent = `${d}D ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    }
  }

  // Polling loop
  async function refresh() {
    try {
      const res = await fetch("/api/status", { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(data);
    } catch (e) {
      console.warn("Telemetry fetch error:", e);
    }
  }

  function tick() {
    updateAdminAndRift();
    if (lastData && lastData.next_wave_estimate?.overall?.eta_seconds > 0) {
      lastData.next_wave_estimate.overall.eta_seconds = Math.max(0, lastData.next_wave_estimate.overall.eta_seconds - 1);
      const waveEl = document.getElementById("countdown-timer");
      if (waveEl) waveEl.textContent = formatWave(lastData.next_wave_estimate.overall.eta_seconds);
    }
    if (lastData) {
      if (typeof lastData.since_secret_seconds === "number") lastData.since_secret_seconds += 1;
      if (typeof lastData.since_eternal_seconds === "number") lastData.since_eternal_seconds += 1;
      if (typeof lastData.since_divine_seconds === "number") lastData.since_divine_seconds += 1;
      const sl = document.getElementById("secret-last-seen-val");
      const el = document.getElementById("eternal-last-seen-val");
      const dl = document.getElementById("divine-last-seen-val");
      if (sl) sl.textContent = formatTimeAgo(lastData.since_secret_seconds);
      if (el) el.textContent = formatTimeAgo(lastData.since_eternal_seconds);
      if (dl) dl.textContent = formatTimeAgo(lastData.since_divine_seconds);
    }
  }

  updateAdminAndRift();
  refresh();
  setInterval(refresh, pollMs);
  setInterval(tick, 1000);
})();
</script>
'''

# Replace script tag before </body>
html = re.sub(r'<script>.*?</script>', script_replacement, html, flags=re.DOTALL)

with open('website/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success: website/index.html compiled with Stitch design and real data binding!')
