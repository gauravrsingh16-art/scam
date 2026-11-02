"""
Prediction Service Module
Loads persistent machine learning artifacts, validates text input, performs real-time inference,
computes class probabilities, and coordinates with SQLite classification logging.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import joblib

from config import MODEL_FILE, VECTORIZER_FILE, METRICS_FILE
from src.preprocessing import clean_text
from src.feature_extraction import FeaturePipeline
from src.database import log_classification
from src.explainability import analyze_heuristics


class SpamClassifierService:
    """
    Production-grade prediction service ensuring inference consistency with training pipeline.
    """

    _instance: Optional["SpamClassifierService"] = None

    def __init__(self):
        self.model = None
        self.vectorizer_pipeline = None
        self.metadata = None
        self.load_artifacts()

    @classmethod
    def get_instance(cls, force_reload: bool = False) -> "SpamClassifierService":
        """Get or initialize singleton instance."""
        if cls._instance is None or force_reload:
            cls._instance = cls()
        return cls._instance

    def is_model_ready(self) -> bool:
        """Check if both model and vectorizer are successfully loaded."""
        return self.model is not None and self.vectorizer_pipeline is not None

    def load_artifacts(self) -> bool:
        """Load serialized model and vectorizer pipeline from disk."""
        if MODEL_FILE.exists() and VECTORIZER_FILE.exists():
            try:
                self.model = joblib.load(MODEL_FILE)
                self.vectorizer_pipeline = FeaturePipeline.load(VECTORIZER_FILE)
                return True
            except Exception as e:
                self.model = None
                self.vectorizer_pipeline = None
                return False
        return False

    def predict_single(
        self,
        text: str,
        message_type: str = "SMS",
        log_to_db: bool = True
    ) -> Dict[str, Any]:
        """
        Classify a single email or SMS message text.
        Returns detailed prediction results with confidence and heuristics.
        """
        if not self.is_model_ready():
            # Try reloading once
            if not self.load_artifacts():
                raise RuntimeError(
                    "Spam detection model is not loaded. Please train the model from the Dataset Management page or run 'python train.py'."
                )

        if not text or not str(text).strip():
            raise ValueError("Input message text cannot be empty.")

        raw_text = str(text)
        char_count = len(raw_text)
        word_count = len(raw_text.split())

        # Clean text using the identical preprocessor used during training
        cleaned = clean_text(raw_text)
        if not cleaned:
            cleaned = "empty_message"

        # Vectorize text
        vectorized = self.vectorizer_pipeline.transform([cleaned])

        # Generate ML model predictions
        raw_pred = self.model.predict(vectorized)[0]
        probabilities = self.model.predict_proba(vectorized)[0]

        ham_prob = float(probabilities[0])
        spam_prob = float(probabilities[1])

        is_spam = bool(raw_pred == 1)
        label = "SPAM" if is_spam else "NOT SPAM"
        confidence = spam_prob if is_spam else ham_prob

        # Run explainability & security analysis
        heuristics = analyze_heuristics(raw_text)

        # Log to SQLite classification history
        if log_to_db:
            vectorizer_name = getattr(self.vectorizer_pipeline, "vectorizer_type", "tfidf")
            log_classification(
                message_type=message_type,
                prediction=label,
                confidence=confidence,
                char_count=char_count,
                vectorizer_used=vectorizer_name,
                text=raw_text
            )

        return {
            "is_spam": is_spam,
            "label": label,
            "confidence": round(confidence, 4),
            "spam_probability": round(spam_prob, 4),
            "ham_probability": round(ham_prob, 4),
            "cleaned_text": cleaned,
            "char_count": char_count,
            "word_count": word_count,
            "heuristics": heuristics,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vectorizer_type": getattr(self.vectorizer_pipeline, "vectorizer_type", "tfidf")
        }

    def predict_bulk(
        self,
        df: pd.DataFrame,
        text_col: str,
        log_to_db: bool = False
    ) -> pd.DataFrame:
        """
        Classify multiple messages in batch with vectorized high performance.
        Returns DataFrame with 'Prediction', 'Confidence', and 'Spam_Probability'.
        """
        if not self.is_model_ready():
            if not self.load_artifacts():
                raise RuntimeError("Spam model is not trained or loaded.")

        if text_col not in df.columns:
            raise ValueError(f"Column '{text_col}' not found in DataFrame.")

        # Copy dataframe
        result_df = df.copy()

        # Clean texts
        cleaned_series = result_df[text_col].fillna("").astype(str).apply(clean_text)
        # Handle cases where cleaned is empty
        cleaned_series = cleaned_series.apply(lambda s: s if s else "empty_message")

        # Vectorize all texts simultaneously
        vectors = self.vectorizer_pipeline.transform(cleaned_series.values)

        # Predict batch
        preds = self.model.predict(vectors)
        probs = self.model.predict_proba(vectors)

        labels = ["SPAM" if p == 1 else "NOT SPAM" for p in preds]
        confidences = [round(float(max(pr[0], pr[1])), 4) for pr in probs]
        spam_probabilities = [round(float(pr[1]), 4) for pr in probs]

        result_df["Prediction"] = labels
        result_df["Confidence"] = confidences
        result_df["Spam_Probability"] = spam_probabilities

        if log_to_db:
            vectorizer_name = getattr(self.vectorizer_pipeline, "vectorizer_type", "tfidf")
            for i, row in result_df.iterrows():
                raw_text = str(row[text_col])
                log_classification(
                    message_type="Bulk",
                    prediction=row["Prediction"],
                    confidence=row["Confidence"],
                    char_count=len(raw_text),
                    vectorizer_used=vectorizer_name,
                    text=raw_text
                )

        return result_df
