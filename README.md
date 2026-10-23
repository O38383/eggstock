# Steal An Egg - Stock Radar Bot

Listens to your server's `#stock-notify` channel (where SenZ V2 posts spawn
alerts), parses each spawn, tracks running stats, and exposes them as JSON
at `/api/status` for your OBS overlay to poll.

## 1. Create YOUR OWN Discord bot (separate from SenZ V2)

1. Go to https://discord.com/developers/applications
2. New Application -> name it whatever (e.g. "Egg Radar Reader")
3. Bot tab -> Add Bot -> copy the **Token** (this is your `DISCORD_TOKEN`)
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**
5. OAuth2 -> URL Generator -> scopes: `bot` -> permissions: `View Channels`,
   `Read Message History` -> use the generated link to invite it to your
   own server (the same one SenZ V2 is in)

## 2. Get your channel ID

In Discord: Settings -> Advanced -> enable Developer Mode.
Right-click `#stock-notify` -> Copy Channel ID -> this is `STOCK_NOTIFY_CHANNEL_ID`.

## 3. Deploy to Railway

1. Push this folder to a GitHub repo
2. In Railway: New Project -> Deploy from GitHub repo
3. Add environment variables (Settings -> Variables) using `.env.example`
   as your guide -- at minimum set `DISCORD_TOKEN` and `STOCK_NOTIFY_CHANNEL_ID`
4. Railway will run the `web: python bot.py` process from the Procfile.
5. Once deployed, Railway gives you a public URL. Use
   `https://your-app.up.railway.app/overlay` as your OBS Browser Source URL.

## 4. Test it

Once the bot is running and in your server, watch the logs in Railway.
When SenZ V2 posts a new spawn alert in `#stock-notify`, you should see a
log line like:
```
Recorded drop: {'rarity': 'secret', 'egg': 'Kraken', 'location': 'Abyss Ocean'} | session_drops=1
```

Then visit `/api/status` to see the live JSON, or `/overlay` to preview the
live panel. The overlay polls the API on the same domain every two seconds.

## OBS overlay

The original, stream-ready overlay is served by this bot, so it does not need
a separate host:

1. In OBS, add a **Browser** source.
2. Set its URL to `https://your-app.up.railway.app/overlay`.
3. Start with a width of 540 px; the panel is responsive and transparent
   outside its own card layout.

It shows the data the API currently provides: the next-wave estimate, session
and rarity counts, last-drop timing, an auto-updating drop feed, and an
expected Saturday 15:00 UTC admin-event countdown. It intentionally shows
"Player API Pending" until a Roblox player-count field is added to the API.

## Notes / things to verify once real messages start flowing

- The parser assumes the embed **title** contains something like
  `"Secret Egg Spawned!! - 8:39 AM"` and the **description/fields** contain
  lines like `Egg: <name>` and `Location: <place>`. If SenZ V2's actual
  embed structure differs slightly (e.g. fields split differently), the
  regex in `parse_embed()` may need small tweaks -- send a real captured
  message and it's a quick fix.
- Wave timing is a median of recently observed real gaps (with a 300-second
  fallback until data arrives). The overlay labels its confidence and source
  instead of presenting the estimate as fact.
- The bot also parses the edited `#last-stock-notify` message to bootstrap
  timing data before new spawn messages arrive.
