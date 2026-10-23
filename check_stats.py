import os
import json
import urllib.request
from datetime import datetime, timezone

SUPABASE_URL = "https://mtymdgujtauyqupjdcsr.supabase.co"
SUPABASE_KEY = "REDACTED_SUPABASE_KEY"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/oauth_users?select=*&order=created_at.desc", headers=HEADERS)
with urllib.request.urlopen(req) as resp:
    users = json.loads(resp.read().decode())

print(f"Total OAuth Users: {len(users)}")
today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
today_users = [u for u in users if u.get("created_at", "").startswith(today_str)]
print(f"Users created today ({today_str} UTC): {len(today_users)}")

for u in users:
    uname = u.get("username", "Unknown")
    created = u.get("created_at", "")
    joined = u.get("joined_guild", False)
    print(f"  - {uname:20} | Created: {created} | Joined: {joined}")

# Check local sqlite database as well
import sqlite3
db_path = "data/oauth_members.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM authorized_members")
    local_count = cur.fetchone()[0]
    print(f"\nLocal SQLite count: {local_count}")
    conn.close()
