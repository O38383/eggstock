/**
 * EggStock.xyz - Site-Wide Discord OAuth Modal
 * High-Converting Session Dwell Model:
 *  - Triggers after 30s of active session dwell time across the entire site.
 *  - Primary CTA connects Discord OAuth (/api/auth/discord/login) for 1-Click Server Join.
 *  - Strict 1x per browsing session limit (stored in sessionStorage).
 *  - Preserves dwell progress seamlessly across page navigation (/codes -> /tier-list -> /).
 *  - Permanent disable option ("Don't show again" or CTA click) saved in localStorage.
 *  - COMPLETELY SUPPRESSED for logged-in users (/api/auth/me or ?auth=success).
 */
// Global test helpers defined immediately
window.__showDiscordModal = function() {
    let m = document.getElementById("discord-modal");
    if (m) {
        m.classList.remove("hidden");
        m.style.display = "flex";
        console.log("[EggStock Discord] Modal opened via __showDiscordModal()");
    }
};

window.__resetDiscordModal = function() {
    try {
        localStorage.removeItem("es_discord_popup_disabled");
        localStorage.removeItem("es_discord_joined");
        sessionStorage.removeItem("es_discord_session_seen");
        sessionStorage.removeItem("es_session_dwell_start");
        console.log("[EggStock Discord] Storage reset successfully! Reload or wait 30s.");
    } catch (e) {}
};

window.__testDiscordModal = window.__showDiscordModal;

