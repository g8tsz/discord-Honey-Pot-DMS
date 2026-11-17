import logging
import os
from getpass import getpass

import discord

from spam_filter import is_promotional_spam

log = logging.getLogger("dm_guard")


def main():
    server_id = int(os.getenv("DISCORD_SERVER_ID") or input("Server ID: ").strip())
    token = os.getenv("DISCORD_BOT_TOKEN") or getpass("Bot token: ").strip()
    intents = discord.Intents.none()
    intents.guilds = True
    intents.dm_messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        guild = client.get_guild(server_id)
        if guild is None or not guild.me.guild_permissions.ban_members:
            log.error("Check the server ID, bot installation and Ban Members permission.")
            await client.close()
            return
        log.info("Monitoring promotional DMs for server %s", server_id)

    @client.event
    async def on_message(message):
        if message.author.bot or not isinstance(message.channel, discord.DMChannel):
            return
        if not is_promotional_spam(message.content):
            return
        await client.wait_until_ready()
        guild = client.get_guild(server_id)
        if guild is None:
            return
        try:
            member = await guild.fetch_member(message.author.id)
            if member.id == guild.owner_id or member.top_role >= guild.me.top_role:
                log.info("Role hierarchy protects member %s", member.id)
                return
            await member.ban(
                reason=f"Promotional spam DM to honeypot (message {message.id})",
                delete_message_seconds=0,
            )
            log.info("Banned member %s for promotional DM %s", member.id, message.id)
        except discord.NotFound:
            return
        except discord.HTTPException:
            log.exception("Could not moderate DM %s from %s", message.id, message.author.id)

    logging.basicConfig(level=logging.INFO)
    client.run(token, log_handler=None)


if __name__ == "__main__":
    main()
