"""
Unit Tests for Dataset Loading and Schema Inference Module
"""

import io
import pytest
import pandas as pd
from src.data_loader import detect_columns, read_data_file, get_dataset_summary


def test_detect_columns_standard():
    df1 = pd.DataFrame({"v1": ["ham", "spam"], "v2": ["hello", "free money"]})
    label_col, text_col = detect_columns(df1)
    assert label_col == "v1"
    assert text_col == "v2"

    df2 = pd.DataFrame({"category": ["ham", "spam"], "message": ["hey", "win cash"]})
    l_col, t_col = detect_columns(df2)
    assert l_col == "category"
    assert t_col == "message"


def test_read_data_file_csv():
    csv_content = io.StringIO("label,text\nham,Hello there\nspam,Win cash now\n")
    df = read_data_file(csv_content)
    assert len(df) == 2
    assert "label" in df.columns
    assert "text" in df.columns


def test_get_dataset_summary():
    df = pd.DataFrame({
        "label": ["ham", "spam", "spam", "ham", None],
        "text": ["hello", "win prize", "claim cash", "see you tomorrow", "missing label"]
    })
    summary = get_dataset_summary(df, label_col="label", text_col="text")
    assert summary["total_rows"] == 5
    assert summary["spam_records"] == 2
    assert summary["ham_records"] == 2
    assert summary["missing_label_values"] == 1
    assert summary["is_valid"] is True
