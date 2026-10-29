from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROPERTY_ID = "553931222"
CREDENTIALS_PATH = "C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/ga_credentials.json"

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

def get_token():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token

def fetch_overview():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 1. Realtime Active Users
    rt_res = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runRealtimeReport",
        headers=headers,
        json={
            "metrics": [{"name": "activeUsers"}],
            "dimensions": [{"name": "country"}]
        }
    ).json()
    
    # 2. Today Totals
    today_res = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport",
        headers=headers,
        json={
            "dateRanges": [{"startDate": "today", "endDate": "today"}],
            "metrics": [
                {"name": "activeUsers"},
                {"name": "newUsers"},
                {"name": "sessions"},
                {"name": "screenPageViews"},
                {"name": "eventCount"}
            ]
        }
    ).json()

    # 3. Top Pages Today
    pages_res = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport",
        headers=headers,
        json={
            "dateRanges": [{"startDate": "today", "endDate": "today"}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
            "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
            "limit": 10
        }
    ).json()

    # 4. Top Traffic Sources / Referrers Today
    sources_res = requests.post(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport",
        headers=headers,
        json={
            "dateRanges": [{"startDate": "today", "endDate": "today"}],
            "dimensions": [{"name": "sessionSource"}],
            "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
            "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
            "limit": 10
        }
    ).json()

    print("\n" + "="*50)
    print("🚀 EGGSTOCK LIVE GOOGLE ANALYTICS REPORT")
    print("="*50)

    # Realtime
    rt_total = sum(int(r["metricValues"][0]["value"]) for r in rt_res.get("rows", []))
    print(f"\n🔴 REAL-TIME ACTIVE USERS (Last 30 Min): {rt_total}")
    print("Top Countries Right Now:")
    for r in rt_res.get("rows", [])[:7]:
        country = r["dimensionValues"][0]["value"]
        users = r["metricValues"][0]["value"]
        print(f"  • {country}: {users} users")

    # Today Totals
    if today_res.get("rows"):
        m = today_res["rows"][0]["metricValues"]
        print(f"\n📅 TODAY'S STATS (Oct 29, 2026):")
        print(f"  • Total Active Users: {m[0]['value']}")
        print(f"  • New Users:          {m[1]['value']}")
        print(f"  • Total Sessions:     {m[2]['value']}")
        print(f"  • Page Views:         {m[3]['value']}")
        print(f"  • Total Events:       {m[4]['value']}")

    # Top Pages
    print(f"\n📄 TOP PAGES TODAY:")
    for r in pages_res.get("rows", []):
        path = r["dimensionValues"][0]["value"]
        views = r["metricValues"][0]["value"]
        users = r["metricValues"][1]["value"]
        print(f"  • {path:<30} {views:>5} views ({users} users)")

    # Top Sources
    print(f"\n🌐 TOP TRAFFIC SOURCES:")
    for r in sources_res.get("rows", []):
        src = r["dimensionValues"][0]["value"]
        sess = r["metricValues"][0]["value"]
        users = r["metricValues"][1]["value"]
        print(f"  • {src:<30} {sess:>5} sessions ({users} users)")
    print("="*50 + "\n")

if __name__ == "__main__":
    fetch_overview()
