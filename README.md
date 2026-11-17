# Discord Honeypot DMs

A single-server moderation bot. When a member sends a matching promotional DM directly to the bot, it immediately requests a server ban. It ignores server chat and has no access to DMs between other accounts.

## Run on Windows

1. Install Python 3.11 or newer. Download and extract this repository or clone it.
2. Create an application in the [Discord Developer Portal](https://discord.com/developers/applications). Under Bot, generate a bot token. Keep it private.
3. Under Installation, configure Guild Install with the bot scope and Ban Members permission. Use the install link to add it to the target server. Leave privileged gateway intents off.
4. In Server Settings → Roles, put the bot above ordinary member roles and below any staff roles you want protected. Enable Developer Mode in Discord's Advanced settings, then right-click the server icon and select Copy Server ID.
5. Open PowerShell in the extracted project folder and run:

```powershell
py -m pip install -r requirements.txt
py -m unittest -v
py dm_guard.py
```

Enter the server ID and token when prompted. For unattended use, set DISCORD_SERVER_ID and DISCORD_BOT_TOKEN in the host environment. Keep one instance running on an always-on computer or host. Publishing the code on GitHub does not host the bot.

## What triggers a ban

A gambling topic must appear alongside promotional signals, such as a casino offer plus an invite, a betting-picks pitch plus a sign-up prompt, or a gambling-specific recruitment message plus a link. The filter reads the sender's message text, including pasted URLs. Discord's generated link previews and image contents are excluded. An invitation alone, ordinary poker chat, or a win screenshot without promotional text passes. The text rules can miss new wording or match a quoted advertisement. Use another channel for reporting ads.

Bans preserve server message history and include the triggering message ID in the audit reason. Discord role hierarchy protects the server owner and equal or higher roles. To check the complete setup, run it in a test server and DM the bot first with ordinary poker chat and then with a sample ad from a disposable member account. Check Server Settings → Audit Log.
