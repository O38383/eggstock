"""
analyze_spawns.py - In-depth statistical and predictive analysis of historical egg spawns.
Fetches hundreds of real spawn alerts from SenZ V2 in #stock-notify.
Analyzes wave intervals, biome rotations, egg rarity distributions, and Markov transitions.
"""

import os
import re
import json
import urllib.request
from datetime import datetime, timezone
from collections import defaultdict, Counter
import statistics

TOKEN = os.environ.get("DISCORD_TOKEN", "")
CHANNEL_ID = "1546504423910670458"
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot (https://eggstock.xyz, 1.0)",
}

TITLE_RE = re.compile(r"(Secret|Eternal|Divine)\s+Egg\s+Spawned", re.IGNORECASE)
FIELD_RE = re.compile(r"\*\*Egg:\*\*\s*(.+)", re.IGNORECASE)
LOCATION_RE = re.compile(r"\*\*Location:\*\*\s*(.+)", re.IGNORECASE)

def sanitize(val):
    if not val:
        return "Unknown"
    cleaned = re.sub(r"<[^>]+>", "", val)
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    cleaned = cleaned.replace("*", "").replace("`", "").replace("_", "").strip()
    return cleaned if cleaned else "Unknown"

def parse_msg(m):
    embeds = m.get("embeds", [])
    if not embeds:
        return None
    e = embeds[0]
    title = e.get("title", "")
    match = TITLE_RE.search(title)
    if not match:
        return None
    rarity = match.group(1).capitalize()
    
    text = e.get("description", "")
    for f in e.get("fields", []):
        text += f"\n{f.get('name','')}: {f.get('value','')}"
        
    egg_m = FIELD_RE.search(text)
    loc_m = LOCATION_RE.search(text)
    
    egg = sanitize(egg_m.group(1) if egg_m else "Unknown")
    loc = sanitize(loc_m.group(1) if loc_m else "Unknown")
    
    # Parse timestamp
    raw_ts = m.get("timestamp")
    dt = datetime.fromisoformat(raw_ts)
    
    return {
        "id": m.get("id"),
        "timestamp": dt.timestamp(),
        "iso": dt.isoformat(),
        "dt": dt,
        "rarity": rarity,
        "egg": egg,
        "location": loc
    }

def fetch_history(target_count=500):
    drops = []
    before = None
    print(f"Fetching up to {target_count} messages from Discord...")
    while len(drops) < target_count:
        url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=100"
        if before:
            url += f"&before={before}"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req) as resp:
                batch = json.loads(resp.read())
                if not batch:
                    break
                for m in batch:
                    parsed = parse_msg(m)
                    if parsed:
                        drops.append(parsed)
                before = batch[-1].get("id")
                print(f"  Fetched {len(batch)} msgs (total parsed drops: {len(drops)})")
                if len(batch) < 100:
                    break
        except Exception as exc:
            print("Fetch error:", exc)
            break
            
    # Sort oldest to newest
    drops.sort(key=lambda x: x["timestamp"])
    return drops

