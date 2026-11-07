/**
 * EggStock.xyz - Open Source Announcement & Community Banner
 * (Replaces legacy Discord popup lock)
 */

(function initOpenSourceAnnouncement() {
    // 1. Permanently disable legacy Discord join popups & unlock full radar feed
    try {
        localStorage.setItem("es_discord_popup_disabled", "true");
        localStorage.setItem("es_discord_joined", "true");
    } catch (e) {}

    // Suppress any existing modal if left in DOM
    const oldModal = document.getElementById("discord-modal");
    if (oldModal) {
        oldModal.remove();
    }

    // 2. Check if user dismissed the announcement banner
    if (localStorage.getItem("es_os_banner_dismissed") === "true") {
        return;
    }

    function injectBanner() {
        if (document.getElementById("es-open-source-banner")) return;

        const banner = document.createElement("div");
        banner.id = "es-open-source-banner";
        banner.className = "w-full bg-[#FFE600] text-black border-b-2 border-black px-3 py-2 text-xs font-mono font-bold flex items-center justify-between shadow-[0_2px_0_#000] z-[9999] relative";
        banner.innerHTML = `
            <div class="flex items-center gap-2 flex-wrap mx-auto text-center justify-center">
                <span class="inline-flex items-center justify-center bg-black text-[#FFE600] px-1.5 py-0.5 rounded text-[10px] uppercase font-black tracking-wider animate-pulse">NEW</span>
                <span>⚡ EggStock is now <strong>100% Free & Open Source</strong>! Free Developer API is live.</span>
                <a href="https://github.com/O38383/eggstock" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 bg-black text-white hover:bg-white hover:text-black border border-black px-2 py-0.5 rounded transition-all shadow-[1px_1px_0px_#000] ml-1">
                    <span>⭐ Star on GitHub</span>
                    <svg class="w-3 h-3 fill-current" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
                </a>
            </div>
            <button id="es-dismiss-banner" aria-label="Dismiss banner" class="text-black hover:opacity-60 font-black text-sm px-1 cursor-pointer ml-2">✕</button>
        `;

        document.body.prepend(banner);

        const dismissBtn = document.getElementById("es-dismiss-banner");
        if (dismissBtn) {
            dismissBtn.addEventListener("click", () => {
                banner.remove();
                try {
                    localStorage.setItem("es_os_banner_dismissed", "true");
                } catch (e) {}
            });
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", injectBanner);
    } else {
        injectBanner();
    }
})();
