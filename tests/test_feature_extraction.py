"""
Unit Tests for Feature Extraction Pipelines
"""

import pytest
from src.feature_extraction import FeaturePipeline


def test_tfidf_pipeline():
    corpus = [
        "Congratulations! You won a free lottery prize.",
        "Are we meeting for lunch at campus?",
        "URGENT: Claim your free lottery reward now.",
        "Your appointment is confirmed."
    ]
    pipe = FeaturePipeline(vectorizer_type="tfidf", ngram_range=(1, 2), max_features=100, min_df=1)
    matrix = pipe.fit_transform(corpus)
    assert matrix.shape[0] == 4
    assert matrix.shape[1] > 0
    assert pipe.is_fitted is True

    # Transform new document
    test_vec = pipe.transform(["Free prize winner"])
    assert test_vec.shape[0] == 1
    assert test_vec.shape[1] == matrix.shape[1]


def test_count_pipeline():
    corpus = [
        "Win cash prizes and free phones",
        "Hello mom I will be late with cash"
    ]
    pipe = FeaturePipeline(vectorizer_type="count", ngram_range=(1, 1), max_features=50, min_df=1)
    matrix = pipe.fit_transform(corpus)
    assert matrix.shape[0] == 2
    assert "cash" in pipe.get_feature_names()


def test_unfitted_transform_error():
    pipe = FeaturePipeline(vectorizer_type="tfidf")
    with pytest.raises(RuntimeError):
        pipe.transform(["Some un-vectorized text"])
