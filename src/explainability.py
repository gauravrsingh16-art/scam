"""
Message Explainability and Security Analysis Module
Detects heuristic indicators (phishing patterns, urgency, suspicious URLs, lottery lures)
and generates cybersecurity risk assessments and actionable user recommendations.
"""

import re
from typing import Dict, Any, List


URGENCY_PATTERNS = [
    r"\burgent\b", r"\bimmediately\b", r"\bact now\b", r"\blimited time\b",
    r"\bexpire[sd]?\b", r"\bsuspend(ed)?\b", r"\bwithin \d+ hours?\b",
    r"\bfinal notice\b", r"\baction required\b", r"\blast chance\b",
    r"\b24\s*hrs?\b", r"\btoday only\b", r"\binstant(ly)?\b"
]

FINANCIAL_PRIZE_PATTERNS = [
    r"\bprize\b", r"\bcash\b", r"\blottery\b", r"\bwinner\b", r"\bcongratulations\b",
    r"\breward\b", r"\bfree\b", r"\bwon\b", r"\b£\d+\b", r"\$\d+\b", r"\b€\d+\b",
    r"\bclaim\b", r"\bbonus\b", r"\bguaranteed\b", r"\bgift card\b", r"\bvoucher\b",
    r"\bmillion\b", r"\bpayout\b", r"\b0%\s*interest\b", r"\bloan\b"
]

CREDENTIAL_HARVESTING_PATTERNS = [
    r"\bverify your (account|identity|details|credentials)\b",
    r"\bsecurity (pin|code|alert)\b", r"\bpassword\b", r"\blogin\b",
    r"\bunauthorized (access|activity|sign-in)\b", r"\bconfirm your identity\b",
    r"\bupdate (billing|payment|security)\b", r"\baccount locked\b",
    r"\bbank account\b", r"\bpaypal\b"
]

SUSPICIOUS_URL_PATTERNS = [
    r"https?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}",          # IP address URL
    r"bit\.ly/\S+", r"tinyurl\.com/\S+", r"t\.co/\S+",  # Link shorteners
    r"\.xyz/\S*", r"\.top/\S*", r"\.biz/\S*",           # Low-reputation TLDs
    r"\.win/\S*", r"\.info/\S*", r"\.click/\S*",
    r"https?://\S+"                                      # Generic URLs
]

PHONE_SHORTCODE_PATTERNS = [
    r"\b090[5-9]\d{6,7}\b",                              # UK premium rate SMS
    r"\b087[0-2]\d{7}\b",
    r"\b0800\d{6}\b",
    r"\b\d{5}\b",                                        # 5-digit shortcodes
    r"\bcall \d+\b",
    r"\btext \w+ to \d+\b"
]


def analyze_heuristics(text: str) -> Dict[str, Any]:
    """
    Perform deep pattern analysis on text to highlight potential threat indicators.
    These heuristic indicators are displayed transparently to complement machine learning predictions.
    """
    if not text or not isinstance(text, str):
        return {
            "has_indicators": False,
            "threat_score": 0,
            "detected_triggers": {},
            "url_count": 0,
            "uppercase_ratio": 0.0,
            "recommendations": []
        }

    detected = {}

    # 1. Urgency Patterns
    urgency_matches = []
    for pat in URGENCY_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            urgency_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
    if urgency_matches:
        detected["Urgent & Coercive Phrasing"] = list(set([m.lower() for m in urgency_matches]))

    # 2. Financial / Prize Lures
    financial_matches = []
    for pat in FINANCIAL_PRIZE_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            financial_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
    if financial_matches:
        detected["Financial & Prize Lures"] = list(set([m.lower() for m in financial_matches]))

    # 3. Credential Harvesting Cues
    credential_matches = []
    for pat in CREDENTIAL_HARVESTING_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            credential_matches.extend([m[0] if isinstance(m, tuple) else m for m in matches])
    if credential_matches:
        detected["Credential / Verification Cues"] = list(set([m.lower() for m in credential_matches]))

    # 4. URLs
    urls = []
    for pat in SUSPICIOUS_URL_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            urls.extend(matches)
    urls = list(set(urls))
    if urls:
        detected["Detected Links / Domains"] = urls

    # 5. Phone / Shortcodes
    phones = []
    for pat in PHONE_SHORTCODE_PATTERNS:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        if matches:
            phones.extend([m[0] if isinstance(m, tuple) else m for m in matches])
    phones = list(set(phones))
    if phones:
        detected["Contact Numbers / Shortcodes"] = phones

    # 6. Formatting Anomalies
    total_letters = sum(c.isalpha() for c in text)
    uppercase_letters = sum(c.isupper() for c in text)
    uppercase_ratio = round(uppercase_letters / total_letters, 3) if total_letters > 0 else 0.0
    exclamation_count = text.count("!")

    if uppercase_ratio > 0.35 and total_letters > 15:
        detected["Abnormal Capitalization"] = [f"{int(uppercase_ratio * 100)}% capital letters (aggressive shouting)"]
    if exclamation_count >= 3:
        detected["High Punctuation Density"] = [f"{exclamation_count} exclamation marks detected"]

    # Compute Threat Score (0 - 100)
    score = 0
    if "Credential / Verification Cues" in detected:
        score += 35
    if "Financial & Prize Lures" in detected:
        score += 25
    if "Urgent & Coercive Phrasing" in detected:
        score += 20
    if "Detected Links / Domains" in detected:
        score += 20
    if "Contact Numbers / Shortcodes" in detected:
        score += 15
    if "Abnormal Capitalization" in detected:
        score += 10
    threat_score = min(score, 100)

    # Recommendations
    recs = generate_security_recommendations(threat_score, detected)

    return {
        "has_indicators": len(detected) > 0,
        "threat_score": threat_score,
        "detected_triggers": detected,
        "url_count": len(urls),
        "uppercase_ratio": uppercase_ratio,
        "recommendations": recs,
    }


def generate_security_recommendations(threat_score: int, detected: Dict[str, List[str]]) -> List[str]:
    """Provide contextual cybersecurity safety guidelines."""
    recs = []

    if threat_score >= 50 or "Credential / Verification Cues" in detected:
        recs.append("NEVER click links to sign in or update passwords from an unexpected message.")
        recs.append("Navigate independently to the official service website or banking application.")
        recs.append("Legitimate institutions will never ask for PINs, passwords, or OTPs via SMS or unauthenticated email.")

    if "Financial & Prize Lures" in detected:
        recs.append("Unsolicited prize notifications for lotteries or contests you never entered are 100% fraudulent.")
        recs.append("Do not wire money or pay 'processing fees' to claim any alleged reward.")

    if "Contact Numbers / Shortcodes" in detected:
        recs.append("Do not call unknown premium phone numbers back; they may incur exorbitant carrier charges.")

    if not recs:
        recs.append("Always inspect sender authenticity before opening attachments or downloading files.")
        recs.append("Classification by AI is probabilistic; maintain vigilance for novel spear-phishing tactics.")

    return recs
