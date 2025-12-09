"""
Unit tests for callback_chat_target module.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pyrit.models import Message, MessagePiece
from pyrit.memory.central_memory import CentralMemory
from pyrit.memory.sqlite_memory import SQLiteMemory

SQLiteMemory._instances.pop(SQLiteMemory, None)
CentralMemory.set_memory_instance(SQLiteMemory(db_path=":memory:"))

from azure.ai.evaluation.red_team._callback_chat_target import _CallbackChatTarget


@pytest.fixture(scope="function")
def mock_callback():
    """Mock callback for tests."""
    return AsyncMock(
        return_value={
            "messages": [{"role": "user", "content": "test prompt"}, {"role": "assistant", "content": "test response"}],
            "stream": False,
            "session_state": None,
            "context": {},
        }
    )


@pytest.fixture(scope="function")
def chat_target(mock_callback):
    """Create a _CallbackChatTarget instance for tests."""
    return _CallbackChatTarget(callback=mock_callback)


@pytest.fixture(scope="function")
def mock_message():
    """Create a Message object compatible with the new PyRIT API."""
    request_piece = MessagePiece(
        role="user",
        original_value="test prompt",
        converted_value="test prompt",
        conversation_id="test-id",
    )
    request_piece.labels = {}
    return Message([request_piece])


@pytest.mark.unittest
class TestCallbackChatTargetInitialization:
    """Test the initialization of _CallbackChatTarget."""

    def test_init(self, mock_callback):
        """Test the initialization of _CallbackChatTarget."""
        target = _CallbackChatTarget(callback=mock_callback)

        assert target._callback == mock_callback
        assert target._stream is False

        # Test with stream=True
        target_with_stream = _CallbackChatTarget(callback=mock_callback, stream=True)
        assert target_with_stream._stream is True


@pytest.mark.unittest
class TestCallbackChatTargetPrompts:
    """Test _CallbackChatTarget prompt handling."""

    @pytest.mark.asyncio
    async def test_send_prompt_async(self, chat_target, mock_message, mock_callback):
        """Test send_prompt_async method."""
        with patch.object(chat_target, "_memory") as mock_memory, patch(
            "azure.ai.evaluation.red_team._callback_chat_target.construct_response_from_request"
        ) as mock_construct:
            # Setup memory mock
            mock_memory.get_chat_messages_with_conversation_id.return_value = []

            # Setup construct_response mock
            mock_construct.return_value = mock_message

            # Call the method
            response = await chat_target.send_prompt_async(message=mock_message)

            # Check that callback was called with correct parameters
            mock_callback.assert_called_once()
            call_args = mock_callback.call_args[1]
            assert call_args["stream"] is False
            assert call_args["session_state"] is None
            assert call_args["context"] == {}

            # Check memory usage
            mock_memory.get_chat_messages_with_conversation_id.assert_called_once_with(conversation_id="test-id")

    @pytest.mark.asyncio
    async def test_send_prompt_async_with_context_from_labels(self, chat_target, mock_callback):
        """Test send_prompt_async method with context from request labels."""
        # Create a request with context in labels
        request_piece = MessagePiece(
            role="user",
            original_value="test prompt",
            converted_value="test prompt",
            conversation_id="test-id",
        )
        request_piece.labels = {"context": {"contexts": ["test context data"]}}
        mock_message = Message([request_piece])

        with patch.object(chat_target, "_memory") as mock_memory, patch(
            "azure.ai.evaluation.red_team._callback_chat_target.construct_response_from_request"
        ) as mock_construct:
            # Setup memory mock
            mock_memory.get_chat_messages_with_conversation_id.return_value = []

            # Setup construct_response mock
            mock_construct.return_value = mock_message

            # Call the method
            response = await chat_target.send_prompt_async(message=mock_message)

            # Check that callback was called with correct parameters including context from labels
            mock_callback.assert_called_once()
            call_args = mock_callback.call_args[1]
            assert call_args["stream"] is False
            assert call_args["session_state"] is None
            assert call_args["context"] == {"contexts": ["test context data"]}

            # Check memory usage
            mock_memory.get_chat_messages_with_conversation_id.assert_called_once_with(conversation_id="test-id")

    def test_validate_request_multiple_pieces(self, chat_target):
        """Test _validate_request with multiple request pieces."""
        pieces = [
            MessagePiece(role="user", original_value="a", conversation_id="test", sequence=0),
            MessagePiece(role="user", original_value="b", conversation_id="test", sequence=0),
        ]
        mock_message = Message(pieces)

        with pytest.raises(ValueError) as excinfo:
            chat_target._validate_request(message=mock_message)

        assert "only supports a single prompt request piece" in str(excinfo.value)

    def test_validate_request_non_text_type(self, chat_target):
        """Test _validate_request with non-text data type."""
        mock_piece = MessagePiece(role="user", original_value="img", original_value_data_type="image_path")
        mock_message = Message([mock_piece])

        with pytest.raises(ValueError) as excinfo:
            chat_target._validate_request(message=mock_message)

        assert "only supports text prompt input" in str(excinfo.value)


@pytest.mark.unittest
class TestCallbackChatTargetFeatures:
    """Test _CallbackChatTarget feature support."""

    def test_is_json_response_supported(self, chat_target):
        """Test is_json_response_supported method."""
        assert chat_target.is_json_response_supported() is False
