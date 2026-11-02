"""
Unit Tests for Preprocessing and Normalization Module
"""

import pytest
import pandas as pd
from src.preprocessing import clean_text, normalize_label, label_to_string, preprocess_dataset


def test_clean_text_basic():
    raw = "  Hello  WORLD!!   Check this out.  "
    cleaned = clean_text(raw)
    assert "hello world" in cleaned
    assert "  " not in cleaned
    assert cleaned.islower()


def test_clean_text_special_tokens():
    raw = "Visit https://secure-bank.xyz/login or email support@bank.com. Win £500 or $1000! Call 0800123456 now."
    cleaned = clean_text(raw)
    assert "url_link" in cleaned
    assert "email_address" in cleaned
    assert "currency_symbol" in cleaned
    assert "phone_number" in cleaned


def test_clean_text_edge_cases():
    assert clean_text("") == ""
    assert clean_text(None) == ""
    assert clean_text(123) == "123"
    assert clean_text(12345) == "phone_number"


def test_normalize_label():
    assert normalize_label("spam") == 1
    assert normalize_label("SPAM") == 1
    assert normalize_label("1") == 1
    assert normalize_label(1) == 1
    assert normalize_label("fraud") == 1

    assert normalize_label("ham") == 0
    assert normalize_label("HAM") == 0
    assert normalize_label("0") == 0
    assert normalize_label(0) == 0
    assert normalize_label("legit") == 0

    assert normalize_label("unknown_value") is None
    assert normalize_label(None) is None


def test_label_to_string():
    assert label_to_string(1) == "SPAM"
    assert label_to_string(0) == "NOT SPAM"


def test_preprocess_dataset():
    data = {
        "v1": ["ham", "spam", "ham", None, "invalid", "ham"],
        "v2": ["Hello friend", "Claim your prize!", "Are you free?", "Missing label", "Invalid label", "Hello friend"]
    }
    df = pd.DataFrame(data)

    cleaned_df, report = preprocess_dataset(df, text_col="v2", label_col="v1", drop_duplicates=True)
    assert len(cleaned_df) == 3
    assert report["missing_label_removed"] == 1
    assert report["unrecognized_labels_removed"] == 1
    assert report["duplicates_detected"] == 1
    assert "clean_text" in cleaned_df.columns
    assert "label" in cleaned_df.columns
