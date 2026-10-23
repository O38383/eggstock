import re

html_content = '''<!DOCTYPE html>
<html class="dark" lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
<title>EggStock | Steal An Egg Live Radar 24/7 by GameFlow</title>
<meta name="description" content="EggStock is the #1 live 24/7 spawn tracker and rarity radar for Roblox Steal An Egg. Real-time wave countdowns, official Roblox badge odds, and drop alerts."/>
<meta name="keywords" content="steal an egg, roblox steal an egg, eggstock, egg stock, steal an egg tracker, egg radar, steal an egg wiki, stealanegg, roblox drops, live spawn tracker"/>
<meta name="author" content="GameFlow"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="https://eggstock.xyz/"/>

<!-- Open Graph / Discord / Social Embed -->
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://eggstock.xyz/"/>
<meta property="og:title" content="EggStock | Steal An Egg Live Radar 24/7"/>
<meta property="og:description" content="Real-time spawn intelligence tracking Secret, Eternal, and Divine drops across active Roblox servers with sub-second synchronization."/>
<meta property="og:image" content="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:url" content="https://eggstock.xyz/"/>
<meta name="twitter:title" content="EggStock | Steal An Egg Live Radar 24/7"/>
<meta name="twitter:description" content="Real-time spawn intelligence tracking Secret, Eternal, and Divine drops with sub-second synchronization."/>
<meta name="twitter:image" content="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Favicon -->
<link rel="icon" type="image/png" href="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3496166469031307" crossorigin="anonymous"></script>

<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet"/>

<style>
    body {
        background-color: #0c1017;
        font-family: 'Inter', sans-serif;
        color: #dfe2f1;
        overflow-x: hidden;
    }
    .dot-grid-bg {
        background-color: #0c1017;
        background-image: radial-gradient(rgba(0, 240, 255, 0.13) 1.2px, transparent 1.2px);
        background-size: 22px 22px;
    }
    .neo-box {
        border: 2px solid #000;
        box-shadow: 3px 3px 0px #000;
    }
    .neo-box-lg {
        border: 2px solid #000;
        box-shadow: 4px 4px 0px #000;
    }
    .neo-btn {
        border: 2px solid #000;
        box-shadow: 3px 3px 0px #000;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .neo-btn:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #000;
    }
    .marquee-track {
        display: flex;
        width: max-content;
        animation: marquee 22s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .font-display { font-family: 'Space Grotesk', sans-serif; }
    .font-mono-data { font-family: 'JetBrains Mono', monospace; }
</style>
</head>
<body class="dot-grid-bg min-h-screen">

<!-- Top Navigation Bar -->
<nav class="sticky top-0 w-full z-50 bg-[#0f131d]/95 backdrop-blur-md border-b-2 border-black">
    <div class="max-w-6xl mx-auto px-3 sm:px-6 h-14 sm:h-16 flex items-center justify-between gap-2">
        <!-- Brand -->
        <a href="/" class="flex items-center gap-2 no-underline">
            <img alt="EggStock Logo" class="w-8 h-8 rounded border border-black" src="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>
            <div class="flex items-center gap-1.5">
                <span class="font-display font-black text-lg sm:text-xl uppercase tracking-tight text-[#00f0ff]">EggStock</span>
                <span class="bg-[#fbff00] text-black text-[10px] font-black px-1.5 py-0.2 uppercase border border-black shadow-[1px_1px_0px_#000]">By GameFlow</span>
            </div>
        </a>

        <!-- Desktop Links -->
        <div class="hidden md:flex items-center gap-4 text-xs font-mono font-bold uppercase">
            <a href="#radar" class="text-white hover:text-[#00f0ff] transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">radar</span> Radar
            </a>
            <a href="#rarity" class="text-slate-300 hover:text-white transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">workspace_premium</span> Odds
            </a>
            <a href="#drops" class="text-slate-300 hover:text-white transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">history</span> Drops
            </a>
            <a href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener" class="text-slate-300 hover:text-[#ff3b3b] transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">smart_display</span> YouTube
            </a>
        </div>

        <!-- Action Controls -->
        <div class="flex items-center gap-2">
            <button id="sound-toggle" class="bg-[#1c1f2a] hover:bg-[#262a35] text-white px-2 sm:px-3 py-1.5 neo-btn flex items-center gap-1 text-[11px] sm:text-xs font-bold uppercase">
                <span class="material-symbols-outlined text-[16px] text-[#00f0ff]" style="font-variation-settings: 'FILL' 1;">volume_up</span>
                <span class="hidden sm:inline">Alerts: On</span>
            </button>
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-[#7df4ff] text-black px-3 sm:px-4 py-1.5 neo-btn text-[11px] sm:text-xs font-black uppercase flex items-center gap-1 no-underline">
                <span>Play</span>
                <span class="material-symbols-outlined text-[14px]">open_in_new</span>
            </a>
        </div>
    </div>
</nav>

<!-- Main Container -->
<main class="max-w-6xl mx-auto px-3 sm:px-6 pt-4 sm:pt-8 pb-16">

    <!-- Hero Section -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-8 items-center mb-6 sm:mb-10">
        <!-- Left: Headline & Live Status -->
        <div class="lg:col-span-7 flex flex-col">
            <div class="inline-flex items-center gap-1.5 bg-[#1c1f2a] text-[#00f0ff] px-2.5 py-1 w-max mb-3 border border-black shadow-[2px_2px_0px_#000] text-[11px] font-mono font-bold uppercase">
                <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-ping"></span>
                <span>Live 24/7 Radar Synchronized</span>
            </div>

            <h1 class="font-display font-black text-3xl sm:text-5xl lg:text-6xl uppercase text-white leading-none tracking-tight">
                TRACK SMART.<br/><span class="text-[#00f0ff]">STEAL FIRST.</span>
            </h1>

            <p class="text-xs sm:text-sm text-slate-300 mt-2 sm:mt-3 max-w-lg leading-relaxed">
                Real-time spawn intelligence tracking Secret, Eternal, and Divine egg drops across Roblox servers with sub-second WebSocket telemetry.
            </p>

            <!-- Stat Chips: 2x2 on mobile, flex on desktop -->
            <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 mt-4">
                <div class="bg-[#fbff00] text-black px-2.5 py-1 font-mono-data text-[11px] sm:text-xs uppercase font-black neo-box flex items-center gap-1">
                    <span class="material-symbols-outlined text-[15px]">groups</span>
                    <span id="active-players-val">--</span> Playing
                </div>
                <div class="bg-[#00f0ff] text-black px-2.5 py-1 font-mono-data text-[11px] sm:text-xs uppercase font-black neo-box flex items-center gap-1">
                    <span class="material-symbols-outlined text-[15px]">timer</span>
                    Wave: <span id="countdown-timer" class="font-bold">--:--</span>
                </div>
                <div class="bg-[#1c1f2a] text-white px-2.5 py-1 font-mono-data text-[11px] sm:text-xs uppercase font-bold neo-box flex items-center gap-1">
                    <span class="material-symbols-outlined text-[15px] text-[#ff00ff]">package_2</span>
                    <span id="session-drops-hero">0</span> Drops Today
                </div>
                <div class="bg-[#ff00ff] text-black px-2.5 py-1 font-mono-data text-[11px] sm:text-xs uppercase font-black neo-box flex items-center gap-1">
                    <span class="w-1.5 h-1.5 bg-black rounded-full animate-pulse"></span>
                    24/7 RADAR
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-3 mt-4 sm:mt-6">
                <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-[#7df4ff] text-black font-display font-black text-center text-xs uppercase px-5 py-2.5 neo-btn flex items-center justify-center gap-1.5 no-underline">
                    <span class="material-symbols-outlined text-[18px]">bolt</span>
                    <span>Launch Steal An Egg</span>
                </a>
                <a href="#drops" class="bg-[#1c1f2a] hover:bg-[#262a35] text-white font-display font-bold text-center text-xs uppercase px-4 py-2.5 neo-btn flex items-center justify-center gap-1.5 no-underline">
                    <span class="material-symbols-outlined text-[18px]">travel_explore</span>
                    <span>View Live Drops Feed</span>
                </a>
            </div>
        </div>

        <!-- Right: Collectible Case File Card (Smooth CSS 3D, zero lag) -->
        <div class="lg:col-span-5 mt-4 lg:mt-0">
            <div class="bg-[#171b26] p-4 sm:p-5 neo-box-lg relative transform sm:rotate-1 hover:rotate-0 transition-transform duration-200">
                <!-- Top Badges -->
                <div class="flex items-center justify-between mb-3">
                    <span class="bg-[#ff00ff] text-black text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">★ RARE TARGET</span>
                    <span class="bg-[#00f0ff] text-black text-[10px] font-mono-data font-black uppercase px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">CASE FILE #001</span>
                </div>

                <!-- Featured Target Box -->
                <div class="bg-[#0c1017] border-2 border-black p-4 text-center relative overflow-hidden">
                    <div class="absolute -right-8 -top-8 w-28 h-28 bg-[#00f0ff]/10 rounded-full blur-xl pointer-events-none"></div>
                    <div class="flex justify-center mb-2">
                        <img id="featured-egg-img" src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Egg Badge" class="w-16 h-16 sm:w-20 sm:h-20 rounded border-2 border-black shadow-[3px_3px_0px_#000]">
                    </div>
                    <div class="font-display font-black text-xl sm:text-2xl uppercase text-white tracking-wide" id="featured-egg-name">Secret Egg Target</div>
                    <div class="text-xs font-mono text-[#fbabff] font-bold mt-0.5" id="featured-egg-loc">Location: Active Radar</div>
                    <div class="mt-3 inline-block bg-[#1c1f2a] border border-black px-3 py-1 text-[11px] font-mono text-slate-300">
                        Next Wave In: <span class="text-[#00f0ff] font-bold" id="featured-egg-timer">--:--</span>
                    </div>
                </div>

                <!-- Card Footer Info -->
                <div class="mt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Telemetry: Verified SenZ V2</span>
                    <span class="text-[#00f0ff]">Auto-Sync ●</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Animated Running Marquee Ticker Ribbon -->
    <div class="w-full bg-[#fbff00] text-black font-mono-data text-xs sm:text-sm font-black py-1.5 sm:py-2 overflow-hidden neo-box mb-6 sm:mb-10">
        <div class="marquee-track">
            <div class="whitespace-nowrap px-4">
                ⚡ LIVE RADAR ACTIVE ⬡ NEXT WAVE PREDICTION SYNCED ⬡ SECRET ODDS 0.051% (1 IN ~1,960) ⬡ ETERNAL ODDS 0.046% (1 IN ~2,170) ⬡ DIVINE ODDS 0.008% (1 IN ~12,500) ⬡ POWERED BY GAMEFLOW (@GameFlow2489) ⬡ HATCH SMART STEAL SMARTER ⬡
            </div>
            <div class="whitespace-nowrap px-4">
                ⚡ LIVE RADAR ACTIVE ⬡ NEXT WAVE PREDICTION SYNCED ⬡ SECRET ODDS 0.051% (1 IN ~1,960) ⬡ ETERNAL ODDS 0.046% (1 IN ~2,170) ⬡ DIVINE ODDS 0.008% (1 IN ~12,500) ⬡ POWERED BY GAMEFLOW (@GameFlow2489) ⬡ HATCH SMART STEAL SMARTER ⬡
            </div>
        </div>
    </div>

    <!-- Live Analytics 4-Card Grid -->
    <section id="radar" class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4 mb-6 sm:mb-10">
        <!-- 1. Wave Prediction -->
        <div class="bg-[#1c1f2a] p-3 sm:p-4 neo-box flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[10px] sm:text-xs uppercase font-mono text-slate-400 font-bold">Wave Prediction</span>
                <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-pulse"></span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#00f0ff]" id="countdown-timer-sub">--:--</span>
                <span class="text-[10px] sm:text-xs font-bold text-[#4edea3] uppercase animate-pulse">● Imminent</span>
            </div>
            <div class="w-full bg-black h-1.5 border border-black/40 overflow-hidden">
                <div class="bg-[#00f0ff] h-full w-3/4 transition-all duration-300" id="countdown-bar"></div>
            </div>
            <span class="mt-1.5 text-[10px] text-slate-400 block truncate">Observed drop intervals</span>
        </div>

        <!-- 2. Session Drops -->
        <div class="bg-[#1c1f2a] p-3 sm:p-4 neo-box flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[10px] sm:text-xs uppercase font-mono text-slate-400 font-bold">Session Drops</span>
                <span class="material-symbols-outlined text-[#ff00ff] text-[18px]">package_2</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-white" id="session-drops-val">0</span>
                <span class="text-[10px] sm:text-xs text-[#fbabff] font-bold truncate" id="last-drop-name">Last: --</span>
            </div>
            <span class="mt-1.5 text-[10px] text-slate-400 block truncate" id="last-drop-loc">Listening for drops...</span>
        </div>

        <!-- 3. Active Roblox Players -->
        <div class="bg-[#1c1f2a] p-3 sm:p-4 neo-box flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[10px] sm:text-xs uppercase font-mono text-slate-400 font-bold">Roblox Players</span>
                <span class="material-symbols-outlined text-[#4edea3] text-[18px]">groups</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#4edea3]" id="active-players-val-sub">--</span>
                <span class="text-[10px] sm:text-xs text-[#4edea3] font-bold">● Live</span>
            </div>
            <span class="mt-1.5 text-[10px] text-slate-400 block truncate">Steal An Egg Universe</span>
        </div>

        <!-- 4. Admin Event Countdown -->
        <div class="bg-[#1c1f2a] p-3 sm:p-4 neo-box flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[10px] sm:text-xs uppercase font-mono text-slate-400 font-bold">Admin 2x Luck</span>
                <span class="material-symbols-outlined text-[#ffb4ab] text-[18px]">bolt</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#ffb4ab]" id="admin-countdown-val">--:--</span>
                <span class="text-[10px] sm:text-xs text-slate-400 font-bold">Boost</span>
            </div>
            <span class="mt-1.5 text-[10px] text-slate-400 block truncate">Next hourly event</span>
        </div>
    </section>

    <!-- Rarity Odds Section -->
    <section id="rarity" class="mb-6 sm:mb-10">
        <div class="flex flex-col sm:flex-row items-start sm:items-end justify-between mb-3 sm:mb-4 gap-1">
            <div>
                <span class="text-[10px] font-black uppercase tracking-wider bg-[#fbff00] text-black px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">Verified Telemetry</span>
                <h2 class="font-display font-black text-xl sm:text-2xl uppercase text-white mt-1">Roblox Badge Odds</h2>
            </div>
            <a href="https://stealanegg.org" target="_blank" rel="noopener" class="text-[11px] font-mono text-slate-400 hover:text-[#00f0ff] underline">
                Documented on stealanegg.org ↗
            </a>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
            <!-- Secret Card -->
            <div class="bg-[#1c1f2a] p-3.5 sm:p-4 neo-box hover:shadow-[5px_5px_0px_#000] transition-shadow">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#fbabff] uppercase font-bold">Mythic Tier</span>
                        <div class="font-display text-lg sm:text-xl font-black text-[#fbabff]">Secret Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Secret Badge" class="w-9 h-9 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="mt-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-2xl sm:text-3xl font-mono-data font-black text-white" id="secret-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Drop</span>
                        <span class="text-xs font-bold text-[#fbabff]" id="secret-last-seen-val">--</span>
                    </div>
                </div>
                <div class="mt-3 pt-2.5 border-t border-black/40 flex items-center justify-between text-[11px] font-mono">
                    <span class="text-white font-bold bg-[#ff00ff]/20 px-1.5 py-0.5 border border-[#ff00ff]/40">Odds: ~0.051% (1 in ~1,960)</span>
                    <span class="text-slate-400 text-[10px]">31.2M+ wins</span>
                </div>
            </div>

            <!-- Eternal Card -->
            <div class="bg-[#1c1f2a] p-3.5 sm:p-4 neo-box hover:shadow-[5px_5px_0px_#000] transition-shadow">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#4edea3] uppercase font-bold">Legendary Tier</span>
                        <div class="font-display text-lg sm:text-xl font-black text-[#4edea3]">Eternal Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter" alt="Eternal Badge" class="w-9 h-9 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="mt-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-2xl sm:text-3xl font-mono-data font-black text-white" id="eternal-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Drop</span>
                        <span class="text-xs font-bold text-[#4edea3]" id="eternal-last-seen-val">--</span>
                    </div>
                </div>
                <div class="mt-3 pt-2.5 border-t border-black/40 flex items-center justify-between text-[11px] font-mono">
                    <span class="text-white font-bold bg-[#4edea3]/20 px-1.5 py-0.5 border border-[#4edea3]/40">Odds: ~0.046% (1 in ~2,170)</span>
                    <span class="text-slate-400 text-[10px]">19.8M+ wins</span>
                </div>
            </div>

            <!-- Divine Card -->
            <div class="bg-[#1c1f2a] p-3.5 sm:p-4 neo-box hover:shadow-[5px_5px_0px_#000] transition-shadow">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#00f0ff] uppercase font-bold">Celestial Tier</span>
                        <div class="font-display text-lg sm:text-xl font-black text-[#00f0ff]">Divine Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter" alt="Divine Badge" class="w-9 h-9 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="mt-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-2xl sm:text-3xl font-mono-data font-black text-white" id="divine-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Drop</span>
                        <span class="text-xs font-bold text-[#00f0ff]" id="divine-last-seen-val">--</span>
                    </div>
                </div>
                <div class="mt-3 pt-2.5 border-t border-black/40 flex items-center justify-between text-[11px] font-mono">
                    <span class="text-white font-bold bg-[#00f0ff]/20 px-1.5 py-0.5 border border-[#00f0ff]/40">Odds: ~0.008% (1 in ~12,500)</span>
                    <span class="text-slate-400 text-[10px]">1.69M+ wins</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Live Drops Feed -->
    <section id="drops" class="mb-12">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5 mb-3">
            <div>
                <h3 class="font-display font-black text-xl sm:text-2xl uppercase text-white">Live Drops Feed</h3>
                <p class="text-xs text-slate-400 font-mono">Captured in real-time with duplicate prevention</p>
            </div>

            <!-- Filter Buttons -->
            <div class="flex items-center gap-1 bg-black p-1 neo-box self-stretch sm:self-auto justify-center">
                <button class="filter-btn active bg-[#00f0ff] text-black font-black uppercase text-[11px] sm:text-xs px-2.5 py-1 border border-black" data-filter="all">All</button>
                <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-[11px] sm:text-xs px-2.5 py-1" data-filter="secret">Secret</button>
                <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-[11px] sm:text-xs px-2.5 py-1" data-filter="eternal">Eternal</button>
                <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-[11px] sm:text-xs px-2.5 py-1" data-filter="divine">Divine</button>
            </div>
        </div>

        <!-- Table Container -->
        <div class="bg-[#1c1f2a] neo-box-lg overflow-x-auto">
            <table class="w-full text-left font-mono-data text-xs">
                <thead class="bg-[#12151e] border-b-2 border-black uppercase text-[11px] text-slate-300">
                    <tr>
                        <th class="p-2.5 sm:p-3 border-r-2 border-black font-black">Egg Target</th>
                        <th class="p-2.5 sm:p-3 border-r-2 border-black font-black">Rarity</th>
                        <th class="p-2.5 sm:p-3 border-r-2 border-black font-black">Location</th>
                        <th class="p-2.5 sm:p-3 border-r-2 border-black font-black">Timestamp</th>
                        <th class="p-2.5 sm:p-3 text-right font-black">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y-2 divide-black" id="drops-table-body">
                    <tr>
                        <td colspan="5" class="py-8 text-center text-slate-400 font-mono">Connecting to live radar feed...</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

</main>

<!-- Footer -->
<footer class="bg-[#0f131d] border-t-2 border-black py-6 px-3 sm:px-6">
    <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-400 text-center sm:text-left">
        <div class="flex items-center gap-2">
            <span class="font-bold text-white uppercase">EggStock</span>
            <span>•</span>
            <span class="text-[#fbff00] font-bold">GameFlow (@GameFlow2489)</span>
        </div>
        <div class="flex flex-wrap items-center justify-center gap-4">
            <a href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener" class="text-white hover:text-[#00f0ff] uppercase font-bold">YouTube</a>
            <a href="/privacy" class="text-slate-400 hover:text-white uppercase">Privacy</a>
            <a href="/terms" class="text-slate-400 hover:text-white uppercase">Terms</a>
            <a href="https://stealanegg.org" target="_blank" rel="noopener" class="text-slate-400 hover:text-white uppercase">Docs</a>
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] text-black px-2.5 py-1 neo-btn font-black uppercase text-[11px] no-underline">Play Roblox ↗</a>
        </div>
    </div>
</footer>

<!-- Client JavaScript: Buttery Smooth 1s Local Countdown + Dedup -->
<script>
document.addEventListener("DOMContentLoaded", () => {
    // Audio Chimes setup
    let soundEnabled = true;
    let audioCtx = null;
    let lastNotifiedTime = null;

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
                gain.gain.setValueAtTime(0.2, now + i * 0.12);
                gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.55);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(now + i * 0.12);
                osc.stop(now + i * 0.12 + 0.6);
            });
        } catch (e) {}
    }

    const soundToggleBtn = document.getElementById("sound-toggle");
    if (soundToggleBtn) {
        soundToggleBtn.addEventListener("click", () => {
            soundEnabled = !soundEnabled;
            const icon = soundToggleBtn.querySelector(".material-symbols-outlined");
            const label = soundToggleBtn.querySelector("span:last-child");
            if (label) label.textContent = soundEnabled ? "Alerts: On" : "Alerts: Off";
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

    // Local Smooth 1-Second Countdown State
    let localWaveSec = null;
    let localIntervalSec = 600;
    let currentFilter = "all";
    let lastData = null;

    function renderWaveUI(sec, interval) {
        const timeStr = formatWave(sec);
        const timer1 = document.getElementById("countdown-timer");
        if (timer1) timer1.textContent = timeStr;
        const timer2 = document.getElementById("countdown-timer-sub");
        if (timer2) timer2.textContent = timeStr;
        const timer3 = document.getElementById("featured-egg-timer");
        if (timer3) timer3.textContent = timeStr;

        const bar = document.getElementById("countdown-bar");
        if (bar && sec !== null && !isNaN(sec) && interval > 0) {
            const pct = Math.min(100, Math.max(5, ((interval - sec) / interval) * 100));
            bar.style.width = pct + "%";
        }
    }

    // Smooth Local 1-Second Timer (decrements every second without jumping)
    setInterval(() => {
        // 1. Decrement wave countdown
        if (localWaveSec !== null && localWaveSec > 0) {
            localWaveSec--;
            renderWaveUI(localWaveSec, localIntervalSec);
        } else if (localWaveSec === 0) {
            // Reached zero - wave cycle restarts
            localWaveSec = localIntervalSec;
            renderWaveUI(localWaveSec, localIntervalSec);
        }

        // 2. Decrement admin event countdown
        const now = new Date();
        const nextHour = new Date(now);
        nextHour.setHours(now.getHours() + 1, 0, 0, 0);
        const adminDiff = Math.max(0, Math.floor((nextHour - now) / 1000));
        const adminEl = document.getElementById("admin-countdown-val");
        if (adminEl) adminEl.textContent = formatWave(adminDiff);
    }, 1000);

    // Filter Buttons
    const filterBtns = document.querySelectorAll(".filter-btn");
    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            filterBtns.forEach(b => {
                b.classList.remove("active", "bg-[#00f0ff]", "text-black", "font-black");
                b.classList.add("text-slate-400");
            });
            btn.classList.add("active", "bg-[#00f0ff]", "text-black", "font-black");
            btn.classList.remove("text-slate-400");
            currentFilter = btn.getAttribute("data-filter") || "all";
            if (lastData) renderTable(lastData.recent_drops || []);
        });
    });

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

    function renderTable(drops) {
        const tbody = document.getElementById("drops-table-body");
        if (!tbody) return;

        const filtered = drops.filter(d => {
            const r = (d.rarity || "").toLowerCase();
            return currentFilter === "all" || r === currentFilter;
        });

        // 10-minute duplicate prevention
        const deduped = [];
        const seen = {};
        for (const d of filtered) {
            const key = `${(d.egg || "").toLowerCase()}|${(d.location || "").toLowerCase()}|${(d.rarity || "").toLowerCase()}`;
            const ts = d.time ? new Date(d.time).getTime() : 0;
            const lastTs = seen[key] || 0;
            if (lastTs && Math.abs(ts - lastTs) < 600000) continue; // 10 min window
            seen[key] = ts;
            deduped.push(d);
        }

        if (deduped.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-slate-400 font-mono">No drops matching filter</td></tr>';
            return;
        }

        tbody.innerHTML = deduped.map(d => {
            const r = (d.rarity || "").toLowerCase();
            const col = rarityColors[r] || "text-white bg-white/10 border-white";
            const icon = badgeIcons[r] || "";
            const timeStr = formatClock(d.time);

            return `
                <tr class="hover:bg-[#262a35] transition-colors">
                    <td class="p-2.5 sm:p-3 border-r-2 border-black font-bold text-white flex items-center gap-2">
                        ${icon ? `<img src="${icon}" class="w-6 h-6 rounded border border-black shrink-0" alt="">` : ''}
                        <span class="truncate">${d.egg || "Unknown"}</span>
                    </td>
                    <td class="p-2.5 sm:p-3 border-r-2 border-black">
                        <span class="px-1.5 py-0.5 uppercase text-[10px] font-black border ${col}">
                            ${d.rarity || "--"}
                        </span>
                    </td>
                    <td class="p-2.5 sm:p-3 border-r-2 border-black text-slate-300 font-sans truncate">
                        ${d.location || "World"}
                    </td>
                    <td class="p-2.5 sm:p-3 border-r-2 border-black font-mono-data text-white text-[11px] whitespace-nowrap">
                        ${timeStr}
                    </td>
                    <td class="p-2.5 sm:p-3 text-right">
                        <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-white text-black px-2.5 py-1 text-[11px] font-black uppercase neo-btn inline-block no-underline">
                            Play ↗
                        </a>
                    </td>
                </tr>
            `;
        }).join("");
    }

    // Polling function (resyncs with server data every 3 seconds)
    async function poll() {
        try {
            const res = await fetch("/api/status");
            if (!res.ok) return;
            const data = await res.json();
            lastData = data;

            // 1. Sync Wave Prediction (only update if drift > 2s to preserve smooth 1s tick)
            const serverEta = data.next_wave_estimate?.overall?.eta_seconds;
            localIntervalSec = data.next_wave_estimate?.overall?.interval_seconds || 600;
            if (serverEta !== undefined && serverEta !== null) {
                if (localWaveSec === null || Math.abs(localWaveSec - serverEta) > 2) {
                    localWaveSec = serverEta;
                    renderWaveUI(localWaveSec, localIntervalSec);
                }
            }

            // 2. Session Drops
            const dropsCount = data.session_drops !== undefined ? data.session_drops : 0;
            const sDrop = document.getElementById("session-drops-val");
            if (sDrop) sDrop.textContent = dropsCount;
            const sDropHero = document.getElementById("session-drops-hero");
            if (sDropHero) sDropHero.textContent = dropsCount;

            // Last drop info
            if (data.last_drop?.egg) {
                const lName = document.getElementById("last-drop-name");
                if (lName) lName.textContent = `Last: ${data.last_drop.egg}`;
                const lLoc = document.getElementById("last-drop-loc");
                if (lLoc && data.last_drop.location) lLoc.textContent = data.last_drop.location;

                // Update Case File Card
                const featName = document.getElementById("featured-egg-name");
                if (featName) featName.textContent = data.last_drop.egg;
                const featLoc = document.getElementById("featured-egg-loc");
                if (featLoc && data.last_drop.location) featLoc.textContent = `Location: ${data.last_drop.location}`;
                const featImg = document.getElementById("featured-egg-img");
                const r = (data.last_drop.rarity || "").toLowerCase();
                if (featImg && badgeIcons[r]) featImg.src = badgeIcons[r];
            }

            // 3. Real Active Roblox Players (No fake numbers)
            if (data.playing_now !== undefined && data.playing_now !== null) {
                const pStr = Number(data.playing_now).toLocaleString();
                const pVal = document.getElementById("active-players-val");
                if (pVal) pVal.textContent = pStr;
                const pValSub = document.getElementById("active-players-val-sub");
                if (pValSub) pValSub.textContent = pStr;
            }

            // 4. Rarity Counts & Last Seen
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

            // Audio Alert on new drop
            if (data.recent_drops && data.recent_drops.length > 0) {
                const latest = data.recent_drops[0];
                if (latest.time && latest.time !== lastNotifiedTime) {
                    if (lastNotifiedTime !== null) {
                        const r = (latest.rarity || "").toLowerCase();
                        if (r === "divine") playChime(true);
                        else if (r === "eternal" || r === "secret") playChime(false);
                    }
                    lastNotifiedTime = latest.time;
                }
            }

            // 5. Render Table with Dedup
            renderTable(data.recent_drops || []);

        } catch (err) {
            console.error("Radar poll error:", err);
        }
    }

    poll();
    setInterval(poll, 3000); // 3-second server poll
});
</script>
</body>
</html>
'''

with open('website/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Created ultra-optimized, mobile-responsive, lag-free website/index.html!")
