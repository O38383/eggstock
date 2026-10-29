from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json
import datetime
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SITE_URL = "https://eggstock.xyz/"
CREDENTIALS_PATH = "C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/ga_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

def get_token():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token

def fetch_gsc_stats():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # GSC data usually has a 2-3 day lag for full analytics, let's query the last 28 days and last 7 days
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=28)).isoformat()
    end_date = today.isoformat()

    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(SITE_URL, safe='')}/searchAnalytics/query"

    # 1. Overall totals
    totals_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["date"]
    }
    totals_res = requests.post(api_url, headers=headers, json=totals_body).json()

    # 2. Top search keywords/queries
    query_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 20
    }
    query_res = requests.post(api_url, headers=headers, json=query_body).json()

    # 3. Top Pages
    pages_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": 10
    }
    pages_res = requests.post(api_url, headers=headers, json=pages_body).json()

    # 4. Top Countries
    country_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["country"],
        "rowLimit": 10
    }
    country_res = requests.post(api_url, headers=headers, json=country_body).json()

    # 5. Sitemaps
    sitemaps_url = f"https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(SITE_URL, safe='')}/sitemaps"
    sitemaps_res = requests.get(sitemaps_url, headers=headers).json()

    print("\n" + "="*60)
    print("🔎 GOOGLE SEARCH CONSOLE PERFORMANCE REPORT (eggstock.xyz)")
    print("="*60)

    total_clicks = sum(r.get("clicks", 0) for r in totals_res.get("rows", []))
    total_impressions = sum(r.get("impressions", 0) for r in totals_res.get("rows", []))
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_pos = (sum(r.get("position", 0) for r in totals_res.get("rows", [])) / len(totals_res["rows"])) if totals_res.get("rows") else 0

    print(f"\n📊 LAST 28 DAYS OVERVIEW:")
    print(f"  • Total Google Clicks:      {total_clicks:,}")
    print(f"  • Total Google Impressions: {total_impressions:,}")
    print(f"  • Average Click-Through:   {avg_ctr:.2f}%")
    print(f"  • Average Ranking Position: #{avg_pos:.1f}")

    print(f"\n🎯 TOP SEARCH QUERIES RANKING ON GOOGLE:")
    print(f"  {'Query / Keyword':<35} {'Clicks':>7} {'Impressions':>12} {'CTR':>8} {'Position':>10}")
    print("  " + "-"*75)
    for r in query_res.get("rows", []):
        q = r["keys"][0]
        clicks = int(r.get("clicks", 0))
        imp = int(r.get("impressions", 0))
        ctr = r.get("ctr", 0) * 100
        pos = r.get("position", 0)
        print(f"  {q:<35} {clicks:>7} {imp:>12} {ctr:>7.1f}% #{pos:>8.1f}")

    print(f"\n📄 TOP RANKING PAGES:")
    for r in pages_res.get("rows", []):
        p = r["keys"][0].replace("https://eggstock.xyz", "")
        if not p: p = "/"
        clicks = int(r.get("clicks", 0))
        imp = int(r.get("impressions", 0))
        pos = r.get("position", 0)
        print(f"  • {p:<25} Clicks: {clicks:>5} | Imp: {imp:>6} | Pos: #{pos:.1f}")

    print(f"\n🗺️ SITEMAPS STATUS:")
    for sm in sitemaps_res.get("sitemap", []):
        sm_path = sm.get("path")
        last_sub = sm.get("lastSubmitted", "N/A")
        warn = sm.get("warnings", 0)
        err = sm.get("errors", 0)
        print(f"  • {sm_path} (Errors: {err}, Warnings: {warn}, Submitted: {last_sub})")

    print("="*60 + "\n")

if __name__ == "__main__":
    fetch_gsc_stats()
