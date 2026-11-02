"""
Unit Tests for Model Training Pipeline
"""

import pytest
import pandas as pd
from src.model_training import train_model, load_saved_metrics
from config import MODEL_FILE, VECTORIZER_FILE, METRICS_FILE


def test_train_model_artifacts_created():
    result = train_model(
        vectorizer_type="tfidf",
        ngram_range=(1, 2),
        max_features=1000,
        min_df=2,
        alpha=0.1
    )

    assert result["status"] == "success"
    assert MODEL_FILE.exists()
    assert VECTORIZER_FILE.exists()
    assert METRICS_FILE.exists()

    metrics = result["test_metrics"]
    assert 0.85 <= metrics["accuracy"] <= 1.0
    assert 0.80 <= metrics["precision"] <= 1.0
    assert 0.75 <= metrics["recall"] <= 1.0
    assert 0.80 <= metrics["f1_score"] <= 1.0
    assert len(metrics["confusion_matrix"]) == 2


def test_load_saved_metrics():
    loaded = load_saved_metrics()
    assert loaded is not None
    assert "test_metrics" in loaded
    assert "hyperparameters" in loaded
