from langfuse import get_client

from app.discord.bot import create_bot, run_bot
from app.discord.commands import setup_commands
from app.discord.events import setup_events


def main():
    bot = create_bot()

    setup_events(bot)
    setup_commands(bot)

    run_bot(bot)


if __name__ == "__main__":
    langfuse = get_client()
    langfuse.auth_check()
    main()
