# Master Claude 3.5 Sonnet Prompt for EggStock UI/UX Audit

Copy and paste the entire prompt below directly into **Claude** (Claude 3.5 Sonnet / Claude Web). 

You can also attach screenshots of `https://eggstock.xyz` (desktop and mobile captured with `Win + Shift + S`) alongside this prompt for Claude's Vision engine.

---

```markdown
You are a Principal Product Designer and Lead UI/UX Architect specializing in high-converting gaming web applications, real-time trackers, and consumer dashboards (benchmarks: Tracker.gg, Blox Fruits Values, Traderie, DexScreener).

I want you to perform a brutal, granular, and actionable UI/UX and visual audit of my live Roblox companion website:
🔗 URL: https://eggstock.xyz

### Product Context:
- **Product**: EggStock — The #1 real-time live stock radar, wave prediction forecaster, trade calculator, and pet value list for the Roblox game "Steal An Egg".
- **Audience**: Roblox gamers (ages 13–24, high-velocity kinetic attention spans, competitive players trying to rush spawns before public lobbies).
- **Traffic Split**: ~70% Mobile (iOS/Android), ~30% Desktop PC.
- **Design Language**: Dark Neo-Brutalist Cyber/Gaming theme (`#0b0f19` obsidian dark base, vibrant neon accents: `#00f0ff` electric cyan, `#ff00ff` hot magenta, `#fbff00` tactical yellow, `#00ff66` neon lime, with bold 2px/3px solid black borders and retro-modern drop shadows).

---

### Audit Instructions:
Analyze the live interface (and any attached screenshots) across the following 7 pillars. Do not give generic advice—be specific about components, layouts, typography, spacing, and micro-interactions.

#### 1. First 3 Seconds & Cognitive Load (Above The Fold)
- Does the user instantly know what to look at within 1.5 seconds of landing?
- Are the Ticker Tape, Live Event Radar Strip, and Wave Prediction card competing for dominance, or is there a clear visual anchor?
- Is the "Next Spawn Wave Countdown" sufficiently prominent as the #1 hero utility?

#### 2. Mobile Ergonomics & Tap Targets (Crucial: 70% of Traffic)
- Audit the mobile experience (375px–420px viewport):
  - Are touch targets at least 44x44px with adequate thumb spacing?
  - Do sticky elements (nav bars, floating audio soundboard, bottom banners) crowd the viewport or create claustrophobia on small screens?
  - Are table data (recent drop logs, tier lists) horizontally scrollable without breaking page layout?

#### 3. Neo-Brutalist Design Consistency & Polish
- Check for styling fragmentation:
  - Are corner radiuses (sharp 0px vs rounded-sm) consistent across cards, badges, and modals?
  - Are shadow offsets (`shadow-[2px_2px_0px_#000]` vs `shadow-[4px_4px_0px_#000]`) used systematically by hierarchy level?
  - Is contrast accessible (WCAG AA) on text placed over dark card backgrounds?

#### 4. Information Architecture & Navigation
- How frictionless is moving between:
  1. Live Radar (`/`)
  2. Trade Calculator (`/calculator`)
  3. Pet Values (`/values`)
  4. Halloween Event Portal Timers
- Is the navigation bar intuitive on both desktop and mobile hamburger menus?

#### 5. Conversion & Funnel Leakage
- Evaluate the Call-to-Action (CTA) hierarchy:
  - "Arm Spawn Alerts (Browser Push)"
  - "Join Discord Live Bot"
  - "Copy Automation Loadstring"
- Are high-value conversion actions clear, or are users experiencing decision paralysis?

#### 6. Micro-Interactions & Gamified Delight
- How does the UI feel as a "live radar tool"? 
- What subtle animations, pulse states, audio feedbacks, or hover effects are missing that would elevate it from a static webpage to a high-tech tactical radar station?

---

### Deliverables Required:
1. **The Executive Verdict**: 3 biggest visual strengths + 3 biggest usability flaws.
2. **Prioritized "Roast & Fix" Table**:
   | Priority (P0 Critical / P1 Medium / P2 Polish) | Specific Component / Area | The Flaw & Why It Hurts UX | Exact Tailwind CSS / Design Fix |
3. **Top 3 High-Impact Quick Wins**: Changes that can be made in under 15 minutes to dramatically improve aesthetics and user retention.
```
