import discord
from discord.ext import commands

from app.core.settings import settings


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot


def run_bot(bot: commands.Bot) -> None:
    bot.run(settings.DISCORD_TOKEN)
