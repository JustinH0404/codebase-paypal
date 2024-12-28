from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class SlackMessageRetrieverTool(BaseTool):
    """Tool for retrieving messages from Slack channels."""
    
    name: str = "slack_message_retriever"
    description: str = "Retrieves messages from a Slack channel using channel ID and optional timestamp"
    slack_token: str = Field(..., description="Slack Bot User OAuth Token")
    _client: Optional[WebClient] = None

    class Config:
        arbitrary_types_allowed = True
        
    def __init__(self, slack_token: str):
        super().__init__(slack_token=slack_token)
        if not self._client:
            self._client = WebClient(token=slack_token)
    
    def _run(self, channel_id: str, thread_ts: Optional[str] = None, limit: int = 100) -> str:
        """
        Retrieve messages from a Slack channel.
        
        Args:
            channel_id (str): The ID of the channel to retrieve messages from
            thread_ts (str, optional): Timestamp of the parent message to retrieve thread
            limit (int): Maximum number of messages to retrieve (default: 100)
            
        Returns:
            str: Formatted string containing the retrieved messages
        """
        try:
            # Get channel messages
            result = self._client.conversations_history(
                channel=channel_id,
                limit=limit,
                thread_ts=thread_ts if thread_ts else None
            )
            
            # Format messages
            messages = []
            for msg in result["messages"]:
                if "user" not in msg:
                    continue
                    
                user_info = self._client.users_info(user=msg["user"])["user"]
                messages.append({
                    "timestamp": msg.get("ts", ""),
                    "username": user_info["real_name"],
                    "text": msg.get("text", ""),
                    "user_id": msg["user"]
                })
            
            return self._format_messages(messages)
            
        except SlackApiError as e:
            return f"Error retrieving messages: {str(e)}"
    
    def _format_messages(self, messages: list[dict]) -> str:
        """
        Format a list of messages into a readable string.
        """
        return "\n".join(
            f"{msg['username']} ({msg['timestamp']}): {msg['text']}"
            for msg in messages
        )
    
    def _arun(self, channel_id: str, thread_ts: Optional[str] = None, limit: int = 100) -> str:
        """Async implementation can be added here if needed"""
        raise NotImplementedError("Async implementation not available")
