from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlmodel import select

from app.database.connection import get_db_session
from app.database.models import ConversationHistory


class ConversationService:
    """Service layer for managing conversation history using runner.to_input_list() format"""

    @staticmethod
    def create_or_get_conversation(
        discord_channel_id: str, discord_guild_id: str, discord_user_id: str, conversation_name: Optional[str] = None
    ) -> ConversationHistory:
        """Create a new conversation or get existing one"""
        with get_db_session() as session:
            # Check if conversation already exists for this channel
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            existing_conversation = session.exec(statement).first()

            if existing_conversation:
                return existing_conversation

            # Create new conversation
            new_conversation = ConversationHistory(
                discord_channel_id=discord_channel_id,
                discord_guild_id=discord_guild_id,
                discord_user_id=discord_user_id,
                conversation_name=conversation_name or f"Chat-{discord_channel_id}",
            )

            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            return new_conversation

    @staticmethod
    def get_conversation_by_channel_id(discord_channel_id: str) -> Optional[ConversationHistory]:
        """Get conversation by Discord channel ID"""
        with get_db_session() as session:
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            return session.exec(statement).first()

    @staticmethod
    def get_conversation_by_id(conversation_id: int) -> Optional[ConversationHistory]:
        """Get conversation by ID"""
        with get_db_session() as session:
            return session.get(ConversationHistory, conversation_id)

    @staticmethod
    def add_message(discord_channel_id: str, role: str, content: str) -> Optional[ConversationHistory]:
        """Add a message to conversation"""
        with get_db_session() as session:
            # Get the conversation
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            conversation = session.exec(statement).first()

            if not conversation:
                return None

            # Add the message
            conversation.add_message(role, content)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation

    @staticmethod
    def get_conversation_history(discord_channel_id: str) -> List[Dict[str, Any]]:
        """Get conversation history in runner.to_input_list() format"""
        with get_db_session() as session:
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            conversation = session.exec(statement).first()

            if conversation:
                return conversation.get_input_list()
            return []

    @staticmethod
    def update_conversation_history(discord_channel_id: str, messages: list[dict]) -> bool:
        """Update the entire conversation history for a channel."""
        with get_db_session() as session:
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            conversation = session.exec(statement).first()

            if conversation:
                conversation.messages = messages
                conversation.updated_at = datetime.utcnow()
                session.add(conversation)
                session.commit()
                return True
            return False

    @staticmethod
    def update_conversation_with_history(
        discord_channel_id: str, messages: List[Dict[str, Any]]
    ) -> Optional[ConversationHistory]:
        """Update conversation with full message history from runner.to_input_list()"""
        with get_db_session() as session:
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            conversation = session.exec(statement).first()

            if not conversation:
                return None

            # Update the entire message history
            conversation.messages = messages
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation

    @staticmethod
    def get_recent_conversations(discord_guild_id: str, limit: int = 10) -> List[ConversationHistory]:
        """Get recent active conversations for a guild"""
        with get_db_session() as session:
            statement = (
                select(ConversationHistory)
                .where(ConversationHistory.discord_guild_id == discord_guild_id, ConversationHistory.is_active)
                .order_by(ConversationHistory.updated_at.desc())
                .limit(limit)
            )

            return list(session.exec(statement).all())

    @staticmethod
    def deactivate_conversation(conversation_id: int) -> bool:
        """Deactivate a conversation"""
        with get_db_session() as session:
            conversation = session.get(ConversationHistory, conversation_id)
            if conversation:
                conversation.is_active = False
                conversation.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False

    @staticmethod
    def clear_conversation_history(discord_channel_id: str) -> bool:
        """Clear all messages from a conversation"""
        with get_db_session() as session:
            statement = select(ConversationHistory).where(
                ConversationHistory.discord_channel_id == discord_channel_id, ConversationHistory.is_active
            )
            conversation = session.exec(statement).first()

            if conversation:
                conversation.clear_history()
                session.add(conversation)
                session.commit()
                return True
            return False
