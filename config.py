"""
System Configuration Module
EMAIL/SMS SPAM DETECTION SYSTEM
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# File Paths
RAW_DATASET_CSV = RAW_DATA_DIR / "sms_spam_collection.csv"
RAW_DATASET_TSV = RAW_DATA_DIR / "sms_spam_collection.tsv"
SAMPLE_BULK_CSV = RAW_DATA_DIR / "sample_bulk_messages.csv"
PROCESSED_DATASET_CSV = PROCESSED_DATA_DIR / "cleaned_dataset.csv"

MODEL_FILE = MODELS_DIR / "spam_model.pkl"
VECTORIZER_FILE = MODELS_DIR / "vectorizer.pkl"
METRICS_FILE = MODELS_DIR / "metrics.json"

# Handle read-only / Vercel serverless environment for SQLite
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    import tempfile
    HISTORY_DB_PATH = Path(tempfile.gettempdir()) / "classification_history.db"
else:
    HISTORY_DB_PATH = DATA_DIR / "classification_history.db"

STYLES_CSS_PATH = ASSETS_DIR / "styles.css"

class SafeColorDict(dict):
    """Centralized theme dictionary that never raises KeyError, providing safe defaults."""
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        # Intelligent, bulletproof fallback defaults
        k = str(key).lower()
        if "text" in k or "white" in k:
            return "#FFFFFF"
        if "muted" in k or "sec" in k and "text" in k:
            return "#B9B1C8"
        if "bg" in k or "card" in k:
            return "#191426"
        if "border" in k:
            return "#3A2B55"
        if "purple" in k:
            return "#8B35F6"
        if "green" in k or "safe" in k:
            return "#16D98B"
        if "red" in k or "spam" in k:
            return "#FF536B"
        return "#8B35F6"

    def get(self, key, default=None):
        if key in self:
            return super().get(key)
        return default if default is not None else self[key]


# Theme Colors (Exact SaaS Design Reference Palette)
COLORS = SafeColorDict({
    "bg": "#0B0912",
    "sidebar": "#100B1D",
    "topbar": "#100D19",
    "card_bg": "#191426",
    "secondary_bg": "#191426",
    "secondary_card": "#211A32",
    "card_border": "#3A2B55",
    "border": "#3A2B55",
    "primary_purple": "#8B35F6",
    "bright_purple": "#A855F7",
    "light_purple": "#C084FC",
    "primary_purple_dark": "#7C3AED",
    "text_primary": "#FFFFFF",
    "text_secondary": "#B9B1C8",
    "text_white": "#FFFFFF",
    "text_muted": "#B9B1C8",
    "safe_green": "#16D98B",
    "safe_green_glow": "rgba(22, 217, 139, 0.25)",
    "spam_red": "#FF536B",
    "spam_red_glow": "rgba(255, 83, 107, 0.25)",
    "warning_orange": "#F59E0B",
    "accent_blue": "#A855F7",
    "card_border_hover": "rgba(168, 85, 247, 0.5)",
})

# Machine Learning Default Hyperparameters
DEFAULT_ML_CONFIG = {
    "vectorizer_type": "tfidf",      # 'tfidf' or 'count'
    "ngram_range": (1, 2),
    "max_features": 5000,
    "min_df": 2,
    "test_size": 0.2,
    "random_state": 42,
    "alpha": 0.1,                     # Laplace smoothing for MultinomialNB
    "stratify": True,
}

# Example Messages for testing and UI demonstration
EXAMPLE_MESSAGES = {
    "spam_lottery": {
        "title": "Lottery Win Scam (SMS)",
        "type": "SMS",
        "subject": "Prize Notification",
        "sender": "claims@cashprize-intl.win",
        "text": "URGENT! You have won a £1,000 cash prize or a guaranteed iPhone 15. Click http://claim-now.xyz/win or call 0800123456 now to claim your reward. Valid 24hrs only!",
    },
    "spam_urgent_phishing": {
        "title": "Bank Account Suspension (Email)",
        "type": "Email",
        "subject": "Urgent: Your Account Access Has Been Suspended",
        "sender": "security-alert@verify-service-auth.com",
        "text": "Dear Customer, Your account access has been temporarily suspended due to suspicious sign-in attempts. You must verify your credentials within 12 hours or your account will be permanently closed. Visit our secure portal immediately: http://update-secure-login.net/banking and enter your security PIN.",
    },
    "ham_meeting": {
        "title": "College Meeting (SMS)",
        "type": "SMS",
        "subject": "Study Group",
        "sender": "alex.campus@university.edu",
        "text": "Hi! Are we meeting at the campus library at 3 PM today to finish the machine learning project report? Let me know if you need me to bring the notes.",
    },
    "ham_appointment": {
        "title": "Medical Appointment (SMS/Email)",
        "type": "Email",
        "subject": "Appointment Confirmation: Dr. Sharma",
        "sender": "reception@cityhealthclinic.org",
        "text": "Hello, this is a friendly reminder that your dental checkup with Dr. Sharma is scheduled for tomorrow at 10:30 AM. Please arrive 10 minutes early. Reply YES to confirm or call 555-0199 to reschedule.",
    },
}

# Ensure directory structures exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, ASSETS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
