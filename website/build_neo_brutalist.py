import re

with open('website/stitch_neo_brutalist.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace title & insert AdSense snippet
adsense_tag = '''<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3496166469031307"
     crossorigin="anonymous"></script>'''
html = re.sub(r'<title>.*?</title>', f'<title>EggStock | Steal An Egg Live Radar 24/7 by GameFlow</title>\\n{adsense_tag}', html)

# Brand in nav
html = html.replace(
    '<span class="font-headline-md text-headline-md font-bold tracking-tighter text-primary">EggStock Pulse</span>',
    '''<div class="flex items-center gap-2">
        <span class="font-headline-md text-headline-md font-bold tracking-tighter text-primary">EggStock</span>
        <span class="bg-[#fbff00] text-black text-[11px] font-black px-2 py-0.5 uppercase tracking-wider border border-black shadow-[2px_2px_0px_#000]">By GameFlow</span>
    </div>'''
)

# Nav links
html = html.replace(
    '''<div class="hidden md:flex gap-space-lg items-center">
<a class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors hover:bg-surface-bright/20 p-2 rounded" href="#">Market</a>
<a class="font-label-lg text-label-lg text-primary border-b-2 border-primary pb-1 active:scale-95 transition-transform p-2" href="#">Telemetry</a>
<a class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors hover:bg-surface-bright/20 p-2 rounded" href="#">Portfolio</a>
<a class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors hover:bg-surface-bright/20 p-2 rounded" href="#">Vault</a>
</div>''',
    '''<div class="hidden md:flex gap-space-md items-center">
        <a class="font-label-lg text-label-lg text-primary border-b-2 border-primary pb-1 font-bold p-2 flex items-center gap-1.5" href="#radar">
            <span class="material-symbols-outlined text-[18px]">radar</span>Live Radar
        </a>
        <a class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors hover:bg-surface-bright/20 p-2 rounded flex items-center gap-1.5" href="#rarity">
            <span class="material-symbols-outlined text-[18px]">workspace_premium</span>Rarity Odds
        </a>
        <a class="font-label-lg text-label-lg text-on-surface-variant hover:text-on-surface transition-colors hover:bg-surface-bright/20 p-2 rounded flex items-center gap-1.5" href="#drops">
            <span class="material-symbols-outlined text-[18px]">history</span>Drop History
        </a>
        <a class="font-label-lg text-label-lg text-on-surface-variant hover:text-[#ff0000] transition-colors hover:bg-surface-bright/20 p-2 rounded flex items-center gap-1.5" href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener">
            <span class="material-symbols-outlined text-[18px]">smart_display</span>YouTube
        </a>
    </div>'''
)

# Connect HUD button -> Play Steal An Egg
html = html.replace(
    '''<button class="bg-[#00f0ff] text-background font-label-lg text-label-lg px-4 py-2 neo-brutal-border neo-brutal-btn uppercase font-bold hidden sm:block">
                    Connect HUD
                </button>''',
    '''<div class="flex items-center gap-3">
        <button id="sound-toggle" class="bg-surface-container-high hover:bg-surface-bright text-on-surface px-3 py-2 border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-1 text-xs font-bold uppercase transition-all active:translate-x-0.5 active:translate-y-0.5">
            <span class="material-symbols-outlined text-[18px] text-primary" style="font-variation-settings: 'FILL' 1;">volume_up</span>
            <span>Alerts: On</span>
        </button>
        <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-[#7df4ff] text-black font-label-lg text-label-lg px-4 py-2 border-2 border-black shadow-[4px_4px_0px_#000] uppercase font-black transition-all active:translate-x-1 active:translate-y-1 flex items-center gap-1 no-underline">
            <span>Play Roblox</span>
            <span class="material-symbols-outlined text-[18px]">open_in_new</span>
        </a>
    </div>'''
)

# Stat chips with dynamic IDs
html = html.replace(
    '''<div class="flex flex-wrap gap-space-sm mt-space-md">
<div class="bg-[#fbff00] text-background px-3 py-1 font-label-md text-label-md uppercase font-bold neo-brutal-border">1.5M Playing</div>
<div class="bg-surface-container-high text-on-surface px-3 py-1 font-label-md text-label-md uppercase neo-brutal-border">Next Wave in 08:42</div>
<div class="bg-surface-container-high text-on-surface px-3 py-1 font-label-md text-label-md uppercase neo-brutal-border">2B+ Visits</div>
<div class="bg-[#ff00ff] text-background px-3 py-1 font-label-md text-label-md uppercase font-bold neo-brutal-border flex items-center gap-2">
<span class="w-2 h-2 bg-background rounded-full animate-pulse"></span>
                        Live Radar: ACTIVE
                    </div>
</div>''',
    '''<div class="flex flex-wrap gap-space-sm mt-space-md">
        <div class="bg-[#fbff00] text-black px-3.5 py-1.5 font-label-md uppercase font-black border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">groups</span>
            <span id="active-players-val">1,455,401</span> Playing
        </div>
        <div class="bg-[#00f0ff] text-black px-3.5 py-1.5 font-label-md uppercase font-black border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">timer</span>
            Next Wave: <span id="countdown-timer" class="font-timer-display font-bold">08:42</span>
        </div>
        <div class="bg-surface-container-high text-on-surface px-3.5 py-1.5 font-label-md uppercase font-bold border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">local_fire_department</span>
            2B+ Visits
        </div>
        <div class="bg-[#ff00ff] text-black px-3.5 py-1.5 font-label-md uppercase font-black border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-1.5">
            <span class="w-2 h-2 bg-black rounded-full animate-ping"></span>
            LIVE RADAR 24/7
        </div>
    </div>
    <!-- Quick action links -->
    <div class="flex items-center gap-4 mt-space-md">
        <a href="#drops" class="bg-white text-black font-bold uppercase text-xs px-4 py-2 border-2 border-black shadow-[3px_3px_0px_#000] hover:bg-[#dbfcff] transition-all flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">travel_explore</span>
            View Drop Feed
        </a>
        <a href="https://stealanegg.org" target="_blank" rel="noopener" class="text-on-surface-variant hover:text-white text-xs font-mono underline flex items-center gap-1">
            <span>Documentation via stealanegg.org</span>
            <span class="material-symbols-outlined text-[14px]">open_in_new</span>
        </a>
    </div>'''
)

# Marquee ticker content
html = html.replace(
    'LIVE TELEMETRY ACTIVE • NEW DIVINE DROP DETECTED • NEXT WAVE IN 08:12 • JOIN SERVER [EU-04] • LIVE TELEMETRY ACTIVE • NEW DIVINE DROP DETECTED • NEXT WAVE IN 08:12 • JOIN SERVER [EU-04] •',
    '⚡ LIVE RADAR ACTIVE ⬡ OVER 1.45M PLAYERS TRACKED ⬡ PREDICTED WAVE COUNTDOWN SYNCED ⬡ SECRET ODDS 0.051% ⬡ ETERNAL ODDS 0.046% ⬡ DIVINE ODDS 0.008% ⬡ VERIFIED ROBLOX BADGE TELEMETRY ⬡ POWERED BY GAMEFLOW (@GameFlow2489) ⬡ HATCH SMART STEAL SMARTER ⬡ ⚡ LIVE RADAR ACTIVE ⬡ OVER 1.45M PLAYERS TRACKED ⬡ PREDICTED WAVE COUNTDOWN SYNCED ⬡ SECRET ODDS 0.051% ⬡ ETERNAL ODDS 0.046% ⬡ DIVINE ODDS 0.008% ⬡'
)

# Wave timer bar + Session Drops bar section before rarity
metrics_bar = '''
<!-- Live Analytics Grid -->
<section id="radar" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md mb-space-2xl">
    <!-- Wave Countdown Card -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[4px_4px_0px_#000] relative overflow-hidden">
        <div class="flex items-center justify-between">
            <span class="text-xs uppercase font-mono tracking-widest text-on-surface-variant">Wave Prediction</span>
            <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-pulse"></span>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
            <span class="font-timer-display text-3xl font-black text-[#00f0ff]" id="countdown-timer-sub">--:--</span>
            <span class="text-xs font-bold text-secondary uppercase animate-pulse">● Imminent</span>
        </div>
        <div class="mt-3 w-full bg-black h-2 border border-black/40 overflow-hidden">
            <div class="bg-[#00f0ff] h-full w-3/4 transition-all duration-1000" id="countdown-bar"></div>
        </div>
        <span class="mt-2 text-[11px] text-on-surface-variant block">Syncing across 120+ active servers</span>
    </div>

    <!-- Session Drops -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[4px_4px_0px_#000] relative overflow-hidden">
        <div class="flex items-center justify-between">
            <span class="text-xs uppercase font-mono tracking-widest text-on-surface-variant">Session Drops</span>
            <span class="material-symbols-outlined text-[#ff00ff] text-[20px]">package_2</span>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-white" id="session-drops-val">0</span>
            <span class="text-xs text-[#fbabff] font-bold" id="last-drop-name">Last: --</span>
        </div>
        <div class="mt-3 flex items-center gap-1 text-xs text-on-surface-variant">
            <span class="material-symbols-outlined text-[14px] text-primary">location_on</span>
            <span id="last-drop-loc" class="truncate">Listening for spawns...</span>
        </div>
    </div>

    <!-- Active Players -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[4px_4px_0px_#000] relative overflow-hidden">
        <div class="flex items-center justify-between">
            <span class="text-xs uppercase font-mono tracking-widest text-on-surface-variant">Active Roblox Players</span>
            <span class="material-symbols-outlined text-[#4edea3] text-[20px]">groups</span>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-black text-[#4edea3]" id="active-players-val-sub">1,455,401</span>
            <span class="text-xs text-[#4edea3] font-bold">● High Traffic</span>
        </div>
        <span class="mt-3 text-[11px] text-on-surface-variant block">Steal An Egg Universe ID 10563114921</span>
    </div>

    <!-- Admin Luck Event -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[4px_4px_0px_#000] relative overflow-hidden">
        <div class="flex items-center justify-between">
            <span class="text-xs uppercase font-mono tracking-widest text-on-surface-variant">Admin Double Luck</span>
            <span class="material-symbols-outlined text-[#ffb4ab] text-[20px]">bolt</span>
        </div>
        <div class="mt-2 flex items-baseline gap-2">
            <span class="font-timer-display text-3xl font-black text-[#ffb4ab]" id="admin-countdown-val">--:--:--</span>
            <span class="text-xs text-on-surface-variant uppercase font-bold">2x Boost</span>
        </div>
        <span class="mt-3 text-[11px] text-on-surface-variant block">Double luck drop multiplier</span>
    </div>
</section>
'''

html = html.replace('<!-- Rarity Telemetry -->', metrics_bar + '\n<!-- Rarity Telemetry -->')

# Replace Rarity Telemetry Cards with official badge icons & odds
rarity_section = '''<!-- Rarity Telemetry Section -->
<div id="rarity" class="flex flex-col md:flex-row items-start md:items-end justify-between mb-space-md gap-2">
    <div>
        <span class="text-xs font-black uppercase tracking-widest bg-[#fbff00] text-black px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">Verified Telemetry</span>
        <h2 class="font-headline-lg text-headline-lg font-black uppercase text-white mt-1">Roblox Badge Rarity Odds</h2>
    </div>
    <p class="text-xs text-on-surface-variant font-mono max-w-md">
        Calculated from official Roblox badge completions documented on <a href="https://stealanegg.org" target="_blank" rel="noopener" class="text-primary underline">stealanegg.org</a>.
    </p>
</div>
<section class="grid grid-cols-1 md:grid-cols-3 gap-space-lg mb-space-2xl">
    <!-- Secret Card -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[5px_5px_0px_#000] relative overflow-hidden group hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[7px_7px_0px_#000] transition-all">
        <div class="flex items-start justify-between">
            <div>
                <span class="text-[11px] font-mono text-[#fbabff] uppercase font-bold tracking-wider">Mythic Tier</span>
                <div class="font-headline-md text-2xl font-black text-[#fbabff] mt-0.5">Secret Rarity</div>
            </div>
            <img src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Secret Badge" class="w-10 h-10 rounded border-2 border-black shadow-[2px_2px_0px_#000]" title="Roblox Badge 383815774941459">
        </div>
        <div class="mt-4 flex items-baseline justify-between">
            <div>
                <span class="text-3xl font-black text-white" id="secret-count-val">0</span>
                <span class="text-xs text-on-surface-variant ml-1 font-mono">spawned</span>
            </div>
            <div class="text-right">
                <span class="text-[10px] uppercase font-mono text-on-surface-variant block">Last Drop</span>
                <span class="text-sm font-bold text-[#fbabff]" id="secret-last-seen-val">--</span>
            </div>
        </div>
        <div class="mt-4 pt-3 border-t border-black/30 flex items-center justify-between text-xs font-mono">
            <span class="text-white font-bold bg-[#ff00ff]/20 px-2 py-0.5 border border-[#ff00ff]/50">Odds: 0.051% (1 in ~1,960)</span>
            <span class="text-on-surface-variant text-[11px]">31.2M+ completions</span>
        </div>
    </div>

    <!-- Eternal Card -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[5px_5px_0px_#000] relative overflow-hidden group hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[7px_7px_0px_#000] transition-all">
        <div class="flex items-start justify-between">
            <div>
                <span class="text-[11px] font-mono text-[#4edea3] uppercase font-bold tracking-wider">Legendary Tier</span>
                <div class="font-headline-md text-2xl font-black text-[#4edea3] mt-0.5">Eternal Rarity</div>
            </div>
            <img src="https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter" alt="Eternal Badge" class="w-10 h-10 rounded border-2 border-black shadow-[2px_2px_0px_#000]" title="Roblox Badge 4448343437950888">
        </div>
        <div class="mt-4 flex items-baseline justify-between">
            <div>
                <span class="text-3xl font-black text-white" id="eternal-count-val">0</span>
                <span class="text-xs text-on-surface-variant ml-1 font-mono">spawned</span>
            </div>
            <div class="text-right">
                <span class="text-[10px] uppercase font-mono text-on-surface-variant block">Last Drop</span>
                <span class="text-sm font-bold text-[#4edea3]" id="eternal-last-seen-val">--</span>
            </div>
        </div>
        <div class="mt-4 pt-3 border-t border-black/30 flex items-center justify-between text-xs font-mono">
            <span class="text-white font-bold bg-[#4edea3]/20 px-2 py-0.5 border border-[#4edea3]/50">Odds: 0.046% (1 in ~2,170)</span>
            <span class="text-on-surface-variant text-[11px]">19.8M+ completions</span>
        </div>
    </div>

    <!-- Divine Card -->
    <div class="bg-surface-container p-space-md border-2 border-black shadow-[5px_5px_0px_#000] relative overflow-hidden group hover:translate-x-[-2px] hover:translate-y-[-2px] hover:shadow-[7px_7px_0px_#000] transition-all">
        <div class="flex items-start justify-between">
            <div>
                <span class="text-[11px] font-mono text-[#00f0ff] uppercase font-bold tracking-wider">Celestial Tier</span>
                <div class="font-headline-md text-2xl font-black text-[#00f0ff] mt-0.5">Divine Rarity</div>
            </div>
            <img src="https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter" alt="Divine Badge" class="w-10 h-10 rounded border-2 border-black shadow-[2px_2px_0px_#000]" title="Roblox Badge 1521646775064072">
        </div>
        <div class="mt-4 flex items-baseline justify-between">
            <div>
                <span class="text-3xl font-black text-white" id="divine-count-val">0</span>
                <span class="text-xs text-on-surface-variant ml-1 font-mono">spawned</span>
            </div>
            <div class="text-right">
                <span class="text-[10px] uppercase font-mono text-on-surface-variant block">Last Drop</span>
                <span class="text-sm font-bold text-[#00f0ff]" id="divine-last-seen-val">--</span>
            </div>
        </div>
        <div class="mt-4 pt-3 border-t border-black/30 flex items-center justify-between text-xs font-mono">
            <span class="text-white font-bold bg-[#00f0ff]/20 px-2 py-0.5 border border-[#00f0ff]/50">Odds: 0.008% (1 in ~12,500)</span>
            <span class="text-on-surface-variant text-[11px]">1.69M+ completions</span>
        </div>
    </div>
</section>
'''

html = re.sub(r'<!-- Rarity Telemetry -->.*?<!-- Live Drops Table -->', rarity_section + '\n<!-- Live Drops Table -->', html, flags=re.DOTALL)

# Table Section: Add filter buttons and real data table
table_section = '''<!-- Live Drops Table Section -->
<div id="drops" class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-space-md">
    <div>
        <h3 class="font-headline-lg text-2xl font-black uppercase text-white">Live Spawn Feed</h3>
        <p class="text-xs text-on-surface-variant font-mono">Real-time drops captured across public and VIP servers</p>
    </div>
    <!-- Tactile Filter Tabs -->
    <div class="flex items-center gap-1.5 bg-black p-1 border-2 border-black shadow-[3px_3px_0px_#000]">
        <button class="filter-btn active bg-[#00f0ff] text-black font-black uppercase text-xs px-3 py-1 border border-black" data-filter="all">All</button>
        <button class="filter-btn text-on-surface-variant hover:text-white font-bold uppercase text-xs px-3 py-1" data-filter="secret">Secret</button>
        <button class="filter-btn text-on-surface-variant hover:text-white font-bold uppercase text-xs px-3 py-1" data-filter="eternal">Eternal</button>
        <button class="filter-btn text-on-surface-variant hover:text-white font-bold uppercase text-xs px-3 py-1" data-filter="divine">Divine</button>
    </div>
</div>
<section class="bg-surface-container border-2 border-black shadow-[6px_6px_0px_#000] overflow-x-auto mb-space-2xl">
<table class="w-full text-left font-body-md">
<thead class="bg-[#171b26] border-b-2 border-black font-label-lg text-label-lg uppercase">
<tr>
<th class="p-space-md border-r-2 border-black text-xs font-black text-on-surface">Egg Target</th>
<th class="p-space-md border-r-2 border-black text-xs font-black text-on-surface">Rarity Tier</th>
<th class="p-space-md border-r-2 border-black text-xs font-black text-on-surface">Location</th>
<th class="p-space-md border-r-2 border-black text-xs font-black text-on-surface">Timestamp</th>
<th class="p-space-md text-xs font-black text-on-surface text-right">Quick Action</th>
</tr>
</thead>
<tbody class="divide-y-2 divide-black" id="drops-table-body">
<tr>
<td colspan="5" class="py-8 text-center text-on-surface-variant font-mono">Connecting to live radar feed...</td>
</tr>
</tbody>
</table>
</section>

<!-- Community & GameFlow Footer -->
<footer class="mt-space-2xl pt-space-xl border-t-2 border-black text-center text-xs text-on-surface-variant font-mono flex flex-col md:flex-row items-center justify-between gap-4 pb-8">
    <div class="flex items-center gap-3">
        <span class="font-bold text-white uppercase">EggStock</span>
        <span>•</span>
        <span>Steal An Egg Tracker</span>
        <span>•</span>
        <span class="text-[#fbff00] font-bold">Created for GameFlow (@GameFlow2489)</span>
    </div>
    <div class="flex items-center gap-4">
        <a href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener" class="text-white hover:text-[#00f0ff] uppercase font-bold">YouTube Channel</a>
        <a href="https://stealanegg.org" target="_blank" rel="noopener" class="text-white hover:text-[#00f0ff] uppercase font-bold">stealanegg.org</a>
        <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] text-black px-3 py-1 border border-black font-black uppercase text-[11px] shadow-[2px_2px_0px_#000]">Play Roblox ↗</a>
    </div>
</footer>
'''

html = re.sub(r'<!-- Live Drops Table -->.*?</body>', table_section + '\n</body>', html, flags=re.DOTALL)

# Inject client-side polling and audio chimes
client_js = '''
<script>
document.addEventListener("DOMContentLoaded", () => {
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
      if (label) label.textContent = soundEnabled ? "Alerts: On" : "Alerts: Off";
      if (icon) {
        icon.textContent = soundEnabled ? "volume_up" : "volume_off";
        icon.style.fontVariationSettings = soundEnabled ? "'FILL' 1" : "'FILL' 0";
      }
      if (soundEnabled) playChime(true);
    });
  }

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
        b.classList.remove("active", "bg-[#00f0ff]", "text-black", "font-black");
        b.classList.add("text-on-surface-variant");
      });
      btn.classList.add("active", "bg-[#00f0ff]", "text-black", "font-black");
      btn.classList.remove("text-on-surface-variant");
      currentFilter = btn.getAttribute("data-filter") || "all";
      if (lastData) renderTable(lastData.recent_drops || []);
    });
  });

  function renderTable(drops) {
    const tbody = document.getElementById("drops-table-body");
    if (!tbody) return;

    const filtered = drops.filter(d => {
      const r = (d.rarity || "").toLowerCase();
      return currentFilter === "all" || r === currentFilter;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-on-surface-variant font-mono">No drops matching filter</td></tr>';
      return;
    }

    const badgeIcons = {
      secret: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter",
      eternal: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter",
      divine: "https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter"
    };

    const rarityColors = {
      divine: "text-[#00f0ff] bg-[#00f0ff]/10 border-[#00f0ff]",
      eternal: "text-[#4edea3] bg-[#4edea3]/10 border-[#4edea3]",
      secret: "text-[#fbabff] bg-[#fbabff]/10 border-[#fbabff]"
    };

    tbody.innerHTML = filtered.map(d => {
      const r = (d.rarity || "").toLowerCase();
      const col = rarityColors[r] || "text-white bg-white/10 border-white";
      const icon = badgeIcons[r] || "";
      const timeStr = formatClock(d.time);

      return `
        <tr class="hover:bg-surface-bright/40 transition-colors font-mono text-sm">
          <td class="p-space-md border-r-2 border-black font-bold text-white flex items-center gap-2">
            ${icon ? `<img src="${icon}" class="w-6 h-6 rounded border border-black" alt="">` : ''}
            <span>${d.egg || "Unknown"}</span>
          </td>
          <td class="p-space-md border-r-2 border-black">
            <span class="px-2 py-0.5 uppercase text-[11px] font-black border ${col}">
              ${d.rarity || "--"}
            </span>
          </td>
          <td class="p-space-md border-r-2 border-black text-on-surface-variant font-sans">
            ${d.location || "World"}
          </td>
          <td class="p-space-md border-r-2 border-black font-timer-display text-white text-xs">
            ${timeStr}
          </td>
          <td class="p-space-md text-right">
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] text-black px-3 py-1 text-xs font-black uppercase border border-black shadow-[2px_2px_0px_#000] hover:bg-white transition-all inline-block no-underline">
              Play ↗
            </a>
          </td>
        </tr>
      `;
    }).join("");
  }

  async function poll() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) return;
      const data = await res.json();
      lastData = data;

      // 1. Next Wave Countdown
      const waveSec = data.next_wave_estimate?.overall?.eta_seconds;
      const intervalSec = data.next_wave_estimate?.overall?.interval_seconds || 600;
      const timeStr = formatWave(waveSec);
      
      const cdTimer = document.getElementById("countdown-timer");
      if (cdTimer) cdTimer.textContent = timeStr;
      const cdTimerSub = document.getElementById("countdown-timer-sub");
      if (cdTimerSub) cdTimerSub.textContent = timeStr;

      const cdBar = document.getElementById("countdown-bar");
      if (cdBar && waveSec !== null && !isNaN(waveSec)) {
        const pct = Math.min(100, Math.max(5, ((intervalSec - waveSec) / intervalSec) * 100));
        cdBar.style.width = pct + "%";
      }

      // 2. Session Drops
      const sDrop = document.getElementById("session-drops-val");
      if (sDrop) sDrop.textContent = (data.session_drops !== undefined ? data.session_drops : "--");
      const lName = document.getElementById("last-drop-name");
      if (lName && data.last_drop?.egg) lName.textContent = `Last: ${data.last_drop.egg}`;
      const lLoc = document.getElementById("last-drop-loc");
      if (lLoc && data.last_drop?.location) lLoc.textContent = data.last_drop.location;

      // 3. Active Players
      if (data.playing_now) {
        const pStr = Number(data.playing_now).toLocaleString();
        const pVal = document.getElementById("active-players-val");
        if (pVal) pVal.textContent = pStr;
        const pValSub = document.getElementById("active-players-val-sub");
        if (pValSub) pValSub.textContent = pStr;
      }

      // 4. Admin Event Countdown
      const now = new Date();
      const nextHour = new Date(now);
      nextHour.setHours(now.getHours() + 1, 0, 0, 0);
      const adminDiff = Math.max(0, Math.floor((nextHour - now) / 1000));
      const adminEl = document.getElementById("admin-countdown-val");
      if (adminEl) adminEl.textContent = formatWave(adminDiff);

      // 5. Rarity Counts & Last Seen
      const rCounts = data.rarity_counts || {};
      const secCount = document.getElementById("secret-count-val");
      if (secCount) secCount.textContent = rCounts.secret || 0;
      const secAgo = document.getElementById("secret-last-seen-val");
      if (secAgo) secAgo.textContent = formatTimeAgo(data.since_secret_seconds);

      const eteCount = document.getElementById("eternal-count-val");
      if (eteCount) eteCount.textContent = rCounts.eternal || 0;
      const eteAgo = document.getElementById("eternal-last-seen-val");
      if (eteAgo) eteAgo.textContent = formatTimeAgo(data.since_eternal_seconds);

      const divCount = document.getElementById("divine-count-val");
      if (divCount) divCount.textContent = rCounts.divine || 0;
      const divAgo = document.getElementById("divine-last-seen-val");
      if (divAgo) divAgo.textContent = formatTimeAgo(data.since_divine_seconds);

      // Audio notification for new Divine / Eternal
      if (data.recent_drops && data.recent_drops.length > 0) {
        const latest = data.recent_drops[0];
        if (latest.time && latest.time !== lastNotifiedDropTime) {
          if (lastNotifiedDropTime !== null) {
            const r = (latest.rarity || "").toLowerCase();
            if (r === "divine") playChime(true);
            else if (r === "eternal" || r === "secret") playChime(false);
          }
          lastNotifiedDropTime = latest.time;
        }
      }

      // 6. Render Table
      renderTable(data.recent_drops || []);

    } catch (err) {
      console.error("Radar poll error:", err);
    }
  }

  poll();
  setInterval(poll, pollMs);
});
</script>
'''

html = html.replace('</body>', client_js + '\n</body>')

with open('website/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully generated website/index.html with Stitch Neo-Brutalist design!")
