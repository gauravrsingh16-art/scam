"""
Text Preprocessing and Normalization Module
Handles text cleaning, token normalization, duplicate detection, and label standardization.
"""

import re
import unicodedata
from typing import Tuple, Dict, Any, Optional
import pandas as pd
import numpy as np


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize input message text:
    - Handles null/NaN/non-string values
    - Unicode normalization
    - Removes HTML tags
    - Standardizes URLs and email patterns to informative tokens
    - Retains alphanumeric tokens and currency symbols ($ £ €)
    - Normalizes multiple spaces and converts to lowercase
    """
    if text is None or pd.isna(text):
        return ""

    if not isinstance(text, str):
        text = str(text)

    # Unicode normalization (NFKC)
    text = unicodedata.normalize("NFKC", text)

    # Remove HTML tags (common in spam emails)
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize URLs into recognizable tokens while retaining presence
    text = re.sub(r"https?://\S+|www\.\S+", " url_link ", text)

    # Normalize email addresses
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " email_address ", text)

    # Normalize phone numbers / shortcodes (numbers with 5+ digits)
    text = re.sub(r"\b\d{5,12}\b", " phone_number ", text)

    # Normalize currency indicators (preserving spam cues like $ £ €)
    text = re.sub(r"[£$€₹]", " currency_symbol ", text)

    # Convert to lowercase
    text = text.lower()

    # Remove unusual non-ASCII or control characters, keeping letters, numbers, spaces, and basic punctuation
    text = re.sub(r"[^\w\s_.,!?'-]", " ", text)

    # Collapse multiple whitespaces into a single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_label(label: Any) -> Optional[int]:
    """
    Normalize diverse dataset label values to binary integers:
    1 = SPAM
    0 = NOT SPAM (HAM)
    Returns None if label is unrecognized or invalid.
    """
    if label is None or pd.isna(label):
        return None

    str_val = str(label).strip().lower()

    if str_val in ["spam", "1", "1.0", "junk", "fraud", "phishing", "true"]:
        return 1
    elif str_val in ["ham", "0", "0.0", "legit", "not spam", "not_spam", "normal", "false"]:
        return 0

    return None


def label_to_string(label_int: int) -> str:
    """Convert binary integer label to human-readable string."""
    return "SPAM" if label_int == 1 else "NOT SPAM"


def preprocess_dataset(
    df: pd.DataFrame,
    text_col: str,
    label_col: str,
    drop_duplicates: bool = False
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Comprehensive dataset preprocessing:
    - Missing value detection & removal
    - Duplicate detection & optional removal
    - Label normalization
    - Text cleaning
    Returns (cleaned_df, report_dict).
    """
    initial_rows = len(df)

    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Required columns '{text_col}' or '{label_col}' not found in dataframe.")

    # Copy to avoid mutating source
    working_df = df[[label_col, text_col]].copy()
    working_df.columns = ["raw_label", "raw_text"]

    # Detect missing values
    missing_text = working_df["raw_text"].isna().sum()
    missing_label = working_df["raw_label"].isna().sum()

    # Drop missing
    working_df = working_df.dropna(subset=["raw_text", "raw_label"])

    # Detect duplicates
    duplicate_count = working_df.duplicated(subset=["raw_text"]).sum()
    if drop_duplicates and duplicate_count > 0:
        working_df = working_df.drop_duplicates(subset=["raw_text"])

    # Normalize labels
    working_df["label"] = working_df["raw_label"].apply(normalize_label)
    unrecognized_labels = working_df["label"].isna().sum()
    working_df = working_df.dropna(subset=["label"])
    working_df["label"] = working_df["label"].astype(int)

    # Clean text
    working_df["clean_text"] = working_df["raw_text"].apply(clean_text)

    # Filter out empty clean texts
    working_df = working_df[working_df["clean_text"].str.len() > 0]

    final_rows = len(working_df)
    spam_count = int((working_df["label"] == 1).sum())
    ham_count = int((working_df["label"] == 0).sum())

    report = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "missing_text_removed": int(missing_text),
        "missing_label_removed": int(missing_label),
        "duplicates_detected": int(duplicate_count),
        "duplicates_removed": bool(drop_duplicates),
        "unrecognized_labels_removed": int(unrecognized_labels),
        "spam_count": spam_count,
        "ham_count": ham_count,
        "spam_ratio": round(spam_count / final_rows, 4) if final_rows > 0 else 0.0,
    }

    return working_df, report
