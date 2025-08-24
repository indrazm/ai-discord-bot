from discord.ext import commands

from .handler import DiscordEventHandler


def setup_events(bot: commands.Bot):
    handler = DiscordEventHandler(bot)

    bot.event(handler.on_ready)
    bot.event(handler.on_message)
