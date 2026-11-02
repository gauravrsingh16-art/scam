"""
PAGE 3: EMAIL ANALYSIS
Redesigned to match the enterprise SaaS design system (Image 2).
Features multi-field email evaluation, quick scenarios,
threat intelligence cards, and architectural security disclaimers.
"""

import streamlit as st
import time
from config import COLORS, EXAMPLE_MESSAGES
from src.prediction import SpamClassifierService


def render_email_analysis():
    """Render Page 3: Email Analysis."""
    st.markdown("""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Email Threat <span class="welcome-gradient-text">Analysis</span> ✉</div>
                <div class="welcome-subtitle">Multi-field lexical evaluation of Email Subject, Sender Domain, and Body payload</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "email_subject_input" not in st.session_state:
        st.session_state["email_subject_input"] = ""
    if "email_sender_input" not in st.session_state:
        st.session_state["email_sender_input"] = ""
    if "email_body_input" not in st.session_state:
        st.session_state["email_body_input"] = ""

    # Form Container Card
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.85rem;">
                Email Structure & Header Components
            </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.8rem; color: #A1A1AA; margin-bottom: 0.5rem; font-weight: 600;'>QUICK TEST SCENARIOS:</div>", unsafe_allow_html=True)
    ecol1, ecol2, _ = st.columns([1, 1, 2])

    with ecol1:
        if st.button("🎣 Phishing Account Alert", key="em_ex1", use_container_width=True):
            sample = EXAMPLE_MESSAGES["spam_urgent_phishing"]
            st.session_state["email_subject_input"] = sample["subject"]
            st.session_state["email_sender_input"] = sample["sender"]
            st.session_state["email_body_input"] = sample["text"]
            st.rerun()

    with ecol2:
        if st.button("💼 Legitimate Meeting Notice", key="em_ex2", use_container_width=True):
            sample = EXAMPLE_MESSAGES["ham_appointment"]
            st.session_state["email_subject_input"] = sample["subject"]
            st.session_state["email_sender_input"] = sample["sender"]
            st.session_state["email_body_input"] = sample["text"]
            st.rerun()

    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)

    fcol1, fcol2 = st.columns([2, 1])
    with fcol1:
        email_subject = st.text_input(
            "Email Subject Line",
            value=st.session_state["email_subject_input"],
            placeholder="e.g. Urgent: Account Verification Required"
        )
    with fcol2:
        email_sender = st.text_input(
            "Sender Address / Display (Optional)",
            value=st.session_state["email_sender_input"],
            placeholder="e.g. security-alert@verify-portal.com"
        )

    email_body = st.text_area(
        "Email Body Content",
        value=st.session_state["email_body_input"],
        height=160,
        placeholder="Paste full email body text here..."
    )

    btn_analyze_col, btn_clear_col, _ = st.columns([1.5, 1, 3])
    analyze_clicked = False
    with btn_analyze_col:
        analyze_clicked = st.button("🔍 Analyze Email", key="btn_analyze_email", type="primary", use_container_width=True)

    with btn_clear_col:
        if st.button("🔄 Reset Fields", key="btn_reset_email", use_container_width=True):
            st.session_state["email_subject_input"] = ""
            st.session_state["email_sender_input"] = ""
            st.session_state["email_body_input"] = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        if not email_body.strip() and not email_subject.strip():
            st.error("⚠️ Please provide at least an Email Subject or Email Body for analysis.")
            return

        parts = []
        if email_subject.strip():
            parts.append(f"Subject: {email_subject.strip()}")
        if email_sender.strip():
            parts.append(f"Sender: {email_sender.strip()}")
        if email_body.strip():
            parts.append(email_body.strip())

        combined_text = " . ".join(parts)

        with st.spinner("Executing lexical analysis and vectorizing payload..."):
            time.sleep(0.12)
            service = SpamClassifierService.get_instance()
            try:
                result = service.predict_single(combined_text, message_type="Email", log_to_db=True)
            except Exception as e:
                st.error(f"❌ Analysis Failed: {str(e)}")
                return

        is_spam = result["is_spam"]
        conf_pct = round(result["confidence"] * 100, 2)
        heuristics = result["heuristics"]

        if is_spam:
            st.markdown(f"""
                <div class="saas-card" style="border: 1px solid {COLORS['spam_red']}; background: linear-gradient(145deg, rgba(240, 82, 104, 0.08) 0%, #1B1921 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 1.8rem;">🚨</span>
                            <div>
                                <div style="font-size: 1.3rem; font-weight: 800; color: {COLORS['spam_red']};">
                                    SUSPICIOUS / PHISHING EMAIL DETECTED
                                </div>
                                <div style="font-size: 0.82rem; color: #A1A1AA;">
                                    High risk of fraudulent credential harvesting or deceptive solicitation
                                </div>
                            </div>
                        </div>
                        <span class="pill-status-spam" style="font-size: 0.85rem; padding: 4px 12px;">Confidence: {conf_pct}%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="saas-card" style="border: 1px solid {COLORS['safe_green']}; background: linear-gradient(145deg, rgba(34, 197, 94, 0.08) 0%, #1B1921 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 1.8rem;">🛡️</span>
                            <div>
                                <div style="font-size: 1.3rem; font-weight: 800; color: {COLORS['safe_green']};">
                                    BENIGN / LEGITIMATE EMAIL
                                </div>
                                <div style="font-size: 0.82rem; color: #A1A1AA;">
                                    Linguistic style aligns with legitimate transactional or interpersonal email
                                </div>
                            </div>
                        </div>
                        <span class="pill-status-ham" style="font-size: 0.85rem; padding: 4px 12px;">Confidence: {conf_pct}%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        hcol1, hcol2 = st.columns(2)

        with hcol1:
            st.markdown("""
                <div class="saas-card">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #A78BFA;">📡</span>
                            <span class="saas-card-title">Email Threat Telemetry</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)

            if heuristics["has_indicators"]:
                for cat, items in heuristics["detected_triggers"].items():
                    st.markdown(f"""
                        <div style="margin-bottom: 0.5rem; font-size: 0.84rem;">
                            <b style="color: #F8FAFC;">{cat}:</b> {', '.join([f'<code>{i}</code>' for i in items[:4]])}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #71717A; font-size: 0.84rem;'>No explicit phishing triggers detected in textual payload.</div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--border-subtle); font-size: 0.8rem; color: #A1A1AA;">
                    Heuristic Score: <b>{heuristics['threat_score']}/100</b> &nbsp;|&nbsp; 
                    Detected URLs: <b>{heuristics['url_count']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with hcol2:
            st.markdown("""
                <div class="saas-card">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #8B5CF6;">🛡️</span>
                            <span class="saas-card-title">Protective Protocol</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)

            for rec in heuristics["recommendations"]:
                st.markdown(f"""
                    <div style="font-size: 0.83rem; color: #E2E8F0; margin-bottom: 0.45rem; display: flex; gap: 0.5rem;">
                        <span style="color: #8B5CF6;">▸</span>
                        <span>{rec}</span>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="background-color: #211E29; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 0.85rem 1.15rem; font-size: 0.82rem; color: #A1A1AA; display: flex; gap: 0.65rem;">
                <span style="color: #A78BFA; font-size: 1rem;">ℹ️</span>
                <div>
                    <b>Architecture Disclosure:</b> Textual classification is computed by the trained 
                    Multinomial Naive Bayes model. The application evaluates textual features and does NOT 
                    perform live SMTP header tracing, DKIM/SPF cryptographic key validation, or active link sandbox analysis.
                </div>
            </div>
        """, unsafe_allow_html=True)
