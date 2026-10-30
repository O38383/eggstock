import sys
import os
import json
import urllib.request
import urllib.error
import datetime

# Configure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_token():
    # 1. Environment variable
    if os.environ.get("MONETAG_TOKEN"):
        return os.environ.get("MONETAG_TOKEN").strip()
    # 2. Local token file
    token_path = os.path.join(os.path.dirname(__file__), "monetag_token.txt")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    raise ValueError("Monetag token not found. Set MONETAG_TOKEN env or create monetag_token.txt.")

def api_get(endpoint, token, params=None):
    url = f"https://api.monetag.com/v5/{endpoint.lstrip('/')}"
    if params:
        query_parts = []
        for k, v in params.items():
            if isinstance(v, list):
                for item in v:
                    query_parts.append(f"{k}[]={item}")
            else:
                query_parts.append(f"{k}={v}")
        url += "?" + "&".join(query_parts)

    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "Eggstock-Monetag-Client/1.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {e.code} on {url}: {err_msg}")

def main():
    token = get_token()

    print("=" * 65)
    print(" 💰 MONETAG LIVE REVENUE & PUSH ANALYTICS (eggstock.xyz)")
    print("=" * 65)

    # 1. Fetch Sites & Zones
    try:
        sites_data = api_get("pub/sites", token)
        sites = sites_data.get("sites", [])
        print("\n🌐 VERIFIED SITES:")
        for s in sites:
            status = "✅ Verified" if s.get("user_verification_status") == 2 else "⏳ Pending"
            print(f"  • {s.get('url')} (Site ID: {s.get('id')}) - {status}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch sites: {e}")

    try:
        zones_data = api_get("pub/zones", token)
        zones = zones_data.get("zones", [])
        print("\n🎯 ACTIVE AD ZONES:")
        for z in zones:
            fmt = "Push Notifications" if z.get("direction_id") == 61 else f"Type {z.get('direction_id')}"
            print(f"  • {z.get('title')} (Zone ID: {z.get('id')}) | Format: {fmt} | Site ID: {z.get('site_id')}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch zones: {e}")

    # 2. Daily Performance (Past 7 Days)
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=7)
    
    print(f"\n📊 PERFORMANCE BREAKDOWN ({start_date} to {today}):")
    try:
        stats = api_get("pub/statistics", token, {
            "date_from": start_date.strftime("%Y-%m-%d"),
            "date_to": today.strftime("%Y-%m-%d"),
            "group_by": ["date_time"]
        })
        rows = sorted(stats.get("result", []), key=lambda x: x.get("date_time", ""))

        header = f"{'Date':<11} | {'Revenue':<10} | {'Push Subs':<10} | {'Impressions':<11} | {'Clicks':<8} | {'CPM':<8}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        tot_rev = 0.0
        tot_subs = 0
        tot_impr = 0
        tot_clicks = 0

        for r in rows:
            date = r.get("date_time", "")
            rev = float(r.get("money", 0))
            subs = int(r.get("subscriptions", 0))
            impr = int(r.get("impressions", 0))
            clicks = int(r.get("clicks", 0))
            cpm = (rev / impr * 1000) if impr else 0.0

            tot_rev += rev
            tot_subs += subs
            tot_impr += impr
            tot_clicks += clicks

            print(f"{date:<11} | ${rev:>8.2f}  | {subs:>9d}  | {impr:>11d} | {clicks:>8d} | ${cpm:>6.2f}")

        print("-" * len(header))
        avg_cpm = (tot_rev / tot_impr * 1000) if tot_impr else 0.0
        print(f"{'TOTAL':<11} | ${tot_rev:>8.2f}  | {tot_subs:>9d}  | {tot_impr:>11d} | {tot_clicks:>8d} | ${avg_cpm:>6.2f}")
    except Exception as e:
        print(f"  ⚠️ Could not fetch daily statistics: {e}")

    print("\n" + "=" * 65)
    print(" 🔌 OFFICIAL MONETAG MCP SERVER CONNECTION DETAILS")
    print("=" * 65)
    print(" • MCP Server URL : https://mcp.monetag.com/mcp")
    print(" • Transport      : HTTP / SSE (Streamable JSON-RPC 2.0)")
    print(" • Authentication : Authorization: Bearer <TOKEN>")
    print(" • Claude CLI add :")
    print('   claude mcp add --transport http monetag https://mcp.monetag.com/mcp')
    print("=" * 65)

if __name__ == "__main__":
    main()
