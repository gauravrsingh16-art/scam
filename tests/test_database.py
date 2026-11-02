"""
Unit Tests for SQLite Classification Database and Privacy Controls
"""

import pytest
from src.database import (
    init_db,
    log_classification,
    get_history,
    get_dashboard_stats,
    clear_history,
    is_history_enabled,
    set_history_enabled,
    is_preview_storage_enabled,
    set_preview_storage_enabled
)


def test_database_lifecycle():
    init_db()

    # Clear prior test state
    clear_history()
    set_history_enabled(True)
    set_preview_storage_enabled(False)

    # Empty stats verification
    stats_empty = get_dashboard_stats()
    assert stats_empty["total_processed"] == 0
    assert stats_empty["has_records"] is False

    # Insert test predictions
    log_classification(
        message_type="SMS",
        prediction="SPAM",
        confidence=0.985,
        char_count=65,
        vectorizer_used="tfidf",
        text="Win free cash now"
    )
    log_classification(
        message_type="Email",
        prediction="NOT SPAM",
        confidence=0.992,
        char_count=45,
        vectorizer_used="tfidf",
        text="Hi are you ready for lunch"
    )

    stats = get_dashboard_stats()
    assert stats["total_processed"] == 2
    assert stats["total_spam"] == 1
    assert stats["total_ham"] == 1
    assert stats["spam_rate"] == 50.0
    assert stats["has_records"] is True

    # Retrieve history
    history = get_history(limit=10)
    assert len(history) == 2
    assert history.iloc[0]["prediction"] in ["SPAM", "NOT SPAM"]
    # Verify preview is empty because preview_storage_enabled was False
    assert history.iloc[0]["text_preview"] == ""

    # Test clearing
    deleted = clear_history()
    assert deleted == 2
    assert get_dashboard_stats()["total_processed"] == 0


def test_privacy_toggles():
    init_db()

    set_history_enabled(False)
    assert is_history_enabled() is False

    # When history is disabled, logging returns False and doesn't record
    logged = log_classification("SMS", "SPAM", 0.99, 50, "tfidf", "test")
    assert logged is False
    assert get_dashboard_stats()["total_processed"] == 0

    # Reset
    set_history_enabled(True)
    assert is_history_enabled() is True
