import urllib.request
import json
import re

req = urllib.request.Request('https://eggstock.xyz/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')
    tokens = re.findall(r'window\.__ES_TOKEN\s*=\s*"([^"]+)"', html)
    token = tokens[0] if tokens else None

print("Token extracted successfully:", bool(token))

req2 = urllib.request.Request('https://eggstock.xyz/api/status', headers={'User-Agent': 'Mozilla/5.0', 'X-EggStock-Token': token})
with urllib.request.urlopen(req2) as resp2:
    data = json.loads(resp2.read().decode('utf-8'))
    print("API Status: 200 OK")
    print("Roblox Playing Now:", data.get('playing_now'))
    print("Discord Online:", data.get('discord_online'))
    print("Discord Members:", data.get('discord_members'))
    print("Last Drop:", data.get('last_drop'))
