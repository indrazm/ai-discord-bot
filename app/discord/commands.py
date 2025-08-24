from discord.ext import commands

from app.core.settings import settings


def setup_commands(bot: commands.Bot):
    @bot.command(name="ping")
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"Pong! 🏓 Latency: {latency}ms")

    @bot.command(name="check_channel")
    async def check_channel(ctx):
        current_id = ctx.channel.id
        is_monitored = current_id == settings.MONITORED_CHANNEL_ID

        await ctx.send(
            f"**Channel Check:**\n"
            f"Current channel ID: `{current_id}`\n"
            f"Monitored channel ID: `{settings.MONITORED_CHANNEL_ID}`\n"
            f"Is monitored: `{is_monitored}`\n\n"
            f"{'✅ This channel will auto-reply!' if is_monitored else '❌ This channel requires mentions.'}"
        )
