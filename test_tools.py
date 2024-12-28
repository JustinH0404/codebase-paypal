import pytest
from unittest.mock import Mock
from slack_sdk.errors import SlackApiError
from tools import SlackMessageRetrieverTool

@pytest.fixture
def mock_client():
    """Create a mock Slack client"""
    client = Mock()
    
    # Set up default successful responses
    client.conversations_history.return_value = {
        "messages": [
            {
                "user": "U123",
                "ts": "1234567890.123456",
                "text": "Hello world!"
            }
        ]
    }
    
    client.users_info.return_value = {
        "user": {
            "real_name": "John Doe"
        }
    }
    
    return client

@pytest.fixture
def tool(mock_client):
    """Create a tool instance with the mock client"""
    tool = SlackMessageRetrieverTool("fake-token")
    tool._client = mock_client  # Inject the mock client
    return tool

def test_run_success(tool, mock_client):
    result = tool._run("C123")
    
    assert "John Doe (1234567890.123456): Hello world!" in result
    mock_client.conversations_history.assert_called_once_with(
        channel="C123",
        limit=100,
        thread_ts=None
    )
    mock_client.users_info.assert_called_once_with(user="U123")