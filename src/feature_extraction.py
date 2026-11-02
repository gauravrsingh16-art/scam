"""
Feature Extraction Pipeline Module
Supports CountVectorizer and TfidfVectorizer with customizable hyperparameters.
"""

from typing import Tuple, Optional, Any, List
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import joblib


def create_vectorizer(
    vectorizer_type: str = "tfidf",
    ngram_range: Tuple[int, int] = (1, 2),
    max_features: Optional[int] = 5000,
    min_df: int = 2,
    stop_words: Optional[str] = "english"
) -> Any:
    """
    Factory function to instantiate CountVectorizer or TfidfVectorizer.
    """
    v_type = vectorizer_type.strip().lower()

    common_kwargs = {
        "ngram_range": ngram_range,
        "max_features": max_features,
        "min_df": min_df,
        "stop_words": stop_words,
        "sublinear_tf": True if v_type == "tfidf" else False,
    }

    if v_type == "tfidf":
        return TfidfVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            min_df=min_df,
            stop_words=stop_words,
            sublinear_tf=True
        )
    elif v_type == "count":
        return CountVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            min_df=min_df,
            stop_words=stop_words
        )
    else:
        raise ValueError(f"Unsupported vectorizer type '{vectorizer_type}'. Must be 'tfidf' or 'count'.")


class FeaturePipeline:
    """
    Encapsulates the text vectorization pipeline for training and inference consistency.
    """

    def __init__(
        self,
        vectorizer_type: str = "tfidf",
        ngram_range: Tuple[int, int] = (1, 2),
        max_features: Optional[int] = 5000,
        min_df: int = 2,
        stop_words: Optional[str] = "english"
    ):
        self.vectorizer_type = vectorizer_type
        self.ngram_range = ngram_range
        self.max_features = max_features
        self.min_df = min_df
        self.stop_words = stop_words
        self.vectorizer = create_vectorizer(
            vectorizer_type=self.vectorizer_type,
            ngram_range=self.ngram_range,
            max_features=self.max_features,
            min_df=self.min_df,
            stop_words=self.stop_words
        )
        self.is_fitted = False

    def fit(self, texts: Any) -> "FeaturePipeline":
        """Fit vectorizer on training texts only (preventing data leakage)."""
        self.vectorizer.fit(texts)
        self.is_fitted = True
        return self

    def transform(self, texts: Any):
        """Transform texts into sparse feature matrix."""
        if not self.is_fitted:
            raise RuntimeError("Vectorizer has not been fitted yet.")
        return self.vectorizer.transform(texts)

    def fit_transform(self, texts: Any):
        """Fit and transform training texts."""
        matrix = self.vectorizer.fit_transform(texts)
        self.is_fitted = True
        return matrix

    def get_feature_names(self) -> List[str]:
        """Get vocabulary feature names."""
        if not self.is_fitted:
            return []
        return list(self.vectorizer.get_feature_names_out())

    def get_vocab_size(self) -> int:
        """Get total number of vocabulary features extracted."""
        if not self.is_fitted:
            return 0
        return len(self.vectorizer.vocabulary_)

    def get_params(self) -> dict:
        """Return configuration dictionary."""
        return {
            "vectorizer_type": self.vectorizer_type,
            "ngram_range": list(self.ngram_range),
            "max_features": self.max_features,
            "min_df": self.min_df,
            "vocab_size": self.get_vocab_size(),
        }

    def save(self, file_path) -> None:
        """Save fitted vectorizer pipeline to disk using joblib."""
        joblib.dump(self, file_path)

    @classmethod
    def load(cls, file_path) -> "FeaturePipeline":
        """Load fitted vectorizer pipeline from disk."""
        return joblib.load(file_path)
