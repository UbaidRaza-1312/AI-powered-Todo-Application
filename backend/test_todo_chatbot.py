"""
Test suite for the updated Todo Chatbot with MCP Integration
Tests the system prompt requirements and functionality
"""
import asyncio
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.chat_agent import ChatAgent
from src.mcp.server import mcp_server
from src.models.message import Message
from src.db.database import get_session_maker


@pytest.fixture
def mock_user_context():
    """Provides a valid user context for testing"""
    return {
        "user_id": str(uuid.uuid4()),
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def invalid_user_context():
    """Provides an invalid user context for testing"""
    return {
        "user_id": "",  # Empty user_id
        "name": "",
        "email": ""
    }


@pytest.mark.asyncio
async def test_user_context_validation_missing():
    """Test that the chatbot validates user context exists"""
    chat_agent = ChatAgent()

    # Mock the database session to avoid actual DB operations
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value

        # Test with missing user_id
        result = await chat_agent.process_message("", "add task Buy milk", str(uuid.uuid4()))

        assert "Missing user context" in result["response"]


@pytest.mark.asyncio
async def test_user_context_validation_invalid():
    """Test that the chatbot validates user_id format"""
    chat_agent = ChatAgent()

    # Mock the database session to avoid actual DB operations
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value

        # Test with invalid user_id format
        result = await chat_agent.process_message("invalid-uuid-format", "add task Buy milk", str(uuid.uuid4()))

        assert "Invalid user context" in result["response"]


@pytest.mark.asyncio
async def test_user_context_validation_valid():
    """Test that the chatbot accepts valid user context"""
    chat_agent = ChatAgent()

    # Mock the database session and MCP tools to avoid actual DB operations
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "task_id": str(uuid.uuid4()),
                "message": "Task 'Buy milk' created successfully"
            }
        }

        # Test with valid user_id
        valid_user_id = str(uuid.uuid4())
        result = await chat_agent.process_message(valid_user_id, "add task Buy milk", str(uuid.uuid4()))

        # The response should not contain error messages about user context
        assert "Missing user context" not in result["response"]
        assert "Invalid user context" not in result["response"]


@pytest.mark.asyncio
async def test_add_task_operation(mock_user_context):
    """Test adding a task via the chatbot"""
    chat_agent = ChatAgent()

    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "task_id": str(uuid.uuid4()),
                "message": "Task 'Buy milk' created successfully"
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            "add task Buy milk",
            str(uuid.uuid4())
        )

        # Verify the tool was called with the correct parameters
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[0][0] == "add_task"  # First argument is tool name
        assert call_args[1]["user_id"] == mock_user_context["user_id"]  # user_id was passed
        assert call_args[1]["title"] == "Buy milk"  # title was extracted

        # Verify the response
        assert "Task 'Buy milk' created successfully" in result["response"]


@pytest.mark.asyncio
async def test_view_all_tasks_operation(mock_user_context):
    """Test viewing all tasks via the chatbot"""
    chat_agent = ChatAgent()

    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "tasks": [
                    {
                        "id": str(uuid.uuid4()),
                        "title": "Buy milk",
                        "description": "Get whole milk from store",
                        "completed": False,
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00"
                    }
                ]
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            "view all tasks",
            str(uuid.uuid4())
        )

        # Verify the tool was called with the correct parameters
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[0][0] == "list_tasks"  # First argument is tool name
        assert call_args[1]["user_id"] == mock_user_context["user_id"]  # user_id was passed

        # Verify the response
        assert "Buy milk" in result["response"]


@pytest.mark.asyncio
async def test_view_single_task_operation(mock_user_context):
    """Test viewing a single task via the chatbot"""
    chat_agent = ChatAgent()

    task_id = str(uuid.uuid4())
    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "task": {
                    "id": task_id,
                    "title": "Buy milk",
                    "description": "Get whole milk from store",
                    "completed": False,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                }
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            f"view task {task_id}",
            str(uuid.uuid4())
        )

        # Verify the tool was called with the correct parameters
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[0][0] == "get_task"  # First argument is tool name
        assert call_args[1]["user_id"] == mock_user_context["user_id"]  # user_id was passed
        assert call_args[1]["task_id"] == task_id  # task_id was passed

        # Verify the response
        assert "Buy milk" in result["response"]


@pytest.mark.asyncio
async def test_update_task_operation(mock_user_context):
    """Test updating a task via the chatbot"""
    chat_agent = ChatAgent()

    task_id = str(uuid.uuid4())
    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "updated_task": {
                    "id": task_id,
                    "title": "Buy almond milk",
                    "description": "Get whole milk from store",
                    "completed": False,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                },
                "message": "Task updated successfully"
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            f"edit task {task_id} change title to Buy almond milk",
            str(uuid.uuid4())
        )

        # Verify the tool was called with the correct parameters
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[0][0] == "update_task"  # First argument is tool name
        assert call_args[1]["user_id"] == mock_user_context["user_id"]  # user_id was passed
        assert call_args[1]["task_id"] == task_id  # task_id was passed
        assert call_args[1]["title"] == "Buy almond milk"  # title was updated

        # Verify the response
        assert "Task updated successfully" in result["response"]


@pytest.mark.asyncio
async def test_delete_task_operation(mock_user_context):
    """Test deleting a task via the chatbot"""
    chat_agent = ChatAgent()

    task_id = str(uuid.uuid4())
    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": True,
                "message": f"Task 'Buy milk' deleted successfully"
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            f"delete task {task_id}",
            str(uuid.uuid4())
        )

        # Verify the tool was called with the correct parameters
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[0][0] == "delete_task"  # First argument is tool name
        assert call_args[1]["user_id"] == mock_user_context["user_id"]  # user_id was passed
        assert call_args[1]["task_id"] == task_id  # task_id was passed

        # Verify the response
        assert "deleted successfully" in result["response"]


@pytest.mark.asyncio
async def test_task_ownership_verification(mock_user_context):
    """Test that the chatbot verifies task ownership before operations"""
    chat_agent = ChatAgent()

    task_id = str(uuid.uuid4())
    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        # Simulate the case where the task doesn't belong to the user
        mock_execute.return_value = {
            "success": True,
            "result": {
                "success": False,
                "error": "Task not found or does not belong to user"
            }
        }

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            f"edit task {task_id} change title",
            str(uuid.uuid4())
        )

        # Verify the response contains the appropriate error
        assert "does not belong to user" in result["response"]


@pytest.mark.asyncio
async def test_empty_message_handling(mock_user_context):
    """Test handling of empty messages"""
    chat_agent = ChatAgent()

    # Mock the database session to avoid actual DB operations
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            "",  # Empty message
            str(uuid.uuid4())
        )

        # Verify the response for empty message
        assert "didn't receive any message" in result["response"]


@pytest.mark.asyncio
async def test_error_handling_in_tool_execution(mock_user_context):
    """Test error handling when tool execution fails"""
    chat_agent = ChatAgent()

    # Mock the database session and MCP tools
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker, \
         patch.object(mcp_server, 'execute_tool', side_effect=Exception("Tool execution failed")):

        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value

        result = await chat_agent.process_message(
            mock_user_context["user_id"],
            "add task Buy milk",
            str(uuid.uuid4())
        )

        # Verify the response contains error information
        assert "encountered an error" in result["response"]
        assert "Tool execution failed" in result["response"]