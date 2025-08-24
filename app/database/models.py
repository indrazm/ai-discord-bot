from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, SQLModel


class ConversationHistory(SQLModel, table=True):
    """Model for storing Discord conversation history using runner.to_input_list() format"""

    __tablename__ = "conversation_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    discord_channel_id: str = Field(index=True)  # Discord channel or thread ID
    discord_guild_id: str = Field(index=True)  # Discord server ID
    discord_user_id: str = Field(index=True)  # User who started the conversation
    conversation_name: Optional[str] = Field(default=None)  # Optional conversation name

    # Store the full conversation history as JSON (runner.to_input_list() format)
    # This will be a list of {"role": "user|assistant", "content": "message"} objects
    messages: List[Dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)  # Whether conversation is still active

    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation history"""
        self.messages.append({"role": role, "content": content})
        self.updated_at = datetime.utcnow()

    def get_input_list(self) -> List[Dict[str, Any]]:
        """Get the conversation history in runner.to_input_list() format"""
        return self.messages.copy()

    def clear_history(self) -> None:
        """Clear all messages from the conversation"""
        self.messages = []
        self.updated_at = datetime.utcnow()

    def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """Get the last n messages from the conversation"""
        return self.messages[-n:] if n > 0 else []