def analyze(drops):
    if not drops:
        print("No drops to analyze.")
        return
        
    print("\n" + "="*60)
    print(f"STEAL AN EGG SPAWN ANALYSIS (Total Drops: {len(drops)})")
    first_time = drops[0]["iso"]
    last_time = drops[-1]["iso"]
    print(f"Time Range: {first_time} to {last_time}")
    print("="*60)
    
    # 1. Rarity Counts
    rarity_counts = Counter(d["rarity"] for d in drops)
    total = len(drops)
    print("\n--- 1. RARITY DISTRIBUTION ---")
    for r, count in rarity_counts.most_common():
        pct = (count / total) * 100
        print(f"  {r:10}: {count:4} drops ({pct:5.1f}%) [1 in {round(total/count, 1)}]")
        
    # 2. Egg Counts
    egg_counts = Counter(d["egg"] for d in drops)
    print("\n--- 2. TOP EGGS SPAWNED ---")
    for egg, count in egg_counts.most_common():
        pct = (count / total) * 100
        print(f"  {egg:24}: {count:4} drops ({pct:5.1f}%)")
        
    # 3. Biome / Location Counts
    loc_counts = Counter(d["location"] for d in drops)
    print("\n--- 3. BIOME / LOCATION DISTRIBUTION ---")
    for loc, count in loc_counts.most_common():
        pct = (count / total) * 100
        print(f"  {loc:20}: {count:4} drops ({pct:5.1f}%)")
        
    # 4. Wave Clustering (Drops within 90 seconds belong to the same spawn wave)
    waves = []
    current_wave = [drops[0]]
    for d in drops[1:]:
        if (d["timestamp"] - current_wave[-1]["timestamp"]) <= 90:
            current_wave.append(d)
        else:
            waves.append(current_wave)
            current_wave = [d]
    if current_wave:
        waves.append(current_wave)
        
    print(f"\n--- 4. SPAWN WAVE CADENCE (Total Waves: {len(waves)}) ---")
    wave_sizes = Counter(len(w) for w in waves)
    for sz, count in sorted(wave_sizes.items()):
        print(f"  Wave with {sz} egg(s): {count} times ({(count/len(waves))*100:.1f}%)")
        
    # Wave Intervals
    wave_intervals = []
    for i in range(1, len(waves)):
        gap = waves[i][0]["timestamp"] - waves[i-1][0]["timestamp"]
        if gap >= 60: # Valid gap
            wave_intervals.append(gap)
            
    if wave_intervals:
        mean_gap = statistics.mean(wave_intervals)
        median_gap = statistics.median(wave_intervals)
        stdev_gap = statistics.stdev(wave_intervals) if len(wave_intervals) > 1 else 0
        min_gap = min(wave_intervals)
        max_gap = max(wave_intervals)
        print(f"\n  Wave Interval Stats:")
        print(f"    Mean Gap:   {mean_gap:.1f}s ({mean_gap/60:.2f} min)")
        print(f"    Median Gap: {median_gap:.1f}s ({median_gap/60:.2f} min)")
        print(f"    Std Dev:    {stdev_gap:.1f}s ({stdev_gap/60:.2f} min)")
        print(f"    Min Gap:    {min_gap:.1f}s | Max Gap: {max_gap:.1f}s")
        
    # 5. Gap by Rarity
    print("\n--- 5. CADENCE BY RARITY ---")
    for r in ["Secret", "Eternal", "Divine"]:
        r_drops = [d for d in drops if d["rarity"].lower() == r.lower()]
        if len(r_drops) > 1:
            r_gaps = []
            for i in range(1, len(r_drops)):
                gap = r_drops[i]["timestamp"] - r_drops[i-1]["timestamp"]
                if gap >= 60:
                    r_gaps.append(gap)
            if r_gaps:
                print(f"  {r:10}: Avg Interval = {statistics.mean(r_gaps)/60:.1f} min | Median = {statistics.median(r_gaps)/60:.1f} min (Count = {len(r_drops)})")
        else:
            print(f"  {r:10}: Only {len(r_drops)} drop(s) observed")
            
    # 6. Hourly Patterns (Top of Hour / Admin Luck)
    minute_buckets = [0] * 60
    for d in drops:
        minute_buckets[d["dt"].minute] += 1
    print("\n--- 6. HOURLY MINUTE CLUSTERING (0-59 min) ---")
    top_mins = sorted(range(60), key=lambda m: minute_buckets[m], reverse=True)[:5]
    print(f"  Top 5 peak spawn minutes of every hour:")
    for m in top_mins:
        print(f"    Minute :{m:02d} -> {minute_buckets[m]} drops")
        
    # Save processed analysis data to json
    summary_data = {
        "total_drops": total,
        "total_waves": len(waves),
        "rarity_distribution": dict(rarity_counts),
        "egg_distribution": dict(egg_counts),
        "biome_distribution": dict(loc_counts),
        "median_wave_interval_sec": round(median_gap) if wave_intervals else 300,
        "mean_wave_interval_sec": round(mean_gap) if wave_intervals else 300,
        "recent_samples": [{
            "egg": d["egg"],
            "rarity": d["rarity"],
            "location": d["location"],
            "timestamp": d["timestamp"],
            "iso": d["iso"]
        } for d in drops[-50:]]
    }
    with open("data/spawn_analysis.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print("\nSaved summary to data/spawn_analysis.json")

if __name__ == "__main__":
    drops = fetch_history(500)
    analyze(drops)
