import urllib.request
import json
import os
import sys

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://mtymdgujtauyqupjdcsr.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_KEY:
    print("SUPABASE_KEY environment variable is not set. Please set it before running this script.")
    sys.exit(0)

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/oauth_users?select=*&order=created_at.desc", headers=HEADERS)
try:
    with urllib.request.urlopen(req) as resp:
        users = json.loads(resp.read().decode('utf-8'))
        print(f"Total OAuth Users in Supabase: {len(users)}")
        for u in users:
            print(f"  - {u.get('username')} ({u.get('user_id')}) | Joined: {u.get('joined_at')} | Last Seen: {u.get('last_seen_at')}")
except Exception as e:
    print("Error querying Supabase:", e)