(function initSiteWideDiscordModal() {
    const STORAGE_KEY_DISABLED = "es_discord_popup_disabled";
    const SESSION_KEY_SEEN = "es_discord_session_seen";
    const SESSION_KEY_START = "es_session_dwell_start";
    const STORAGE_KEY_JOINED = "es_discord_joined";
    const DWELL_DELAY_MS = 25000; // 25 seconds active dwell time

    // 0. If user just completed OAuth login (?auth=success), permanently disable and exit
    if (window.location.search.includes("auth=success")) {
        try {
            localStorage.setItem(STORAGE_KEY_DISABLED, "true");
        } catch (e) {}
        console.log("[EggStock Discord] OAuth login successful. Popup permanently disabled.");
        return;
    }

    // 1. If already joined or permanently disabled, never show
    if (localStorage.getItem(STORAGE_KEY_JOINED) === "true") {
        console.log("[EggStock Discord] User already joined Discord. Modal suppressed.");
        return;
    }
    if (localStorage.getItem(STORAGE_KEY_DISABLED) === "true") {
        console.log("[EggStock Discord] Popup permanently disabled on this browser.");
        return;
    }

    // 2. If already closed, dismissed, or shown in the current browsing session, exit immediately
    if (sessionStorage.getItem(SESSION_KEY_SEEN) === "true") {
        console.log("[EggStock Discord] Popup already shown/closed in this session.");
        return;
    }

    // 3. Asynchronously check if user is already authenticated
    try {
        fetch("/api/auth/me")
            .then(res => res.json())
            .then(data => {
                if (data && data.authenticated) {
                    localStorage.setItem(STORAGE_KEY_DISABLED, "true");
                    const existingModal = document.getElementById("discord-modal");
                    if (existingModal) {
                        existingModal.classList.add("hidden");
                        existingModal.style.display = "none";
                    }
                    console.log("[EggStock Discord] User is logged in. Popup permanently suppressed.");
                }
            })
            .catch(() => {});
    } catch (e) {}

    // 4. Track cumulative session dwell time across page navigation
    const now = Date.now();
    let sessionStart = parseInt(sessionStorage.getItem(SESSION_KEY_START) || "0", 10);
    if (!sessionStart || isNaN(sessionStart)) {
        sessionStart = now;
        sessionStorage.setItem(SESSION_KEY_START, sessionStart.toString());
    }

    const elapsed = now - sessionStart;
    const remainingDelay = Math.max(1000, DWELL_DELAY_MS - elapsed);
    console.log(`[EggStock Discord] Dwell tracker active: ${Math.round(elapsed / 1000)}s elapsed. Modal will show in ${Math.round(remainingDelay / 1000)}s.`);

    // 5. Modal Injection Helper
    function injectModal() {
        const existing = document.getElementById("discord-modal");
        if (existing) return existing;

        // Ensure backdrop & visibility CSS exists
        if (!document.getElementById("discord-modal-css")) {
            const style = document.createElement("style");
            style.id = "discord-modal-css";
            style.textContent = `
                .modal-backdrop {
                    background: rgba(5, 7, 12, 0.85);
                    backdrop-filter: blur(8px);
                }
                #discord-modal.hidden {
                    display: none !important;
                }
                #discord-modal:not(.hidden) {
                    display: flex !important;
                }
            `;
            (document.head || document.documentElement).appendChild(style);
        }

        const modalDiv = document.createElement("div");
        modalDiv.id = "discord-modal";
        modalDiv.className = "fixed inset-0 z-[99999] flex items-center justify-center p-4 modal-backdrop hidden";
        modalDiv.setAttribute("role", "dialog");
        modalDiv.setAttribute("aria-modal", "true");
        modalDiv.setAttribute("aria-labelledby", "discord-modal-title");

        modalDiv.innerHTML = `
            <div class="neo-card bg-[#131722] max-w-md w-full p-5 sm:p-6 relative border-2 border-black shadow-[6px_6px_0px_#000]">
                <!-- Header Badge & Discord Branding -->
                <div class="flex items-center gap-3 mb-3.5">
                    <div class="w-12 h-12 bg-[#5865f2] rounded border-2 border-black shadow-[2px_2px_0px_#000] flex items-center justify-center shrink-0">
                        <svg class="w-7 h-7 fill-white" viewBox="0 0 127.14 96.36">
                            <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,45.91,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,45.91,96.12,53,91.08,65.69,84.69,65.69Z"/>
                        </svg>
                    </div>
                    <div>
                        <div class="flex items-center gap-1.5 mb-1 flex-wrap">
                            <span class="bg-[#5865f2] text-white text-[9px] sm:text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[1px_1px_0px_#000]">OFFICIAL SERVER</span>
                            <span class="bg-[#00f0ff] text-black text-[9px] sm:text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[1px_1px_0px_#000]">1-CLICK AUTO-JOIN</span>
                        </div>
                        <h3 id="discord-modal-title" class="font-display font-black text-lg sm:text-xl uppercase text-white tracking-tight leading-tight">
                            Join EggStock Discord
                        </h3>
                    </div>
                </div>

                <!-- Subtitle -->
                <p class="text-xs text-slate-300 font-sans leading-relaxed mb-3.5">
                    Connect your Discord to auto-join the server, get instant stock alerts, and claim your verified Member role!
                </p>

                <!-- 3 Feature Bullets -->
                <div class="space-y-2 mb-4 font-mono text-xs">
                    <div class="bg-[#0a0d14] border border-black p-2.5 flex items-start gap-2.5">
                        <span class="text-base leading-none shrink-0">⚡</span>
                        <div>
                            <div class="font-bold text-[#00f0ff] uppercase text-[11px]">1-Click Auto-Join &amp; Role</div>
                            <div class="text-slate-300 text-[11px] leading-tight">Authorize once &amp; get automatically joined with verified @Member role instantly.</div>
                        </div>
                    </div>
                    <div class="bg-[#0a0d14] border border-black p-2.5 flex items-start gap-2.5">
                        <span class="text-base leading-none shrink-0">🔔</span>
                        <div>
                            <div class="font-bold text-[#fbabff] uppercase text-[11px]">Instant Stock Pings</div>
                            <div class="text-slate-300 text-[11px] leading-tight">Instant @pings the moment Divine (Kitsune, Nightflame), Secret &amp; Eternal eggs spawn.</div>
                        </div>
                    </div>
                    <div class="bg-[#0a0d14] border border-black p-2.5 flex items-start gap-2.5">
                        <span class="text-base leading-none shrink-0">🤝</span>
                        <div>
                            <div class="font-bold text-[#facc15] uppercase text-[11px]">VIP Trading &amp; Giveaways</div>
                            <div class="text-slate-300 text-[11px] leading-tight">Verified trade tiers, sneak peeks at upcoming biomes, and community giveaways.</div>
                        </div>
                    </div>
                </div>

                <!-- Primary CTA Button (Discord OAuth 1-Click Auto-Join) -->
                <a id="discord-modal-cta" href="/api/auth/discord/login" class="w-full bg-[#5865f2] hover:bg-[#4752c4] text-white font-display font-black py-3 px-4 text-sm sm:text-base uppercase neo-btn flex items-center justify-center gap-2 no-underline cursor-pointer mb-2.5 shadow-[3px_3px_0px_#000]">
                    <svg class="w-5 h-5 fill-white shrink-0" viewBox="0 0 127.14 96.36">
                        <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,45.91,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,45.91,96.12,53,91.08,65.69,84.69,65.69Z"/>
                    </svg>
                    <span>⚡ 1-Click Join with Discord ↗</span>
                </a>

                <!-- Secondary Fallback Link -->
                <div class="text-center mb-3">
                    <span class="text-[11px] text-slate-400 font-mono">Prefer manual invite? </span>
                    <a href="https://discord.gg/Jmvam6Ktgm" target="_blank" rel="noopener noreferrer" class="text-[11px] text-[#00f0ff] hover:underline font-mono font-bold">discord.gg/Jmvam6Ktgm ↗</a>
                </div>

                <!-- Exactly Two Dismissal Button Options -->
                <div class="flex items-center justify-between pt-3 border-t border-slate-800 text-xs font-mono gap-2">
                    <button id="discord-modal-disable" class="bg-[#241317] hover:bg-[#3d181f] text-red-300 hover:text-red-200 px-3 py-1.5 border border-black neo-btn text-xs font-bold flex items-center gap-1 cursor-pointer transition-colors shadow-[2px_2px_0px_#000]" title="Turn off permanently">
                        <span>🚫 Don't show again</span>
                    </button>
                    <button id="discord-modal-close" class="bg-[#181d2c] hover:bg-slate-700 text-slate-200 px-3 py-1.5 border border-black neo-btn text-xs font-bold flex items-center gap-1 cursor-pointer transition-colors shadow-[2px_2px_0px_#000]" title="Close for this visit">
                        <span>✕ Close this time</span>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(modalDiv);

        function closeDiscordModal(permanent) {
            modalDiv.classList.add("hidden");
            sessionStorage.setItem(SESSION_KEY_SEEN, "true");
            if (permanent) {
                localStorage.setItem(STORAGE_KEY_DISABLED, "true");
            }
            console.log("[EggStock Discord] Modal closed.", permanent ? "Permanently disabled." : "Dismissed for this session.");
        }

        const closeBtn = document.getElementById("discord-modal-close");
        const disableBtn = document.getElementById("discord-modal-disable");
        const ctaBtn = document.getElementById("discord-modal-cta");

        if (closeBtn) {
            closeBtn.addEventListener("click", () => closeDiscordModal(false));
        }

        if (disableBtn) {
            disableBtn.addEventListener("click", () => {
                closeDiscordModal(true);
                if (typeof window.showToast === "function") {
                    window.showToast("Discord prompt disabled permanently.");
                }
            });
        }

        if (ctaBtn) {
            ctaBtn.addEventListener("click", () => {
                localStorage.setItem("es_discord_joined", "true");
                closeDiscordModal(true);
            });
        }

        const manualLink = modalDiv.querySelector('a[href*="discord.gg"]');
        if (manualLink) {
            manualLink.addEventListener("click", () => {
                localStorage.setItem("es_discord_joined", "true");
                closeDiscordModal(true);
                if (typeof window.showToast === "function") {
                    window.showToast("🎉 Discord Joined! Welcome to the server.");
                }
            });
        }

        modalDiv.addEventListener("click", (e) => {
            if (e.target === modalDiv) closeDiscordModal(false);
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && !modalDiv.classList.contains("hidden")) {
                closeDiscordModal(false);
            }
        });

        return modalDiv;
    }

    // 6. Schedule modal display after session dwell delay
    setTimeout(() => {
        if (localStorage.getItem(STORAGE_KEY_DISABLED) === "true") return;
        if (sessionStorage.getItem(SESSION_KEY_SEEN) === "true") return;

        let modal = document.getElementById("discord-modal") || injectModal();
        if (modal) {
            modal.classList.remove("hidden");
            console.log("[EggStock Discord] OAuth popup displayed successfully after 30s dwell!");
        }
    }, remainingDelay);

    // Pre-inject modal HTML when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", injectModal);
    } else {
        injectModal();
    }

    // Interactive developer/test override
    window.__testDiscordModal = function() {
        sessionStorage.removeItem(SESSION_KEY_SEEN);
        sessionStorage.removeItem(SESSION_KEY_START);
        let modal = document.getElementById("discord-modal") || injectModal();
        if (modal) {
            modal.classList.remove("hidden");
            console.log("[EggStock Discord] Modal forced visible via __testDiscordModal()!");
        }
    };
})();
