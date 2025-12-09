import logging
import unittest.mock as mock

import pytest

try:
    import pyrit

    has_pyrit = True
except ImportError:
    has_pyrit = False

if has_pyrit:
    from azure.ai.evaluation.red_team._utils._rai_service_true_false_scorer import AzureRAIServiceTrueFalseScorer
    from azure.ai.evaluation.red_team._attack_objective_generator import RiskCategory
    from pyrit.models import Message, MessagePiece, Score, UnvalidatedScore
    from pyrit.memory.central_memory import CentralMemory
    from pyrit.memory.sqlite_memory import SQLiteMemory

    SQLiteMemory._instances.pop(SQLiteMemory, None)
    CentralMemory.set_memory_instance(SQLiteMemory(db_path=":memory:"))

# Mocks
MockGeneratedRAIClient = mock.Mock()
MockCredential = mock.Mock()
MockAzureAIProject = mock.Mock()
MockLogger = mock.Mock(spec=logging.Logger)
MockRAIServiceEvalChatTarget = mock.Mock()


@pytest.fixture
def mock_message_piece():
    return MessagePiece(
        role="assistant",
        original_value="Response to score",
        converted_value="Response to score",
        conversation_id="score_conv_id",
        sequence=2,
        original_value_data_type="text",
        converted_value_data_type="text",
        id="test_piece_id",
        labels={"context": "scoring context", "objective": "Evaluate for sexual content"},
        attack_identifier={"attack": "id"},
    )


@pytest.fixture
def mock_message(mock_message_piece):
    return Message([mock_message_piece])


@pytest.fixture
@mock.patch(
    "azure.ai.evaluation.red_team._utils._rai_service_true_false_scorer.RAIServiceEvalChatTarget",
    return_value=MockRAIServiceEvalChatTarget,
)
def true_false_scorer(mock_chat_target):
    """Fixture to create an instance of the scorer."""
    scorer = AzureRAIServiceTrueFalseScorer(
        client=MockGeneratedRAIClient,
        risk_category=RiskCategory.Sexual,
        credential=MockCredential,
        azure_ai_project=MockAzureAIProject,
        logger=MockLogger,
    )
    # Reset mock calls for each test
    MockLogger.reset_mock()
    mock_chat_target.reset_mock()
    MockRAIServiceEvalChatTarget.reset_mock()  # Reset the instance mock as well
    MockRAIServiceEvalChatTarget.context = None
    return scorer


@pytest.mark.asyncio
@mock.patch.object(AzureRAIServiceTrueFalseScorer, "_score_value_with_llm")
async def test_score_async_success(mock_score_llm, true_false_scorer, mock_message, mock_message_piece):
    """Tests the successful scoring flow."""
    mock_task = "Evaluate for sexual content"
    mock_unvalidated_score = UnvalidatedScore(
        raw_score_value="true",
        score_value_description="test_description",
        score_category=["test_category"],
        score_rationale="Detected explicit content.",
        score_metadata={"meta": "data"},
        scorer_class_identifier=true_false_scorer.get_identifier(),
        message_piece_id="test_piece_id",
        objective=mock_task,
    )
    mock_score_llm.return_value = mock_unvalidated_score

    scores = await true_false_scorer.score_async(mock_message, objective=mock_task)
    mock_score_llm.assert_called_once_with(
        prompt_target=MockRAIServiceEvalChatTarget,
        system_prompt="Please evaluate the following response.",
        message_value="Response to score",
        message_data_type="text",
        scored_prompt_id="test_piece_id",
        objective=mock_task,
        attack_identifier={"attack": "id"},
    )

    assert len(scores) == 1
    score = scores[0]
    assert isinstance(score, Score)
    assert score.score_value == "true"
    assert score.score_rationale == "Detected explicit content."
    assert score.score_metadata == {"meta": "data"}
    assert score.scorer_class_identifier["__type__"] == "AzureRAIServiceTrueFalseScorer"
    MockLogger.info.assert_called_with("Starting to score prompt response")
    assert MockRAIServiceEvalChatTarget.context == "scoring context"


def test_validate_return_scores_no_error(true_false_scorer):
    """Tests that validate_return_scores allows matching score types."""
    score = Score(
        score_value="true",
        score_value_description="desc",
        score_type="true_false",
        score_category=["test_category"],
        score_rationale="",
        score_metadata={},
        message_piece_id="piece-id",
        scorer_class_identifier={"__type__": "AzureRAIServiceTrueFalseScorer"},
    )
    try:
        true_false_scorer.validate_return_scores([score])
    except Exception as e:
        pytest.fail(f"validate_return_scores raised an exception unexpectedly: {e}")


# Add more tests if validate logic becomes more complex
