"""
Unit Tests for Prediction Service Module
Validates predictions on representative Spam and Ham benchmark cases.
"""

import pytest
import pandas as pd
from src.prediction import SpamClassifierService


@pytest.fixture(scope="module")
def classifier_service():
    """Ensure service is initialized with trained model."""
    service = SpamClassifierService.get_instance(force_reload=True)
    assert service.is_model_ready(), "Model must be trained prior to testing predictions"
    return service


def test_prediction_spam_prize(classifier_service):
    """SPAM EXAMPLE 1: Prize lure message."""
    text = "Congratulations! You have won a free prize. Claim your reward now!"
    result = classifier_service.predict_single(text, message_type="SMS", log_to_db=False)
    assert result["is_spam"] is True
    assert result["label"] == "SPAM"
    assert result["confidence"] > 0.70
    assert result["spam_probability"] > result["ham_probability"]


def test_prediction_ham_college(classifier_service):
    """HAM EXAMPLE 1: Casual student conversation."""
    text = "Hi, are we meeting at college today?"
    result = classifier_service.predict_single(text, message_type="SMS", log_to_db=False)
    assert result["is_spam"] is False
    assert result["label"] == "NOT SPAM"
    assert result["confidence"] > 0.70
    assert result["ham_probability"] > result["spam_probability"]


def test_prediction_spam_lottery(classifier_service):
    """SPAM EXAMPLE 2: Urgent lottery phishing with links."""
    text = "URGENT! You have won a lottery. Click here to claim your cash prize."
    result = classifier_service.predict_single(text, message_type="SMS", log_to_db=False)
    assert result["is_spam"] is True
    assert result["label"] == "SPAM"
    assert result["confidence"] > 0.70
    assert result["heuristics"]["threat_score"] > 0


def test_prediction_ham_appointment(classifier_service):
    """HAM EXAMPLE 2: Legitimate appointment confirmation."""
    text = "Your appointment is confirmed for tomorrow."
    result = classifier_service.predict_single(text, message_type="SMS", log_to_db=False)
    assert result["is_spam"] is False
    assert result["label"] == "NOT SPAM"
    assert result["confidence"] > 0.70


def test_prediction_empty_message(classifier_service):
    """Input validation: empty messages must raise ValueError."""
    with pytest.raises(ValueError):
        classifier_service.predict_single("", message_type="SMS")

    with pytest.raises(ValueError):
        classifier_service.predict_single("   ", message_type="SMS")


def test_bulk_prediction(classifier_service):
    """Test batch classification on DataFrame."""
    df = pd.DataFrame({
        "msg_id": [1, 2, 3],
        "content": [
            "WINNER! Free vacation package to Bahamas. Call now to claim prize!",
            "Can you pick up groceries on the way home?",
            "URGENT! You have won a £2,000 cash prize. Call 09061743813 now to claim."
        ]
    })
    result_df = classifier_service.predict_bulk(df, text_col="content", log_to_db=False)
    assert "Prediction" in result_df.columns
    assert "Confidence" in result_df.columns
    assert "Spam_Probability" in result_df.columns
    assert len(result_df) == 3
    assert result_df.iloc[0]["Prediction"] == "SPAM"
    assert result_df.iloc[1]["Prediction"] == "NOT SPAM"
    assert result_df.iloc[2]["Prediction"] == "SPAM"
