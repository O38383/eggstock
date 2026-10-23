import os

html = '''<!DOCTYPE html>
<html class="dark" lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
<title>EggStock | Steal An Egg Live Radar 24/7 by GameFlow</title>
<meta name="description" content="EggStock is the #1 live 24/7 spawn tracker and rarity radar for Roblox Steal An Egg. Real-time wave countdowns, official Roblox badge odds, hatch calculator, and drop alerts."/>
<meta name="keywords" content="steal an egg, roblox steal an egg, eggstock, egg stock, steal an egg tracker, egg radar, steal an egg wiki, stealanegg, roblox drops, live spawn tracker, egg odds calculator"/>
<meta name="author" content="GameFlow"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="https://eggstock.xyz/"/>

<!-- Open Graph / Discord / Social Embed -->
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://eggstock.xyz/"/>
<meta property="og:title" content="EggStock | Steal An Egg Live Radar 24/7"/>
<meta property="og:description" content="Real-time spawn intelligence tracking Secret, Eternal, and Divine drops with sub-second synchronization and interactive odds calculator."/>
<meta property="og:image" content="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:url" content="https://eggstock.xyz/"/>
<meta name="twitter:title" content="EggStock | Steal An Egg Live Radar 24/7"/>
<meta name="twitter:description" content="Real-time spawn intelligence tracking Secret, Eternal, and Divine drops with sub-second synchronization."/>
<meta name="twitter:image" content="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Favicon -->
<link rel="icon" type="image/png" href="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>

<!-- Google Verification & AdSense -->
<meta name="google-site-verification" content="google2dcf6b5ce2c3be8e"/>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3496166469031307" crossorigin="anonymous"></script>

<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet"/>

<style>
    body {
        background-color: #0a0d14;
        font-family: 'Inter', sans-serif;
        color: #dfe2f1;
        overflow-x: hidden;
    }
    .dot-grid-bg {
        background-color: #0a0d14;
        background-image: radial-gradient(rgba(0, 240, 255, 0.12) 1.2px, transparent 1.2px);
        background-size: 24px 24px;
    }
    .neo-card {
        background: #131722;
        border: 2px solid #000;
        box-shadow: 4px 4px 0px #000;
    }
    .neo-card-sm {
        background: #131722;
        border: 2px solid #000;
        box-shadow: 2.5px 2.5px 0px #000;
    }
    .neo-btn {
        border: 2px solid #000;
        box-shadow: 3px 3px 0px #000;
        transition: all 0.1s ease;
    }
    .neo-btn:active {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #000;
    }
    .marquee-track {
        display: flex;
        width: max-content;
        animation: marquee 24s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .font-display { font-family: 'Space Grotesk', sans-serif; }
    .font-mono-data { font-family: 'JetBrains Mono', monospace; }

    /* Custom range slider style */
    input[type=range] {
        accent-color: #00f0ff;
    }

    /* Modal animation */
    .modal-backdrop {
        background: rgba(5, 7, 12, 0.85);
        backdrop-filter: blur(8px);
    }
</style>
</head>
<body class="dot-grid-bg min-h-screen flex flex-col pb-20 sm:pb-8">

<!-- Toast Notification Container -->
<div id="toast" class="fixed top-18 right-4 z-50 transform -translate-y-12 opacity-0 pointer-events-none transition-all duration-300 bg-[#00f0ff] text-black font-mono font-bold text-xs px-4 py-2 border-2 border-black shadow-[3px_3px_0px_#000] flex items-center gap-2">
    <span class="material-symbols-outlined text-[18px]">check_circle</span>
    <span id="toast-msg">Copied to clipboard!</span>
</div>

<!-- TOP NAVIGATION BAR -->
<header class="sticky top-0 w-full z-40 bg-[#0a0d14]/90 backdrop-blur-lg border-b-2 border-black">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between">
        <!-- Brand -->
        <a href="/" class="flex items-center gap-2.5 no-underline">
            <img alt="EggStock Logo" class="w-7 h-7 sm:w-8 sm:h-8 rounded border border-black" src="https://lh3.googleusercontent.com/aida/AEtjO1Wa4M5ukyQa4aUCumL2E7BTkVxzPcYpW3DHQF_VckG29CkHj9qDi4n0nyUEQCzU5EVDGOAB-fzIIs6832eMnQx3xy1X-lk1xD2Sp84fta7YieJXfbwJruOgqTt9jJ0fchDFCllw5AIgfWYfhjtkndLqLdC9JS4cckQk-bzQHVA_i8QJDmYPjXGLDnyXIqci8Qu_sSwBfQrbT5akGcc_KEmGjgtkWqf_dBYF1uah0NIogZqDs3zRw8RNAmE"/>
            <div class="flex items-center gap-1.5">
                <span class="font-display font-black text-base sm:text-xl uppercase tracking-tight text-[#00f0ff]">EggStock</span>
                <span class="bg-[#fbff00] text-black text-[9px] sm:text-[10px] font-black px-1.5 py-0.2 uppercase border border-black shadow-[1px_1px_0px_#000]">GameFlow</span>
            </div>
        </a>

        <!-- Desktop Links -->
        <div class="hidden lg:flex items-center gap-5 text-xs font-mono font-bold uppercase">
            <a href="#radar" class="text-white hover:text-[#00f0ff] transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">radar</span> Radar
            </a>
            <a href="#calculator" class="text-slate-400 hover:text-[#00f0ff] transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">calculate</span> Odds Calc
            </a>
            <a href="#rarity" class="text-slate-400 hover:text-white transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">workspace_premium</span> Odds
            </a>
            <a href="#worlds" class="text-slate-400 hover:text-white transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">map</span> Worlds
            </a>
            <a href="#drops" class="text-slate-400 hover:text-white transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">history</span> Drops
            </a>
            <a href="https://www.youtube.com/@GameFlow2489" target="_blank" rel="noopener" class="text-slate-400 hover:text-[#ff3b3b] transition-colors flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">smart_display</span> YouTube
            </a>
        </div>

        <!-- Quick Controls -->
        <div class="flex items-center gap-2">
            <button id="sound-toggle" title="Toggle Sound Alerts" class="bg-[#181d2c] hover:bg-[#23293d] text-white p-2 sm:px-3 sm:py-1.5 neo-btn flex items-center gap-1 text-xs font-bold">
                <span class="material-symbols-outlined text-[16px] text-[#00f0ff]" style="font-variation-settings: 'FILL' 1;">volume_up</span>
                <span class="hidden sm:inline uppercase text-[11px]" id="sound-toggle-label">Sound</span>
            </button>
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-[#7df4ff] text-black px-3 sm:px-4 py-1.5 neo-btn text-xs font-black uppercase flex items-center gap-1 no-underline">
                <span>Play</span>
                <span class="material-symbols-outlined text-[14px]">open_in_new</span>
            </a>
        </div>
    </div>
</header>

<!-- MAIN CONTAINER -->
<main class="max-w-6xl mx-auto px-4 sm:px-6 pt-6 sm:pt-10 flex-grow w-full space-y-8 sm:space-y-12">

    <!-- HERO SECTION -->
    <section class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-10 items-center">
        <!-- Left Column -->
        <div class="lg:col-span-7 flex flex-col space-y-4 sm:space-y-5">
            <!-- Pill Status Badge -->
            <div class="inline-flex items-center gap-2 bg-[#131722] px-3 py-1 w-max border border-black shadow-[2px_2px_0px_#000]">
                <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-ping"></span>
                <span class="text-[11px] font-mono font-bold uppercase text-[#00f0ff]">24/7 Live Spawn Radar</span>
            </div>

            <!-- Big Confident Headline -->
            <h1 class="font-display font-black text-3xl sm:text-5xl lg:text-6xl uppercase text-white leading-[1.05] tracking-tight">
                HATCH RARE.<br/>
                <span class="text-[#00f0ff]">STEAL SMARTER.</span>
            </h1>

            <p class="text-xs sm:text-sm text-slate-300 max-w-lg leading-relaxed">
                Real-time spawn intelligence tracking Secret, Eternal, and Divine egg drops across active Roblox servers with sub-second wave predictions.
            </p>

            <!-- Stat Chips -->
            <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 pt-1">
                <div class="bg-[#181d2c] text-white px-3 py-1.5 font-mono-data text-xs neo-card-sm flex items-center gap-2">
                    <span class="material-symbols-outlined text-[16px] text-[#fbff00]">groups</span>
                    <div>
                        <div class="text-[9px] uppercase text-slate-400 font-bold">Online Now</div>
                        <div class="font-bold text-white" id="active-players-val">--</div>
                    </div>
                </div>
                <div class="bg-[#181d2c] text-white px-3 py-1.5 font-mono-data text-xs neo-card-sm flex items-center gap-2">
                    <span class="material-symbols-outlined text-[16px] text-[#00f0ff]">timer</span>
                    <div>
                        <div class="text-[9px] uppercase text-slate-400 font-bold">Next Wave</div>
                        <div class="font-bold text-[#00f0ff]" id="countdown-timer">--:--</div>
                    </div>
                </div>
                <div class="bg-[#181d2c] text-white px-3 py-1.5 font-mono-data text-xs neo-card-sm flex items-center gap-2">
                    <span class="material-symbols-outlined text-[16px] text-[#ff00ff]">package_2</span>
                    <div>
                        <div class="text-[9px] uppercase text-slate-400 font-bold">Session Drops</div>
                        <div class="font-bold text-white" id="session-drops-hero">0</div>
                    </div>
                </div>
                <div class="bg-[#181d2c] text-white px-3 py-1.5 font-mono-data text-xs neo-card-sm flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-[#4edea3] animate-pulse"></span>
                    <div>
                        <div class="text-[9px] uppercase text-slate-400 font-bold">Admin Boost</div>
                        <div class="font-bold text-[#4edea3]" id="hero-admin-countdown">--:--</div>
                    </div>
                </div>
            </div>

            <!-- Primary CTAs -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
                <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-[#7df4ff] text-black font-display font-black text-center text-xs uppercase px-6 py-3 neo-btn flex items-center justify-center gap-2 no-underline">
                    <span class="material-symbols-outlined text-[18px]">bolt</span>
                    <span>Play Steal An Egg ↗</span>
                </a>
                <a href="#calculator" class="bg-[#fbff00] hover:bg-yellow-300 text-black font-display font-black text-center text-xs uppercase px-5 py-3 neo-btn flex items-center justify-center gap-2 no-underline">
                    <span class="material-symbols-outlined text-[18px]">calculate</span>
                    <span>Test Hatch Odds</span>
                </a>
                <a href="#drops" class="bg-[#181d2c] hover:bg-[#23293d] text-white font-display font-bold text-center text-xs uppercase px-4 py-3 neo-btn flex items-center justify-center gap-2 no-underline">
                    <span class="material-symbols-outlined text-[18px]">travel_explore</span>
                    <span>Live Drops Feed ↓</span>
                </a>
            </div>
        </div>

        <!-- Right Column: Interactive Collectible Card -->
        <div class="lg:col-span-5">
            <div class="neo-card p-5 relative transform sm:rotate-1 hover:rotate-0 transition-transform duration-200 cursor-pointer" id="hero-card-trigger">
                <!-- Card Header -->
                <div class="flex items-center justify-between mb-4">
                    <span class="bg-[#ff00ff] text-black text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">★ LATEST TARGET</span>
                    <span class="bg-[#00f0ff] text-black text-[10px] font-mono-data font-black uppercase px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">CLICK FOR INTEL 🔍</span>
                </div>

                <!-- Showcase Center -->
                <div class="bg-[#0a0d14] border-2 border-black p-5 text-center relative overflow-hidden">
                    <div class="flex justify-center mb-3">
                        <img id="featured-egg-img" src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Egg Badge" class="w-16 h-16 sm:w-20 sm:h-20 rounded border-2 border-black shadow-[3px_3px_0px_#000]">
                    </div>
                    <div class="font-display font-black text-xl sm:text-2xl uppercase text-white tracking-wide" id="featured-egg-name">Waiting For Spawn...</div>
                    <div class="text-xs font-mono text-[#fbabff] font-bold mt-1" id="featured-egg-loc">Location: Active Radar</div>
                    
                    <div class="mt-4 inline-flex items-center gap-2 bg-[#181d2c] border border-black px-3 py-1.5 text-xs font-mono">
                        <span class="text-slate-400">Next Wave:</span>
                        <span class="text-[#00f0ff] font-black font-mono-data" id="featured-egg-timer">--:--</span>
                    </div>
                </div>

                <!-- Card Footer -->
                <div class="mt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
                    <span>Telemetry: SenZ V2 Live</span>
                    <span class="text-[#4edea3] flex items-center gap-1 font-bold">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#4edea3]"></span> Synced
                    </span>
                </div>
            </div>
        </div>
    </section>

    <!-- TICKER TAPE -->
    <div class="w-full bg-[#fbff00] text-black font-mono-data text-xs font-black py-2 overflow-hidden neo-card-sm">
        <div class="marquee-track">
            <div class="whitespace-nowrap px-4">
                ⚡ LIVE RADAR ACTIVE ⬡ NEXT WAVE PREDICTION SYNCED ⬡ SECRET ODDS 0.051% (1 IN ~1,960) ⬡ ETERNAL ODDS 0.046% (1 IN ~2,170) ⬡ DIVINE ODDS 0.008% (1 IN ~12,500) ⬡ POWERED BY GAMEFLOW (@GameFlow2489) ⬡ HATCH SMART STEAL SMARTER ⬡
            </div>
            <div class="whitespace-nowrap px-4">
                ⚡ LIVE RADAR ACTIVE ⬡ NEXT WAVE PREDICTION SYNCED ⬡ SECRET ODDS 0.051% (1 IN ~1,960) ⬡ ETERNAL ODDS 0.046% (1 IN ~2,170) ⬡ DIVINE ODDS 0.008% (1 IN ~12,500) ⬡ POWERED BY GAMEFLOW (@GameFlow2489) ⬡ HATCH SMART STEAL SMARTER ⬡
            </div>
        </div>
    </div>

    <!-- LIVE TELEMETRY 4-METRIC GRID -->
    <section id="radar" class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <!-- 1. Wave Countdown -->
        <div class="neo-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[11px] uppercase font-mono text-slate-400 font-bold">Wave Prediction</span>
                <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-pulse"></span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#00f0ff]" id="countdown-timer-sub">--:--</span>
            </div>
            <div class="w-full bg-black h-2 border border-black/40 overflow-hidden">
                <div class="bg-[#00f0ff] h-full w-3/4 transition-all duration-300" id="countdown-bar"></div>
            </div>
            <span class="mt-2 text-[10px] text-slate-400 block truncate">Observed drop cycle</span>
        </div>

        <!-- 2. Session Drops -->
        <div class="neo-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[11px] uppercase font-mono text-slate-400 font-bold">Session Drops</span>
                <span class="material-symbols-outlined text-[#ff00ff] text-[18px]">package_2</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-white" id="session-drops-val">0</span>
                <span class="text-xs text-[#fbabff] font-bold truncate" id="last-drop-name">Last: --</span>
            </div>
            <span class="mt-2 text-[10px] text-slate-400 block truncate" id="last-drop-loc">Listening for drops...</span>
        </div>

        <!-- 3. Active Roblox Players -->
        <div class="neo-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[11px] uppercase font-mono text-slate-400 font-bold">Roblox Online</span>
                <span class="material-symbols-outlined text-[#4edea3] text-[18px]">groups</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#4edea3]" id="active-players-val-sub">--</span>
            </div>
            <span class="mt-2 text-[10px] text-slate-400 block truncate">Steal An Egg Players</span>
        </div>

        <!-- 4. Admin Double Luck -->
        <div class="neo-card p-4 flex flex-col justify-between">
            <div class="flex items-center justify-between">
                <span class="text-[11px] uppercase font-mono text-slate-400 font-bold">Admin 2x Luck</span>
                <span class="material-symbols-outlined text-[#ffb4ab] text-[18px]">bolt</span>
            </div>
            <div class="my-2 flex items-baseline gap-1.5">
                <span class="font-mono-data text-2xl sm:text-3xl font-black text-[#ffb4ab]" id="admin-countdown-val">--:--</span>
            </div>
            <span class="mt-2 text-[10px] text-slate-400 block truncate">Top of hour event</span>
        </div>
    </section>

    <!-- INTERACTIVE HATCH ODDS CALCULATOR & SIMULATOR -->
    <section id="calculator" class="neo-card p-5 sm:p-7">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-6">
            <div>
                <span class="bg-[#fbff00] text-black text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">Interactive Tool</span>
                <h2 class="font-display font-black text-2xl sm:text-3xl uppercase text-white mt-1">Hatch Odds & Luck Simulator</h2>
                <p class="text-xs text-slate-400 font-mono">Calculate real mathematical probabilities and test your luck before spending Robux/coins.</p>
            </div>
            <div class="text-right">
                <span class="text-xs font-mono text-[#00f0ff]">Formula: P = 1 - (1 - p)ⁿ</span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            <!-- Controls (Left) -->
            <div class="lg:col-span-7 space-y-5">
                <!-- 1. Select Target Tier -->
                <div>
                    <label class="block text-xs font-mono font-bold uppercase text-slate-300 mb-2">1. Select Target Rarity</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button class="calc-tier-btn active p-2.5 neo-card-sm text-center border-2 border-[#fbabff] bg-[#fbabff]/15 text-white" data-rate="0.00051" data-name="Secret" data-color="#fbabff">
                            <div class="text-xs font-display font-bold text-[#fbabff]">Secret</div>
                            <div class="text-[10px] font-mono text-slate-300">~0.051%</div>
                        </button>
                        <button class="calc-tier-btn p-2.5 neo-card-sm text-center border-2 border-black text-slate-400 hover:text-white" data-rate="0.00046" data-name="Eternal" data-color="#4edea3">
                            <div class="text-xs font-display font-bold text-[#4edea3]">Eternal</div>
                            <div class="text-[10px] font-mono text-slate-300">~0.046%</div>
                        </button>
                        <button class="calc-tier-btn p-2.5 neo-card-sm text-center border-2 border-black text-slate-400 hover:text-white" data-rate="0.00008" data-name="Divine" data-color="#00f0ff">
                            <div class="text-xs font-display font-bold text-[#00f0ff]">Divine</div>
                            <div class="text-[10px] font-mono text-slate-300">~0.008%</div>
                        </button>
                    </div>
                </div>

                <!-- 2. Luck Multiplier -->
                <div>
                    <label class="block text-xs font-mono font-bold uppercase text-slate-300 mb-2">2. Luck Boost Multiplier</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button class="calc-luck-btn active p-2 neo-card-sm text-center border-2 border-[#00f0ff] bg-[#00f0ff]/15 text-white" data-luck="1">
                            <div class="text-xs font-bold text-white">1x Normal</div>
                            <div class="text-[9px] font-mono text-slate-400">Base Luck</div>
                        </button>
                        <button class="calc-luck-btn p-2 neo-card-sm text-center border-2 border-black text-slate-400 hover:text-white" data-luck="2">
                            <div class="text-xs font-bold text-[#fbff00]">2x Admin</div>
                            <div class="text-[9px] font-mono text-slate-400">Hourly Event</div>
                        </button>
                        <button class="calc-luck-btn p-2 neo-card-sm text-center border-2 border-black text-slate-400 hover:text-white" data-luck="3">
                            <div class="text-xs font-bold text-[#ff00ff]">3x VIP Stack</div>
                            <div class="text-[9px] font-mono text-slate-400">Admin + VIP Pass</div>
                        </button>
                    </div>
                </div>

                <!-- 3. Number of Hatches -->
                <div>
                    <div class="flex justify-between items-center mb-2">
                        <label class="text-xs font-mono font-bold uppercase text-slate-300">3. Number of Hatches</label>
                        <span class="font-mono font-bold text-sm text-[#00f0ff]" id="calc-hatch-display">1,000 Hatches</span>
                    </div>
                    <input type="range" min="50" max="10000" step="50" value="1000" class="w-full h-2 bg-black rounded-none appearance-none cursor-pointer border border-black" id="calc-hatch-slider">
                    
                    <!-- Quick Presets -->
                    <div class="flex flex-wrap gap-1.5 mt-2.5">
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-slate-300 border border-black" data-val="100">100</button>
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-slate-300 border border-black" data-val="500">500</button>
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-[#00f0ff] border border-black" data-val="1000">1,000</button>
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-slate-300 border border-black" data-val="2500">2,500</button>
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-slate-300 border border-black" data-val="5000">5,000</button>
                        <button class="calc-preset-btn text-[10px] font-mono font-bold px-2.5 py-1 bg-[#181d2c] hover:bg-[#23293d] text-slate-300 border border-black" data-val="10000">10,000</button>
                    </div>
                </div>
            </div>

            <!-- Output & Simulator (Right) -->
            <div class="lg:col-span-5 bg-[#0a0d14] border-2 border-black p-5 neo-card-sm flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-[10px] font-mono uppercase text-slate-400 font-bold">Calculated Probability</span>
                        <span class="text-[10px] font-mono text-[#00f0ff] font-bold" id="calc-effective-rate">Rate: 0.051%</span>
                    </div>

                    <!-- Giant Percentage Display -->
                    <div class="text-center py-4 bg-[#131722] border-2 border-black shadow-[3px_3px_0px_#000] mb-4">
                        <div class="text-[10px] uppercase font-mono text-slate-400">Chance to Hatch ≥ 1 <span id="calc-tier-name-label" class="text-[#fbabff]">Secret</span></div>
                        <div class="font-display font-black text-4xl sm:text-5xl text-[#00f0ff] my-1" id="calc-prob-pct">40.0%</div>
                        <div class="text-[11px] font-mono text-slate-300" id="calc-avg-hatches">Average needed: 1,960 hatches</div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="w-full bg-black h-3 border border-black mb-4 overflow-hidden">
                        <div class="bg-[#00f0ff] h-full transition-all duration-300" id="calc-prob-bar" style="width: 40%"></div>
                    </div>
                </div>

                <!-- Interactive Hatch Test Roll -->
                <div class="pt-3 border-t border-black/50">
                    <div class="flex items-center justify-between mb-2 text-xs font-mono">
                        <span class="text-slate-400">Try Your Luck Right Now:</span>
                        <span id="sim-result-tag" class="font-bold text-slate-300">Ready to roll</span>
                    </div>
                    <div class="flex gap-2">
                        <button id="sim-roll-1" class="flex-1 bg-[#fbff00] hover:bg-yellow-300 text-black font-display font-black py-2.5 text-xs uppercase neo-btn">
                            Roll 1x
                        </button>
                        <button id="sim-roll-10" class="flex-1 bg-[#00f0ff] hover:bg-[#7df4ff] text-black font-display font-black py-2.5 text-xs uppercase neo-btn">
                            Roll 10x 🎲
                        </button>
                    </div>
                    <div id="sim-history" class="mt-3 min-h-[28px] text-[11px] font-mono flex items-center justify-center gap-1.5 flex-wrap">
                        <span class="text-slate-500 text-[10px]">Click Roll to simulate a live drop</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- RARITY ODDS SECTION (WITH BADGES) -->
    <section id="rarity">
        <div class="flex flex-col sm:flex-row items-start sm:items-end justify-between mb-4 gap-1">
            <div>
                <span class="text-[10px] font-black uppercase tracking-wider bg-[#fbff00] text-black px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">Verified Telemetry</span>
                <h2 class="font-display font-black text-xl sm:text-2xl uppercase text-white mt-1">Roblox Badge Odds</h2>
            </div>
            <span class="text-xs font-mono text-slate-400">Official In-Game Probabilities</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
            <!-- Secret -->
            <div class="neo-card p-4 hover:shadow-[6px_6px_0px_#000] transition-shadow cursor-pointer rarity-card-click" data-rarity="secret">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#fbabff] uppercase font-bold">Mythic Tier</span>
                        <div class="font-display text-xl font-black text-[#fbabff]">Secret Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter" alt="Secret Badge" class="w-10 h-10 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="my-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-3xl font-mono-data font-black text-white" id="secret-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Seen</span>
                        <span class="text-xs font-bold text-[#fbabff]" id="secret-last-seen-val">--</span>
                    </div>
                </div>
                <div class="pt-2.5 border-t border-black/40 flex items-center justify-between text-xs font-mono">
                    <span class="text-white font-bold bg-[#ff00ff]/20 px-2 py-0.5 border border-[#ff00ff]/40">0.051% (1 in ~1,960)</span>
                    <span class="text-slate-400 text-[10px]">31.2M+ wins</span>
                </div>
            </div>

            <!-- Eternal -->
            <div class="neo-card p-4 hover:shadow-[6px_6px_0px_#000] transition-shadow cursor-pointer rarity-card-click" data-rarity="eternal">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#4edea3] uppercase font-bold">Legendary Tier</span>
                        <div class="font-display text-xl font-black text-[#4edea3]">Eternal Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter" alt="Eternal Badge" class="w-10 h-10 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="my-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-3xl font-mono-data font-black text-white" id="eternal-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Seen</span>
                        <span class="text-xs font-bold text-[#4edea3]" id="eternal-last-seen-val">--</span>
                    </div>
                </div>
                <div class="pt-2.5 border-t border-black/40 flex items-center justify-between text-xs font-mono">
                    <span class="text-white font-bold bg-[#4edea3]/20 px-2 py-0.5 border border-[#4edea3]/40">0.046% (1 in ~2,170)</span>
                    <span class="text-slate-400 text-[10px]">19.8M+ wins</span>
                </div>
            </div>

            <!-- Divine -->
            <div class="neo-card p-4 hover:shadow-[6px_6px_0px_#000] transition-shadow cursor-pointer rarity-card-click" data-rarity="divine">
                <div class="flex items-start justify-between">
                    <div>
                        <span class="text-[10px] font-mono text-[#00f0ff] uppercase font-bold">Celestial Tier</span>
                        <div class="font-display text-xl font-black text-[#00f0ff]">Divine Rarity</div>
                    </div>
                    <img src="https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter" alt="Divine Badge" class="w-10 h-10 rounded border border-black shadow-[2px_2px_0px_#000]">
                </div>
                <div class="my-3 flex items-baseline justify-between">
                    <div>
                        <span class="text-3xl font-mono-data font-black text-white" id="divine-count-val">0</span>
                        <span class="text-xs text-slate-400 ml-1 font-mono">spawned</span>
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] uppercase font-mono text-slate-400 block">Last Seen</span>
                        <span class="text-xs font-bold text-[#00f0ff]" id="divine-last-seen-val">--</span>
                    </div>
                </div>
                <div class="pt-2.5 border-t border-black/40 flex items-center justify-between text-xs font-mono">
                    <span class="text-white font-bold bg-[#00f0ff]/20 px-2 py-0.5 border border-[#00f0ff]/40">0.008% (1 in ~12,500)</span>
                    <span class="text-slate-400 text-[10px]">1.69M+ wins</span>
                </div>
            </div>
        </div>
    </section>

    <!-- INTERACTIVE WORLDS GUIDE -->
    <section id="worlds">
        <div class="flex flex-col sm:flex-row items-start sm:items-end justify-between mb-4 gap-1">
            <div>
                <span class="text-[10px] font-black uppercase tracking-wider bg-[#00f0ff] text-black px-2 py-0.5 border border-black shadow-[2px_2px_0px_#000]">Map Intelligence</span>
                <h2 class="font-display font-black text-xl sm:text-2xl uppercase text-white mt-1">Spawn Hotspots & Worlds</h2>
            </div>
            <span class="text-xs font-mono text-slate-400">Click any world to filter live drops feed</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <!-- Abyss Ocean -->
            <div class="neo-card p-3.5 cursor-pointer hover:border-[#00f0ff] transition-all world-card-btn" data-world="Abyss Ocean">
                <div class="text-2xl mb-1">🌊</div>
                <div class="font-display font-bold text-sm text-white">Abyss Ocean</div>
                <div class="text-[10px] font-mono text-[#00f0ff] mt-0.5">Spawns: Kraken</div>
                <p class="text-[10px] text-slate-400 mt-2 line-clamp-2">Deep aquatic trench. Watch perimeter bridges.</p>
            </div>

            <!-- Snow Mountain -->
            <div class="neo-card p-3.5 cursor-pointer hover:border-[#4edea3] transition-all world-card-btn" data-world="Snow">
                <div class="text-2xl mb-1">❄️</div>
                <div class="font-display font-bold text-sm text-white">Snow Summit</div>
                <div class="text-[10px] font-mono text-[#4edea3] mt-0.5">Yeti & Ice Dragon</div>
                <p class="text-[10px] text-slate-400 mt-2 line-clamp-2">Frozen ridge. Ice Dragon spawns near peak.</p>
            </div>

            <!-- Prehistoric Island -->
            <div class="neo-card p-3.5 cursor-pointer hover:border-[#fbff00] transition-all world-card-btn" data-world="Prehistoric">
                <div class="text-2xl mb-1">🌋</div>
                <div class="font-display font-bold text-sm text-white">Prehistoric</div>
                <div class="text-[10px] font-mono text-[#fbff00] mt-0.5">TRex & Tralaledon</div>
                <p class="text-[10px] text-slate-400 mt-2 line-clamp-2">Volcano caves. High-traffic ambush zone.</p>
            </div>

            <!-- Titan Temple -->
            <div class="neo-card p-3.5 cursor-pointer hover:border-[#ff00ff] transition-all world-card-btn" data-world="Titan Temple">
                <div class="text-2xl mb-1">🏛️</div>
                <div class="font-display font-bold text-sm text-white">Titan Temple</div>
                <div class="text-[10px] font-mono text-[#ff00ff] mt-0.5">Mutant Shark</div>
                <p class="text-[10px] text-slate-400 mt-2 line-clamp-2">Colosseum courtyard. Guard inner altar.</p>
            </div>

            <!-- Cosmic Void -->
            <div class="neo-card p-3.5 cursor-pointer hover:border-[#fbabff] transition-all world-card-btn" data-world="Cosmic">
                <div class="text-2xl mb-1">🌌</div>
                <div class="font-display font-bold text-sm text-white">Cosmic Realm</div>
                <div class="text-[10px] font-mono text-[#fbabff] mt-0.5">Cosmic Skeleton</div>
                <p class="text-[10px] text-slate-400 mt-2 line-clamp-2">Zero-g void. Boss drops in center ring.</p>
            </div>
        </div>
    </section>

    <!-- LIVE DROPS FEED SECTION (SEARCH, FILTERS, SHARE, INTEL) -->
    <section id="drops">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
            <div>
                <h3 class="font-display font-black text-xl sm:text-2xl uppercase text-white">Live Drops Feed</h3>
                <p class="text-xs text-slate-400 font-mono">Real-time spawn feed with 10-minute duplicate prevention</p>
            </div>

            <!-- Search & Filters Container -->
            <div class="w-full sm:w-auto flex flex-col sm:flex-row gap-2">
                <!-- Search input -->
                <div class="relative flex-1 sm:w-48">
                    <input type="text" id="drop-search-input" placeholder="Search egg or world..." class="w-full bg-[#131722] text-xs font-mono text-white px-3 py-1.5 pl-8 border-2 border-black neo-card-sm focus:outline-none focus:border-[#00f0ff]">
                    <span class="material-symbols-outlined text-[16px] text-slate-400 absolute left-2 top-2">search</span>
                </div>

                <!-- Filter Buttons -->
                <div class="flex items-center gap-1 bg-[#131722] p-1 neo-card-sm overflow-x-auto">
                    <button class="filter-btn active bg-[#00f0ff] text-black font-black uppercase text-xs px-3 py-1 border border-black shrink-0" data-filter="all">All</button>
                    <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-xs px-3 py-1 shrink-0" data-filter="secret">Secret</button>
                    <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-xs px-3 py-1 shrink-0" data-filter="eternal">Eternal</button>
                    <button class="filter-btn text-slate-400 hover:text-white font-bold uppercase text-xs px-3 py-1 shrink-0" data-filter="divine">Divine</button>
                </div>
            </div>
        </div>

        <!-- Active Filter indicator if world filtered -->
        <div id="active-world-filter-tag" class="hidden mb-3 items-center gap-2 bg-[#00f0ff]/10 border border-[#00f0ff] px-3 py-1 text-xs font-mono text-[#00f0ff] w-max">
            <span>Filtering world: <b id="active-world-name"></b></span>
            <button id="clear-world-filter" class="text-white hover:text-red-400 font-bold ml-2">✕ Clear</button>
        </div>

        <!-- Desktop Table View (>= 640px) -->
        <div class="hidden sm:block neo-card overflow-x-auto">
            <table class="w-full text-left font-mono-data text-xs">
                <thead class="bg-[#0a0d14] border-b-2 border-black uppercase text-slate-300">
                    <tr>
                        <th class="p-3 border-r-2 border-black font-black">Egg Target (Click For Intel)</th>
                        <th class="p-3 border-r-2 border-black font-black">Rarity</th>
                        <th class="p-3 border-r-2 border-black font-black">Location</th>
                        <th class="p-3 border-r-2 border-black font-black">Timestamp</th>
                        <th class="p-3 text-right font-black">Quick Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y-2 divide-black" id="drops-table-body">
                    <tr>
                        <td colspan="5" class="py-8 text-center text-slate-400 font-mono">Connecting to live radar feed...</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Mobile Card View (< 640px) -->
        <div class="block sm:hidden space-y-2.5" id="drops-mobile-cards">
            <div class="p-4 neo-card text-center text-slate-400 font-mono text-xs">Connecting to live radar feed...</div>
        </div>
    </section>

</main>

<!-- STICKY FLOATING MOBILE BAR (< 640px) -->
<div class="block sm:hidden fixed bottom-0 left-0 right-0 z-30 bg-[#0a0d14]/95 backdrop-blur-md border-t-2 border-black p-2.5 shadow-[0_-4px_10px_rgba(0,0,0,0.5)]">
    <div class="flex items-center justify-between gap-2">
        <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[#00f0ff] animate-ping"></span>
            <div>
                <div class="text-[9px] uppercase font-mono text-slate-400">Wave ETA</div>
                <div class="font-mono font-black text-sm text-[#00f0ff]" id="mobile-float-wave">--:--</div>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button id="mobile-sound-btn" class="bg-[#181d2c] text-white p-2 neo-btn text-xs" title="Toggle Sound">
                <span class="material-symbols-outlined text-[16px] text-[#00f0ff]">volume_up</span>
            </button>
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] text-black font-display font-black text-xs uppercase px-4 py-2 neo-btn flex items-center gap-1 no-underline">
                <span>Play Roblox</span>
                <span class="material-symbols-outlined text-[14px]">bolt</span>
            </a>
        </div>
    </div>
</div>

<!-- EGG INTELLIGENCE DOSSIER MODAL -->
<div id="egg-modal" class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop hidden">
    <div class="neo-card bg-[#131722] max-w-md w-full p-5 sm:p-6 relative">
        <!-- Close button -->
        <button id="modal-close-btn" class="absolute top-4 right-4 bg-[#181d2c] hover:bg-red-500 hover:text-white text-slate-400 w-8 h-8 flex items-center justify-center border border-black font-bold">
            ✕
        </button>

        <div class="flex items-center gap-3 mb-4">
            <img id="modal-egg-img" src="" alt="" class="w-14 h-14 rounded border-2 border-black shadow-[3px_3px_0px_#000]">
            <div>
                <span id="modal-egg-tier" class="px-2 py-0.5 uppercase text-[10px] font-black border"></span>
                <h3 id="modal-egg-name" class="font-display font-black text-2xl uppercase text-white mt-1 leading-none"></h3>
            </div>
        </div>

        <div class="space-y-3 font-mono text-xs text-slate-300">
            <div class="bg-[#0a0d14] border border-black p-3 space-y-1.5">
                <div class="flex justify-between">
                    <span class="text-slate-400">Primary World:</span>
                    <span id="modal-egg-world" class="text-white font-bold"></span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-400">Official Odds:</span>
                    <span id="modal-egg-odds" class="text-[#00f0ff] font-bold"></span>
                </div>
                <div class="flex justify-between">
                    <span class="text-slate-400">Badge Completions:</span>
                    <span id="modal-egg-badge-wins" class="text-[#4edea3] font-bold"></span>
                </div>
            </div>

            <div>
                <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Tactical Camping Advice:</span>
                <p id="modal-egg-tips" class="text-[11px] leading-relaxed bg-[#181d2c] p-2.5 border border-black text-slate-200"></p>
            </div>
        </div>

        <div class="flex gap-2 mt-5">
            <button id="modal-copy-btn" class="flex-1 bg-[#fbff00] hover:bg-yellow-300 text-black font-display font-black py-2 text-xs uppercase neo-btn flex items-center justify-center gap-1">
                <span class="material-symbols-outlined text-[16px]">content_copy</span>
                <span>Copy Alert</span>
            </button>
            <a id="modal-play-link" href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="flex-1 bg-[#00f0ff] hover:bg-[#7df4ff] text-black font-display font-black py-2 text-xs uppercase neo-btn flex items-center justify-center gap-1 no-underline">
                <span>Play Roblox</span>
                <span class="material-symbols-outlined text-[14px]">open_in_new</span>
            </a>
        </div>
    </div>
</div>

<!-- FOOTER -->
<footer class="bg-[#0a0d14] border-t-2 border-black py-8 px-4 sm:px-6 mt-auto">
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
            <a href="https://discord.gg/Jmvam6Ktgm" target="_blank" rel="noopener noreferrer" class="text-[#5865f2] hover:text-white uppercase font-bold">Discord</a>
            <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener noreferrer" class="bg-[#00f0ff] text-black px-3 py-1 neo-btn font-black uppercase text-xs no-underline">Play Roblox ↗</a>
        </div>
    </div>
</footer>

<!-- COMPLETE CLIENT LOGIC -->
<script>
document.addEventListener("DOMContentLoaded", () => {
    // ── 1. Toast Notification Helper ──
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toast-msg");
    function showToast(msg) {
        if (!toast) return;
        toastMsg.textContent = msg;
        toast.classList.remove("opacity-0", "pointer-events-none", "-translate-y-12");
        toast.classList.add("opacity-100", "translate-y-0");
        setTimeout(() => {
            toast.classList.remove("opacity-100", "translate-y-0");
            toast.classList.add("opacity-0", "pointer-events-none", "-translate-y-12");
        }, 2200);
    }

    // ── 2. Audio Engine ──
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

    function toggleSound() {
        soundEnabled = !soundEnabled;
        const icon = document.querySelector("#sound-toggle .material-symbols-outlined");
        const label = document.getElementById("sound-toggle-label");
        if (label) label.textContent = soundEnabled ? "Sound" : "Muted";
        if (icon) {
            icon.textContent = soundEnabled ? "volume_up" : "volume_off";
            icon.style.fontVariationSettings = soundEnabled ? "'FILL' 1" : "'FILL' 0";
        }
        const mIcon = document.querySelector("#mobile-sound-btn .material-symbols-outlined");
        if (mIcon) {
            mIcon.textContent = soundEnabled ? "volume_up" : "volume_off";
        }
        showToast(soundEnabled ? "🔊 Sound alerts enabled" : "🔇 Sound alerts muted");
        if (soundEnabled) playChime(true);
    }

    const soundBtn = document.getElementById("sound-toggle");
    if (soundBtn) soundBtn.addEventListener("click", toggleSound);
    const mSoundBtn = document.getElementById("mobile-sound-btn");
    if (mSoundBtn) mSoundBtn.addEventListener("click", toggleSound);

    // ── 3. Formatting Helpers ──
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

    // ── 4. Egg Intelligence Database ──
    const eggDatabase = {
        "Kitsune": {
            tier: "divine",
            odds: "0.004% (1 in 25,000)",
            badgeWins: "1.76M+",
            world: "Cherry Blossom",
            tips: "Top-tier celestial Divine pet ($1.8B/sec base income). Highly valued across high-level trading servers.",
            icon: "https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter"
        },
        "Nightflame": {
            tier: "divine",
            odds: "0.004% (1 in 25,000)",
            badgeWins: "1.76M+",
            world: "Volcano",
            tips: "Supreme highest-earning Divine pet ($3B/sec base income). The undisputed crown jewel in Steal An Egg.",
            icon: "https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter"
        },
        "Unicorn": {
            tier: "divine",
            odds: "0.004% (1 in 25,000)",
            badgeWins: "1.76M+",
            world: "Forest",
            tips: "Ultra-rare Divine egg ($1B/sec base income). Spawns with a bright celestial aura.",
            icon: "https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter"
        },
        "Phoenix": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Volcano",
            tips: "Fiery Eternal pet. Guarded by the Volcano beast. Train speed above 850,000 to escape safely.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Eternal Lunar Dragon": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Cosmic",
            tips: "Mythic lunar serpent in the Cosmic realm. High trading liquidity and heavy weight roll potential.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Oni Tiger": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Cherry Blossom",
            tips: "S-Tier Eternal pet in the Cherry Blossom biome. High passive income boost.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Mosasaurus": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Prehistoric",
            tips: "Prehistoric aquatic apex predator egg. High multiplier with Spirit Bloom mutation.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Ice Dragon": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Snow",
            tips: "Legendary spawn at the Snow biome peak. Requires minimum 170,000 Speed threshold.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Lava Dragon": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Volcano",
            tips: "Elite molten beast in the Volcano area. Requires 700,000 Speed threshold.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Gorilla King": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Jungle",
            tips: "Jungle monarch egg with massive cash-per-second output. Requires 50,000 Speed.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "El Maja": {
            tier: "eternal",
            odds: "0.039% (1 in ~2,560)",
            badgeWins: "20.3M+",
            world: "Desert",
            tips: "Desert guardian Eternal pet. Requires 10,000 Speed to outrun.",
            icon: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter"
        },
        "Cerberus": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Volcano",
            tips: "Three-headed underworld hound egg in Volcano biome. Instant value in trading.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Mutant Shark": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Titan Temple",
            tips: "High-demand Secret pet from the Titan Temple guardian.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Stag": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Forest",
            tips: "Forest Secret egg with rapid early-game progression acceleration.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Kraken": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Abyss Ocean",
            tips: "Abyss Ocean guardian nest egg. Requires 2,500,000 Speed to outrun the tentacles.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Tralaledon": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Prehistoric",
            tips: "Prehistoric Secret beast egg. High trade liquidity.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Cosmic Dragon": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Cosmic",
            tips: "Cosmic realm Secret egg with glowing star aura.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Cosmic Skeleton Boss": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Cosmic",
            tips: "Boss tier Secret drop in Cosmic realm.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Yeti": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Snow",
            tips: "Snow biome Secret pet. Outrun with speed coils or high treadmill stats.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "TRex": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Prehistoric",
            tips: "Prehistoric predator egg. Great weight roll scaling.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        },
        "Snake King": {
            tier: "secret",
            odds: "0.050% (1 in ~2,000)",
            badgeWins: "31.8M+",
            world: "Desert",
            tips: "Desert mythical serpent egg. High multiplier scaling.",
            icon: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter"
        }
    };

    const badgeIcons = {
        secret: "https://tr.rbxcdn.com/180DAY-66ba84cc7ac5060813a2baa96a92073b/150/150/Image/Png/noFilter",
        eternal: "https://tr.rbxcdn.com/180DAY-b7e0a52efc32612abd8015e2d3e33ead/150/150/Image/Png/noFilter",
        divine: "https://tr.rbxcdn.com/180DAY-712ad5642dc26dee5c980788e86977d8/150/150/Image/Png/noFilter"
    };

    const rarityStyles = {
        divine: { text: "text-[#00f0ff]", badge: "border-[#00f0ff] text-[#00f0ff] bg-[#00f0ff]/10" },
        eternal: { text: "text-[#4edea3]", badge: "border-[#4edea3] text-[#4edea3] bg-[#4edea3]/10" },
        secret: { text: "text-[#fbabff]", badge: "border-[#fbabff] text-[#fbabff] bg-[#fbabff]/10" }
    };

    // ── 5. Egg Intel Modal ──
    const modal = document.getElementById("egg-modal");
    const modalClose = document.getElementById("modal-close-btn");
    let currentModalEgg = null;

    function openEggModal(eggName, fallbackLocation, fallbackRarity) {
        const info = eggDatabase[eggName] || {
            tier: (fallbackRarity || "secret").toLowerCase(),
            odds: fallbackRarity === "divine" ? "0.008% (1 in ~12,500)" : fallbackRarity === "eternal" ? "0.046% (1 in ~2,170)" : "0.051% (1 in ~1,960)",
            badgeWins: fallbackRarity === "divine" ? "1.69M+" : fallbackRarity === "eternal" ? "19.8M+" : "31.2M+",
            world: fallbackLocation || "Active World",
            tips: "Active rare spawn tracked live by EggStock. Check designated spawn points and look for glowing beacons.",
            icon: badgeIcons[(fallbackRarity || "secret").toLowerCase()] || badgeIcons.secret
        };

        currentModalEgg = { name: eggName, ...info };

        document.getElementById("modal-egg-name").textContent = eggName;
        document.getElementById("modal-egg-img").src = info.icon;
        const tierEl = document.getElementById("modal-egg-tier");
        tierEl.textContent = info.tier;
        const st = rarityStyles[info.tier] || rarityStyles.secret;
        tierEl.className = `px-2 py-0.5 uppercase text-[10px] font-black border ${st.badge}`;
        document.getElementById("modal-egg-world").textContent = info.world;
        document.getElementById("modal-egg-odds").textContent = info.odds;
        document.getElementById("modal-egg-badge-wins").textContent = info.badgeWins;
        document.getElementById("modal-egg-tips").textContent = info.tips;

        modal.classList.remove("hidden");
    }

    if (modalClose) modalClose.addEventListener("click", () => modal.classList.add("hidden"));
    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.add("hidden");
        });
    }
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && modal) modal.classList.add("hidden");
    });

    // Copy alert from modal
    const modalCopyBtn = document.getElementById("modal-copy-btn");
    if (modalCopyBtn) {
        modalCopyBtn.addEventListener("click", () => {
            if (!currentModalEgg) return;
            const text = `🔥 [EggStock] ${currentModalEgg.name} (${currentModalEgg.tier.toUpperCase()}) active at ${currentModalEgg.world}! Track live: https://eggstock.xyz`;
            navigator.clipboard.writeText(text).then(() => {
                showToast("Copied alert to clipboard!");
            });
        });
    }

    // Click on Hero Showcase card opens modal
    const heroCardTrigger = document.getElementById("hero-card-trigger");
    if (heroCardTrigger) {
        heroCardTrigger.addEventListener("click", () => {
            const eggName = document.getElementById("featured-egg-name")?.textContent || "Kraken";
            if (eggName !== "Waiting For Spawn...") {
                openEggModal(eggName);
            }
        });
    }

    // ── 6. Smooth 1-Second Timer Engine ──
    let localWaveSec = null;
    let localIntervalSec = 600;

    function renderWaveUI(sec, interval) {
        const timeStr = formatWave(sec);
        const timer1 = document.getElementById("countdown-timer");
        if (timer1) timer1.textContent = timeStr;
        const timer2 = document.getElementById("countdown-timer-sub");
        if (timer2) timer2.textContent = timeStr;
        const timer3 = document.getElementById("featured-egg-timer");
        if (timer3) timer3.textContent = timeStr;
        const timer4 = document.getElementById("mobile-float-wave");
        if (timer4) timer4.textContent = timeStr;

        const bar = document.getElementById("countdown-bar");
        if (bar && sec !== null && !isNaN(sec) && interval > 0) {
            const pct = Math.min(100, Math.max(5, ((interval - sec) / interval) * 100));
            bar.style.width = pct + "%";
        }
    }

    setInterval(() => {
        // Wave countdown
        if (localWaveSec !== null && localWaveSec > 0) {
            localWaveSec--;
            renderWaveUI(localWaveSec, localIntervalSec);
        } else if (localWaveSec === 0) {
            localWaveSec = localIntervalSec;
            renderWaveUI(localWaveSec, localIntervalSec);
        }

        // Admin event countdown (top of hour)
        const now = new Date();
        const nextHour = new Date(now);
        nextHour.setHours(now.getHours() + 1, 0, 0, 0);
        const adminDiff = Math.max(0, Math.floor((nextHour - now) / 1000));
        const timeStr = formatWave(adminDiff);
        const adminEl = document.getElementById("admin-countdown-val");
        if (adminEl) adminEl.textContent = timeStr;
        const heroAdmin = document.getElementById("hero-admin-countdown");
        if (heroAdmin) heroAdmin.textContent = timeStr;
    }, 1000);

    // ── 7. Interactive Hatch Calculator Logic ──
    let calcRate = 0.00051; // Secret
    let calcLuck = 1;
    let calcHatches = 1000;
    let calcTierName = "Secret";
    let calcTierColor = "#fbabff";

    function updateCalculator() {
        const effectiveP = Math.min(0.9999, calcRate * calcLuck);
        // Probability of at least 1 hit: 1 - (1 - p)^n
        const prob = 1 - Math.pow(1 - effectiveP, calcHatches);
        const pctStr = (prob * 100).toFixed(2) + "%";
        const avgNeeded = Math.round(1 / effectiveP);

        document.getElementById("calc-prob-pct").textContent = pctStr;
        document.getElementById("calc-avg-hatches").textContent = `Average needed: ${avgNeeded.toLocaleString()} hatches`;
        document.getElementById("calc-effective-rate").textContent = `Rate: ${(effectiveP * 100).toFixed(4)}%`;
        document.getElementById("calc-hatch-display").textContent = `${Number(calcHatches).toLocaleString()} Hatches`;
        
        const tierLabel = document.getElementById("calc-tier-name-label");
        if (tierLabel) {
            tierLabel.textContent = calcTierName;
            tierLabel.style.color = calcTierColor;
        }

        const probBar = document.getElementById("calc-prob-bar");
        if (probBar) {
            probBar.style.width = Math.min(100, Math.max(3, prob * 100)) + "%";
        }
    }

    // Tier buttons
    document.querySelectorAll(".calc-tier-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".calc-tier-btn").forEach(b => {
                b.classList.remove("active", "border-[#fbabff]", "border-[#4edea3]", "border-[#00f0ff]", "bg-[#fbabff]/15", "bg-[#4edea3]/15", "bg-[#00f0ff]/15");
                b.classList.add("border-black", "text-slate-400");
            });
            btn.classList.add("active");
            btn.classList.remove("border-black", "text-slate-400");
            const color = btn.dataset.color;
            btn.style.borderColor = color;
            btn.style.backgroundColor = `${color}25`;
            btn.classList.add("text-white");
            calcRate = parseFloat(btn.dataset.rate);
            calcTierName = btn.dataset.name;
            calcTierColor = color;
            updateCalculator();
        });
    });

    // Luck buttons
    document.querySelectorAll(".calc-luck-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".calc-luck-btn").forEach(b => {
                b.classList.remove("active", "border-[#00f0ff]", "bg-[#00f0ff]/15");
                b.classList.add("border-black", "text-slate-400");
            });
            btn.classList.add("active", "border-[#00f0ff]", "bg-[#00f0ff]/15", "text-white");
            btn.classList.remove("border-black", "text-slate-400");
            calcLuck = parseFloat(btn.dataset.luck);
            updateCalculator();
        });
    });

    // Slider
    const hatchSlider = document.getElementById("calc-hatch-slider");
    if (hatchSlider) {
        hatchSlider.addEventListener("input", (e) => {
            calcHatches = parseInt(e.target.value);
            updateCalculator();
        });
    }

    // Presets
    document.querySelectorAll(".calc-preset-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            calcHatches = parseInt(btn.dataset.val);
            if (hatchSlider) hatchSlider.value = calcHatches;
            updateCalculator();
        });
    });

    // ── 8. Hatch Simulator (Roll Buttons) ──
    function simulateRoll(rolls = 1) {
        const effectiveP = Math.min(0.9999, calcRate * calcLuck);
        const historyEl = document.getElementById("sim-history");
        const tagEl = document.getElementById("sim-result-tag");
        let hits = 0;

        for (let i = 0; i < rolls; i++) {
            if (Math.random() < effectiveP) hits++;
        }

        if (hits > 0) {
            playChime(true);
            tagEl.textContent = `🎉 JACKPOT! Hatched ${hits}x ${calcTierName}!`;
            tagEl.className = "font-bold text-[#00f0ff] animate-pulse";
            showToast(`🔥 JACKPOT! You rolled ${hits}x ${calcTierName}!`);
            if (historyEl) {
                historyEl.innerHTML = `<span class="bg-[#00f0ff] text-black px-2 py-0.5 font-black border border-black animate-bounce">★ HIT ${calcTierName.toUpperCase()}! (${hits}/${rolls})</span>`;
            }
        } else {
            tagEl.textContent = `Missed (Rolled ${rolls}x)`;
            tagEl.className = "font-bold text-slate-400";
            if (historyEl) {
                historyEl.innerHTML = `<span class="text-slate-400">Rolled ${rolls}x eggs: 0 ${calcTierName} found. Try again!</span>`;
            }
        }
    }

    document.getElementById("sim-roll-1")?.addEventListener("click", () => simulateRoll(1));
    document.getElementById("sim-roll-10")?.addEventListener("click", () => simulateRoll(10));

    // ── 9. Live Feed Filter & Search ──
    let currentFilter = "all";
    let currentWorldFilter = null;
    let searchQuery = "";
    let lastData = null;

    // Rarity filter buttons
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".filter-btn").forEach(b => {
                b.classList.remove("active", "bg-[#00f0ff]", "text-black", "font-black");
                b.classList.add("text-slate-400");
            });
            btn.classList.add("active", "bg-[#00f0ff]", "text-black", "font-black");
            btn.classList.remove("text-slate-400");
            currentFilter = btn.dataset.filter || "all";
            if (lastData) renderFeed(lastData.recent_drops || []);
        });
    });

    // Search input
    document.getElementById("drop-search-input")?.addEventListener("input", (e) => {
        searchQuery = (e.target.value || "").trim().toLowerCase();
        if (lastData) renderFeed(lastData.recent_drops || []);
    });

    // World card filter triggers
    document.querySelectorAll(".world-card-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const world = btn.dataset.world;
            currentWorldFilter = world;
            const tag = document.getElementById("active-world-filter-tag");
            const wName = document.getElementById("active-world-name");
            if (tag && wName) {
                wName.textContent = world;
                tag.classList.remove("hidden");
                tag.classList.add("flex");
            }
            // Scroll smoothly to feed
            document.getElementById("drops")?.scrollIntoView({ behavior: "smooth" });
            if (lastData) renderFeed(lastData.recent_drops || []);
        });
    });

    // Clear world filter
    document.getElementById("clear-world-filter")?.addEventListener("click", () => {
        currentWorldFilter = null;
        const tag = document.getElementById("active-world-filter-tag");
        if (tag) {
            tag.classList.add("hidden");
            tag.classList.remove("flex");
        }
        if (lastData) renderFeed(lastData.recent_drops || []);
    });

    // Rarity card click triggers filter
    document.querySelectorAll(".rarity-card-click").forEach(card => {
        card.addEventListener("click", () => {
            const r = card.dataset.rarity;
            const targetBtn = document.querySelector(`.filter-btn[data-filter="${r}"]`);
            if (targetBtn) targetBtn.click();
            document.getElementById("drops")?.scrollIntoView({ behavior: "smooth" });
        });
    });

    // ── 10. Feed Renderer (Table + Mobile Cards + Click-to-Modal + Share) ──
    function renderFeed(drops) {
        const tbody = document.getElementById("drops-table-body");
        const mCards = document.getElementById("drops-mobile-cards");

        // Apply filters & search
        const filtered = drops.filter(d => {
            const r = (d.rarity || "").toLowerCase();
            const egg = (d.egg || "").toLowerCase();
            const loc = (d.location || "").toLowerCase();

            // Rarity filter
            if (currentFilter !== "all" && r !== currentFilter) return false;
            // World filter
            if (currentWorldFilter && !loc.includes(currentWorldFilter.toLowerCase())) return false;
            // Search query
            if (searchQuery && !egg.includes(searchQuery) && !loc.includes(searchQuery) && !r.includes(searchQuery)) return false;

            return true;
        });

        // 10-minute duplicate prevention
        const deduped = [];
        const seen = {};
        for (const d of filtered) {
            const key = `${(d.egg || "").toLowerCase()}|${(d.location || "").toLowerCase()}|${(d.rarity || "").toLowerCase()}`;
            const ts = d.time ? new Date(d.time).getTime() : 0;
            const lastTs = seen[key] || 0;
            if (lastTs && Math.abs(ts - lastTs) < 600000) continue;
            seen[key] = ts;
            deduped.push(d);
        }

        if (deduped.length === 0) {
            if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="py-8 text-center text-slate-400 font-mono">No drops matching filter</td></tr>';
            if (mCards) mCards.innerHTML = '<div class="p-4 neo-card text-center text-slate-400 font-mono text-xs">No drops matching filter</div>';
            return;
        }

        // Desktop Table
        if (tbody) {
            tbody.innerHTML = deduped.map(d => {
                const r = (d.rarity || "").toLowerCase();
                const st = rarityStyles[r] || { text: "text-white", badge: "border-white text-white" };
                const icon = badgeIcons[r] || "";
                const timeStr = formatClock(d.time);
                const eggSafe = (d.egg || "Unknown").replace(/"/g, '&quot;');
                const locSafe = (d.location || "World").replace(/"/g, '&quot;');

                return `
                    <tr class="hover:bg-[#1a1f2e] transition-colors">
                        <td class="p-3 border-r-2 border-black font-bold text-white cursor-pointer hover:text-[#00f0ff] feed-egg-trigger" data-egg="${eggSafe}" data-loc="${locSafe}" data-rarity="${r}">
                            <div class="flex items-center gap-2.5">
                                ${icon ? `<img src="${icon}" class="w-6 h-6 rounded border border-black shrink-0" alt="">` : ''}
                                <span class="underline decoration-dotted decoration-slate-500">${d.egg || "Unknown"}</span>
                                <span class="text-[10px] text-slate-400">🔍</span>
                            </div>
                        </td>
                        <td class="p-3 border-r-2 border-black">
                            <span class="px-2 py-0.5 uppercase text-[10px] font-black border ${st.badge}">
                                ${d.rarity || "--"}
                            </span>
                        </td>
                        <td class="p-3 border-r-2 border-black text-slate-300 font-sans">
                            ${d.location || "World"}
                        </td>
                        <td class="p-3 border-r-2 border-black font-mono-data text-white text-[11px] whitespace-nowrap">
                            ${timeStr}
                        </td>
                        <td class="p-3 text-right">
                            <div class="flex items-center justify-end gap-1.5">
                                <button class="feed-share-btn bg-[#181d2c] hover:bg-slate-700 text-slate-300 px-2.5 py-1 text-xs font-mono font-bold border border-black neo-btn" data-egg="${eggSafe}" data-loc="${locSafe}" data-rarity="${r}" title="Copy or Share Alert">
                                    📋 Share
                                </button>
                                <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] hover:bg-white text-black px-3 py-1 text-xs font-black uppercase neo-btn inline-block no-underline">
                                    Play ↗
                                </a>
                            </div>
                        </td>
                    </tr>
                `;
            }).join("");
        }

        // Mobile Cards
        if (mCards) {
            mCards.innerHTML = deduped.map(d => {
                const r = (d.rarity || "").toLowerCase();
                const st = rarityStyles[r] || { text: "text-white", badge: "border-white text-white" };
                const icon = badgeIcons[r] || "";
                const timeStr = formatClock(d.time);
                const eggSafe = (d.egg || "Unknown").replace(/"/g, '&quot;');
                const locSafe = (d.location || "World").replace(/"/g, '&quot;');

                return `
                    <div class="neo-card p-3.5 flex items-center justify-between gap-3">
                        <div class="flex items-center gap-3 min-w-0 cursor-pointer feed-egg-trigger" data-egg="${eggSafe}" data-loc="${locSafe}" data-rarity="${r}">
                            ${icon ? `<img src="${icon}" class="w-10 h-10 rounded border border-black shrink-0" alt="">` : ''}
                            <div class="min-w-0">
                                <div class="font-display font-bold text-sm text-white truncate flex items-center gap-1">
                                    <span>${d.egg || "Unknown"}</span>
                                    <span class="text-[10px] text-[#00f0ff]">🔍</span>
                                </div>
                                <div class="flex items-center gap-1.5 mt-0.5">
                                    <span class="px-1.5 py-0.2 uppercase text-[9px] font-black border ${st.badge}">
                                        ${d.rarity || "--"}
                                    </span>
                                    <span class="text-[11px] font-mono text-slate-400 truncate">📍 ${d.location || "World"}</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right shrink-0 flex flex-col items-end gap-1">
                            <div class="text-[10px] font-mono text-slate-400">${timeStr}</div>
                            <div class="flex items-center gap-1">
                                <button class="feed-share-btn bg-[#181d2c] text-slate-300 px-2 py-1 text-[10px] font-bold neo-btn" data-egg="${eggSafe}" data-loc="${locSafe}" data-rarity="${r}">
                                    Share
                                </button>
                                <a href="https://www.roblox.com/games/107778070777162" target="_blank" rel="noopener" class="bg-[#00f0ff] text-black px-2.5 py-1 text-[10px] font-black uppercase neo-btn inline-block no-underline">
                                    Play ↗
                                </a>
                            </div>
                        </div>
                    </div>
                `;
            }).join("");
        }

        // Wire click-to-modal on egg names
        document.querySelectorAll(".feed-egg-trigger").forEach(el => {
            el.addEventListener("click", () => {
                openEggModal(el.dataset.egg, el.dataset.loc, el.dataset.rarity);
            });
        });

        // Wire share/copy alert buttons
        document.querySelectorAll(".feed-share-btn").forEach(el => {
            el.addEventListener("click", (e) => {
                e.stopPropagation();
                const egg = el.dataset.egg;
                const loc = el.dataset.loc;
                const r = (el.dataset.rarity || "rare").toUpperCase();
                const text = `🔥 [EggStock] ${egg} (${r}) just dropped at ${loc}! Track live at https://eggstock.xyz`;

                if (navigator.share && /mobile|android|iphone/i.test(navigator.userAgent)) {
                    navigator.share({
                        title: "EggStock Spawn Alert",
                        text: text,
                        url: "https://eggstock.xyz"
                    }).catch(() => {});
                } else {
                    navigator.clipboard.writeText(text).then(() => {
                        showToast(`Copied ${egg} drop alert!`);
                    });
                }
            });
        });
    }

    // ── 11. Polling & Data Engine ──
    async function poll() {
        try {
            const res = await fetch("/api/status");
            if (!res.ok) return;
            const data = await res.json();
            lastData = data;

            // 1. Sync Wave Prediction smoothly
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

            // 3. Real Active Roblox Players
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

            // Audio notification
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

            // 5. Render Feed
            renderFeed(data.recent_drops || []);

        } catch (err) {
            console.error("Radar poll error:", err);
        }
    }

    // Initialize Calculator and Polling
    updateCalculator();
    poll();
    setInterval(poll, 3000);
});
</script>
</body>
</html>
'''

with open('website/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated feature-complete, interactive, mobile-optimized website/index.html!")
