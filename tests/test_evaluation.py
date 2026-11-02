"""
Unit Tests for Evaluation Metrics Module
"""

import pytest
import numpy as np
from src.evaluation import compute_metrics


def test_compute_metrics():
    y_true = [0, 0, 1, 1, 0, 1, 0, 0]
    y_pred = [0, 0, 1, 1, 0, 0, 0, 1]  # 1 FN, 1 FP, 4 TN, 2 TP
    y_prob = np.array([
        [0.9, 0.1],
        [0.8, 0.2],
        [0.1, 0.9],
        [0.2, 0.8],
        [0.7, 0.3],
        [0.6, 0.4],
        [0.85, 0.15],
        [0.4, 0.6]
    ])

    metrics = compute_metrics(y_true, y_pred, y_prob)

    assert metrics["accuracy"] == 0.75  # 6/8
    assert metrics["true_positives"] == 2
    assert metrics["true_negatives"] == 4
    assert metrics["false_positives"] == 1
    assert metrics["false_negatives"] == 1
    assert metrics["precision"] == round(2 / 3, 4)
    assert metrics["recall"] == round(2 / 3, 4)
    assert metrics["f1_score"] == round(2 / 3, 4)
    assert metrics["roc_auc"] is not None
    assert metrics["roc_curve_data"] is not None
