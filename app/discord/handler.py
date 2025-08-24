from typing import List, Optional, Tuple

from discord.ext import commands
from loguru import logger

from app.core.settings import settings
from app.database.connection import init_database
from app.database.service import ConversationService
from app.llm.agent import run_agent

from .utils import send_long_message


class DiscordEventHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_ready(self):
        logger.info(f"{self.bot.user} has connected to Discord!")
        logger.info(f"Bot is in {len(self.bot.guilds)} guilds")

        try:
            init_database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        self._log_message_info(message)

        conversation_channel_id = str(message.channel.id)
        existing_conversation = self._get_existing_conversation(conversation_channel_id)

        if existing_conversation:
            await self._handle_existing_conversation(message, conversation_channel_id)

        if self.bot.user in message.mentions:
            await self._handle_mention(message)

        await self.bot.process_commands(message)

    def _log_message_info(self, message):
        parent_channel_id = (
            getattr(message.channel, "parent_id", None) if hasattr(message.channel, "parent_id") else None
        )

        logger.info(
            f"Message received in channel ID: {message.channel.id}, monitored ID: {settings.MONITORED_CHANNEL_ID}"
        )
        logger.info(f"Parent channel ID: {parent_channel_id}")
        logger.info(f"Channel match: {message.channel.id == settings.MONITORED_CHANNEL_ID}")
        logger.info(
            f"Parent match: {parent_channel_id == settings.MONITORED_CHANNEL_ID if parent_channel_id else False}"
        )
        logger.info(f"Message content: '{message.content}'")

    def _get_existing_conversation(self, conversation_channel_id: str) -> Optional[object]:
        try:
            return ConversationService.get_conversation_by_channel_id(conversation_channel_id)
        except Exception as e:
            logger.error(f"Error checking existing conversation: {e}")
            return None

    def _extract_image_urls(self, message) -> List[str]:
        image_urls = []
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_urls.append(attachment.url)
        return image_urls

    def _clean_mention_content(self, content: str) -> str:
        return content.replace(f"<@{self.bot.user.id}>", "").replace(f"<@!{self.bot.user.id}>", "").strip()

    async def _process_agent_response(
        self, content: str, channel_id: str, image_urls: List[str], context: str = ""
    ) -> Tuple[str, List]:
        chat_messages = ConversationService.get_conversation_history(channel_id)
        logger.info(f"{context}: Got conversation context: {len(chat_messages)} messages")

        if image_urls:
            logger.info(f"Found {len(image_urls)} image(s) in message")

        response, updated_chat_messages = await run_agent(content, chat_messages, image_urls)
        logger.info(f"{context}: Got response from agent: {len(response) if response else 0} characters")

        return response, updated_chat_messages

    async def _send_and_save_response(self, channel, response: str, channel_id: str, updated_chat_messages: List):
        bot_message = await send_long_message(channel, response)
        try:
            if bot_message:
                ConversationService.update_conversation_with_history(
                    discord_channel_id=channel_id, messages=updated_chat_messages
                )
        except Exception as e:
            logger.error(f"Failed to save bot response to database: {e}")

    async def _handle_existing_conversation(self, message, conversation_channel_id: str):
        content = message.content.strip()
        image_urls = self._extract_image_urls(message)

        if content or image_urls:
            logger.info(f"Auto-replying to message in existing conversation: {content[:50]}...")

            response, updated_chat_messages = await self._process_agent_response(
                content, conversation_channel_id, image_urls, "Existing conversation"
            )

            await self._send_and_save_response(
                message.channel, response, conversation_channel_id, updated_chat_messages
            )
        else:
            logger.info("Message has no content, skipping auto-reply")

    async def _handle_mention(self, message):
        content = self._clean_mention_content(message.content)
        image_urls = self._extract_image_urls(message)

        if hasattr(message.channel, "parent") and message.channel.parent:
            await self._handle_thread_mention(message, content, image_urls)
        else:
            await self._handle_new_thread_mention(message, content, image_urls)

    async def _handle_thread_mention(self, message, content: str, image_urls: List[str]):
        channel_id = str(message.channel.id)

        try:
            ConversationService.create_or_get_conversation(
                discord_channel_id=channel_id,
                discord_guild_id=str(message.guild.id),
                discord_user_id=str(message.author.id),
            )
        except Exception as e:
            logger.error(f"Failed to create conversation: {e}")

        response, updated_chat_messages = await self._process_agent_response(content, channel_id, image_urls, "Thread")

        await self._send_and_save_response(message.channel, response, channel_id, updated_chat_messages)

    async def _handle_new_thread_mention(self, message, content: str, image_urls: List[str]):
        thread_name = f"Chat with {message.author.display_name}"
        if content:
            thread_name = f"Re: {content[:50]}..."

        thread = await message.create_thread(name=thread_name)
        thread_id = str(thread.id)

        try:
            ConversationService.create_or_get_conversation(
                discord_channel_id=thread_id,
                discord_guild_id=str(message.guild.id),
                discord_user_id=str(message.author.id),
            )
        except Exception as e:
            logger.error(f"Failed to create conversation for new thread: {e}")

        response, updated_chat_messages = await self._process_agent_response(
            content, thread_id, image_urls, "New thread"
        )

        await self._send_and_save_response(thread, response, thread_id, updated_chat_messages)
