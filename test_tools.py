import pytest
from unittest.mock import MagicMock
from tools import SlackRetrievalTool

@pytest.fixture
def slack_tool():
    """Fixture for the SlackRetrievalTool with a mocked WebClient."""
    tool = SlackRetrievalTool(token="fake-token")
    tool.client.conversations_history = MagicMock()
    return tool

def test_tool_success(slack_tool):
    """Test successful tool execution."""
    channel_id = "C12345678"
    message_ts = "1618081234.56789"
    
    # Mock response
    slack_tool.client.conversations_history.return_value = {
        "messages": [{"text": "Hello, CrewAI!", "ts": message_ts}],
    }
    
    result = slack_tool.run(channel_id, message_ts)
    assert result == "Hello, CrewAI!"

def test_tool_no_message(slack_tool):
    """Test tool when no message is retrieved."""
    channel_id = "C12345678"
    message_ts = "1618081234.56789"
    
    # Mock response with no messages
    slack_tool.client.conversations_history.return_value = {"messages": []}
    
    result = slack_tool.run(channel_id, message_ts)
    assert result == "No message found for the given timestamp."

def test_tool_error_handling(slack_tool):
    """Test tool error handling."""
    channel_id = "C12345678"
    message_ts = "1618081234.56789"
    
    # Simulate API error
    slack_tool.client.conversations_history.side_effect = Exception("API Error")
    
    result = slack_tool.run(channel_id, message_ts)
    assert "Error retrieving message: API Error" in result
