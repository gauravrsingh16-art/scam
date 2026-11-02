"""
Model Training Service Module
Orchestrates preprocessing, stratified train/test split, feature extraction,
Multinomial Naive Bayes fitting, test evaluation, and model artifact persistence.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, Union
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from config import (
    MODEL_FILE,
    VECTORIZER_FILE,
    METRICS_FILE,
    PROCESSED_DATASET_CSV,
    DEFAULT_ML_CONFIG,
    RAW_DATASET_CSV,
)
from src.data_loader import load_default_dataset, detect_columns
from src.preprocessing import preprocess_dataset
from src.feature_extraction import FeaturePipeline
from src.evaluation import compute_metrics


def get_top_features(
    model: MultinomialNB,
    feature_names: List[str],
    top_n: int = 15
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    Extract vocabulary tokens with highest log-likelihood differential for Spam vs Ham.
    """
    if not hasattr(model, "feature_log_prob_") or len(feature_names) == 0:
        return [], []

    # Difference: spam log prob - ham log prob
    # Positive difference indicates strong spam affinity
    diff = model.feature_log_prob_[1] - model.feature_log_prob_[0]

    top_spam_indices = np.argsort(diff)[-top_n:][::-1]
    top_ham_indices = np.argsort(diff)[:top_n]

    top_spam = [(feature_names[i], round(float(diff[i]), 3)) for i in top_spam_indices]
    top_ham = [(feature_names[i], round(float(-diff[i]), 3)) for i in top_ham_indices]

    return top_spam, top_ham


def train_model(
    df: Optional[pd.DataFrame] = None,
    text_col: Optional[str] = None,
    label_col: Optional[str] = None,
    vectorizer_type: str = "tfidf",
    ngram_range: Tuple[int, int] = (1, 2),
    max_features: int = 5000,
    min_df: int = 2,
    test_size: float = 0.2,
    random_state: int = 42,
    alpha: float = 0.1,
    drop_duplicates: bool = False
) -> Dict[str, Any]:
    """
    Execute end-to-end model training workflow and save validated artifacts.
    """
    # 1. Load dataset
    if df is None:
        df = load_default_dataset()

    # 2. Detect column names if not explicitly provided
    if text_col is None or label_col is None:
        det_label, det_text = detect_columns(df)
        label_col = label_col or det_label
        text_col = text_col or det_text

    if not label_col or not text_col:
        raise ValueError("Could not detect valid label and message text columns.")

    # 3. Clean and normalize dataset
    cleaned_df, prep_report = preprocess_dataset(
        df=df,
        text_col=text_col,
        label_col=label_col,
        drop_duplicates=drop_duplicates
    )

    if len(cleaned_df) < 50:
        raise ValueError(f"Cleaned dataset has only {len(cleaned_df)} rows, insufficient for training.")

    # 4. Save cleaned dataset for auditability
    PROCESSED_DATASET_CSV.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(PROCESSED_DATASET_CSV, index=False)

    X = np.array(cleaned_df["clean_text"].tolist(), dtype=object)
    y = np.array(cleaned_df["label"].tolist(), dtype=int)

    # 5. Stratified Train / Test Split (Strictly avoiding data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    # 6. Fit Feature Pipeline exclusively on training fold
    feature_pipeline = FeaturePipeline(
        vectorizer_type=vectorizer_type,
        ngram_range=ngram_range,
        max_features=max_features,
        min_df=min_df,
        stop_words="english"
    )
    X_train_vec = feature_pipeline.fit_transform(X_train)
    X_test_vec = feature_pipeline.transform(X_test)

    # 7. Fit Multinomial Naive Bayes model
    model = MultinomialNB(alpha=alpha)
    model.fit(X_train_vec, y_train)

    # 8. Evaluate on Held-out Test Set
    y_test_pred = model.predict(X_test_vec)
    y_test_prob = model.predict_proba(X_test_vec)

    # Training set performance check
    y_train_pred = model.predict(X_train_vec)
    train_acc = float((y_train_pred == y_train).mean())

    test_metrics = compute_metrics(
        y_true=y_test,
        y_pred=y_test_pred,
        y_prob=y_test_prob
    )

    # 9. Top Informative Features
    feature_names = feature_pipeline.get_feature_names()
    top_spam, top_ham = get_top_features(model, feature_names, top_n=15)

    # 10. Split Statistics
    train_spam = int((y_train == 1).sum())
    train_ham = int((y_train == 0).sum())
    test_spam = int((y_test == 1).sum())
    test_ham = int((y_test == 0).sum())

    training_metadata = {
        "status": "success",
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_type": "MultinomialNB",
        "vectorizer_type": vectorizer_type,
        "hyperparameters": {
            "alpha": alpha,
            "ngram_range": list(ngram_range),
            "max_features": max_features,
            "min_df": min_df,
            "test_size": test_size,
            "random_state": random_state,
            "vocabulary_size": len(feature_names),
        },
        "dataset_statistics": {
            "initial_rows": prep_report["initial_rows"],
            "cleaned_rows": prep_report["final_rows"],
            "train_samples": len(y_train),
            "test_samples": len(y_test),
            "train_spam": train_spam,
            "train_ham": train_ham,
            "test_spam": test_spam,
            "test_ham": test_ham,
            "duplicates_removed": drop_duplicates,
        },
        "train_accuracy": round(train_acc, 4),
        "test_metrics": test_metrics,
        "top_spam_features": top_spam,
        "top_ham_features": top_ham,
    }

    # 11. Persist Model and Vectorizer Artifacts
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    feature_pipeline.save(VECTORIZER_FILE)

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(training_metadata, f, indent=2)

    return training_metadata


def load_saved_metrics() -> Optional[Dict[str, Any]]:
    """Load existing metrics from disk if available."""
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None
