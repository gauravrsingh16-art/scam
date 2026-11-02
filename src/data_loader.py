"""
Dataset Loading and Validation Module
Supports UCI SMS Spam Collection format, CSV, TSV, and multiple column conventions.
"""

import io
import urllib.request
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, Union
import pandas as pd
from config import RAW_DATASET_CSV, RAW_DATASET_TSV
from src.preprocessing import normalize_label


# Recognized column aliases
LABEL_CANDIDATES = ["v1", "label", "category", "class", "target", "spam", "type", "tag"]
TEXT_CANDIDATES = ["v2", "message", "text", "content", "email", "sms", "body", "email_text", "sms_text"]


def detect_columns(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
    """
    Intelligently infer which columns correspond to the label and message text.
    Returns (label_col, text_col) or (None, None) if undetermined.
    """
    cols_lower = {str(col).strip().lower(): col for col in df.columns}

    detected_label = None
    for cand in LABEL_CANDIDATES:
        if cand in cols_lower:
            detected_label = cols_lower[cand]
            break

    detected_text = None
    for cand in TEXT_CANDIDATES:
        if cand in cols_lower and cols_lower[cand] != detected_label:
            detected_text = cols_lower[cand]
            break

    # If not found by candidate names, inspect column types and distinct values
    if detected_label is None or detected_text is None:
        for col in df.columns:
            if col == detected_label or col == detected_text:
                continue
            unique_count = df[col].nunique(dropna=True)
            # Labels typically have 2 to 5 unique values
            if detected_label is None and 1 < unique_count <= 5:
                detected_label = col
            # Message text usually has high cardinality and average length > 15
            elif detected_text is None:
                sample = df[col].dropna().astype(str)
                if len(sample) > 0 and sample.str.len().mean() > 15:
                    detected_text = col

    return detected_label, detected_text


def read_data_file(
    source: Union[str, Path, io.BytesIO, io.StringIO]
) -> pd.DataFrame:
    """
    Read CSV or TSV file safely with encoding and delimiter fallbacks.
    Handles UTF-8, Latin-1, and CP1252 encodings.
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            if isinstance(source, (str, Path)):
                path_str = str(source)
                sep = "\t" if path_str.endswith(".tsv") else None
                df = pd.read_csv(path_str, sep=sep, encoding=enc, engine="python")
            else:
                # Seek to beginning if bytes/string buffer
                if hasattr(source, "seek"):
                    source.seek(0)
                # Try sniffing delimiter
                df = pd.read_csv(source, sep=None, encoding=enc, engine="python")

            # Check if dataset has unassigned header like the raw UCI TSV
            if len(df.columns) >= 2:
                # If first column contains 'ham' or 'spam' and is named '0', it had no header
                first_col_val = str(df.iloc[0, 0]).strip().lower()
                if first_col_val in ["ham", "spam"] and str(df.columns[0]).isdigit():
                    df.columns = ["v1", "v2"] + [f"extra_{i}" for i in range(len(df.columns) - 2)]
            return df
        except Exception:
            continue

    raise ValueError("Unable to parse file. Please ensure the file is a valid CSV or TSV with UTF-8 or Latin-1 encoding.")


def load_default_dataset() -> pd.DataFrame:
    """Load the bundled or raw SMS Spam Collection dataset."""
    if RAW_DATASET_CSV.exists():
        return read_data_file(RAW_DATASET_CSV)
    elif RAW_DATASET_TSV.exists():
        return read_data_file(RAW_DATASET_TSV)
    else:
        # Download from authoritative mirror
        url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
        urllib.request.urlretrieve(url, RAW_DATASET_TSV)
        df = read_data_file(RAW_DATASET_TSV)
        df.to_csv(RAW_DATASET_CSV, index=False)
        return df


def get_dataset_summary(
    df: pd.DataFrame,
    label_col: str,
    text_col: str
) -> Dict[str, Any]:
    """
    Generate comprehensive dataset health report:
    Total records, spam count, ham count, missing values, duplicates, and class distribution.
    """
    total_rows = len(df)
    missing_text = int(df[text_col].isna().sum()) if text_col in df.columns else 0
    missing_label = int(df[label_col].isna().sum()) if label_col in df.columns else 0

    duplicate_rows = int(df.duplicated(subset=[text_col]).sum()) if text_col in df.columns else 0

    # Count normalized labels
    norm_labels = df[label_col].apply(normalize_label) if label_col in df.columns else pd.Series([])
    spam_count = int((norm_labels == 1).sum())
    ham_count = int((norm_labels == 0).sum())
    unknown_labels = int(norm_labels.isna().sum())

    spam_pct = round((spam_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
    ham_pct = round((ham_count / total_rows) * 100, 2) if total_rows > 0 else 0.0

    return {
        "total_rows": total_rows,
        "label_column": label_col,
        "text_column": text_col,
        "spam_records": spam_count,
        "ham_records": ham_count,
        "unknown_label_records": unknown_labels,
        "missing_text_values": missing_text,
        "missing_label_values": missing_label,
        "duplicate_records": duplicate_rows,
        "spam_percentage": spam_pct,
        "ham_percentage": ham_pct,
        "is_valid": (total_rows > 0 and (spam_count + ham_count) > 0 and text_col in df.columns),
    }
