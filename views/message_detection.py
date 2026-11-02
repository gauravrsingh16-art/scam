"""
PAGE 2: MESSAGE DETECTION
Redesigned to match the enterprise SaaS design system (Image 2).
Features channel selection, benchmark pills, sleek input card,
and high-contrast cybersecurity prediction cards with heuristic threat diagnostics.
"""

import streamlit as st
import time
from config import COLORS, EXAMPLE_MESSAGES
from src.prediction import SpamClassifierService


def render_message_detection():
    """Render Page 2: Single Message Spam Detection."""
    st.markdown("""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Message <span class="welcome-gradient-text">Detection Engine</span> ⚡</div>
                <div class="welcome-subtitle">Real-time NLP classification and threat intelligence for SMS and Email text streams</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "input_message_text" not in st.session_state:
        st.session_state["input_message_text"] = ""
    if "selected_msg_channel" not in st.session_state:
        st.session_state["selected_msg_channel"] = "SMS"

    # Main Input Card
    st.markdown("""
        <div class="saas-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem;">
                <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC;">
                    Message Input & Payload
                </div>
                <div style="font-size: 0.78rem; color: #A1A1AA;">
                    Format: Plain Text / Unicode
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Benchmark Buttons Row
    st.markdown("<div style='font-size: 0.8rem; color: #A1A1AA; margin-bottom: 0.5rem; font-weight: 600;'>BENCHMARK EXAMPLES:</div>", unsafe_allow_html=True)
    bcol1, bcol2, bcol3, bcol4 = st.columns(4)

    with bcol1:
        if st.button("🚨 Lottery Scam (Spam)", key="btn_ex1", use_container_width=True):
            st.session_state["input_message_text"] = EXAMPLE_MESSAGES["spam_lottery"]["text"]
            st.session_state["selected_msg_channel"] = "SMS"
            st.rerun()

    with bcol2:
        if st.button("🎣 Bank Phishing (Spam)", key="btn_ex2", use_container_width=True):
            st.session_state["input_message_text"] = EXAMPLE_MESSAGES["spam_urgent_phishing"]["text"]
            st.session_state["selected_msg_channel"] = "Email"
            st.rerun()

    with bcol3:
        if st.button("📚 Campus Meeting (Ham)", key="btn_ex3", use_container_width=True):
            st.session_state["input_message_text"] = EXAMPLE_MESSAGES["ham_meeting"]["text"]
            st.session_state["selected_msg_channel"] = "SMS"
            st.rerun()

    with bcol4:
        if st.button("🏥 Clinic Booking (Ham)", key="btn_ex4", use_container_width=True):
            st.session_state["input_message_text"] = EXAMPLE_MESSAGES["ham_appointment"]["text"]
            st.session_state["selected_msg_channel"] = "Email"
            st.rerun()

    # Input Text Area
    user_text = st.text_area(
        label="Message Text to Analyze",
        value=st.session_state["input_message_text"],
        height=150,
        placeholder="Paste SMS or email text here (e.g. 'URGENT! You have won £1,000 cash prize. Call now...')...",
        label_visibility="collapsed"
    )

    char_count = len(user_text)
    word_count = len(user_text.split())

    col_meta1, col_meta2 = st.columns([2, 1])
    with col_meta1:
        st.markdown(f"""
            <div style="font-size: 0.8rem; color: #71717A; margin-top: 0.25rem;">
                Characters: <b style="color: #F8FAFC;">{char_count}</b> &nbsp;|&nbsp; 
                Words: <b style="color: #F8FAFC;">{word_count}</b>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.85rem;'></div>", unsafe_allow_html=True)

    btn_run_col, btn_clear_col, _ = st.columns([1.5, 1, 3])

    classify_clicked = False
    with btn_run_col:
        classify_clicked = st.button("⚡ Classify Message", key="btn_classify", type="primary", use_container_width=True)

    with btn_clear_col:
        if st.button("🔄 Clear Input", key="btn_clear_msg", use_container_width=True):
            st.session_state["input_message_text"] = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Classification Execution
    if classify_clicked:
        if not user_text.strip():
            st.error("⚠️ Input message cannot be empty. Please enter or paste text to classify.")
            return

        with st.spinner("Processing token vectors and evaluating MultinomialNB distribution..."):
            time.sleep(0.12)
            service = SpamClassifierService.get_instance()
            try:
                result = service.predict_single(user_text, message_type=st.session_state["selected_msg_channel"], log_to_db=True)
            except Exception as e:
                st.error(f"❌ Classification Error: {str(e)}")
                return

        is_spam = result["is_spam"]
        conf_pct = round(result["confidence"] * 100, 2)
        spam_pct = round(result["spam_probability"] * 100, 2)
        ham_pct = round(result["ham_probability"] * 100, 2)
        heuristics = result["heuristics"]

        # Result Display Card
        if is_spam:
            st.markdown(f"""
                <div class="saas-card" style="border: 1px solid {COLORS['spam_red']}; background: linear-gradient(145deg, rgba(240, 82, 104, 0.08) 0%, #1B1921 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 1.8rem;">🚨</span>
                            <div>
                                <div style="font-size: 1.3rem; font-weight: 800; color: {COLORS['spam_red']}; letter-spacing: -0.02em;">
                                    CLASSIFIED AS SPAM / THREAT
                                </div>
                                <div style="font-size: 0.82rem; color: #A1A1AA;">
                                    High-confidence deceptive or unsolicited solicitation detected
                                </div>
                            </div>
                        </div>
                        <div>
                            <span class="pill-status-spam" style="font-size: 0.85rem; padding: 4px 12px;">Confidence: {conf_pct}%</span>
                        </div>
                    </div>
                    <div style="background-color: #211E29; border-radius: 8px; padding: 0.85rem 1rem; border: 1px solid rgba(240, 82, 104, 0.2);">
                        <div style="font-size: 0.85rem; color: #F8FAFC; line-height: 1.5;">
                            <b>Model Inference Explanation:</b> The lexical feature distribution matches trained spam vectors 
                            with <b>{spam_pct}%</b> probability (vs <b>{ham_pct}%</b> legitimate correspondence).
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="saas-card" style="border: 1px solid {COLORS['safe_green']}; background: linear-gradient(145deg, rgba(34, 197, 94, 0.08) 0%, #1B1921 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <span style="font-size: 1.8rem;">🛡️</span>
                            <div>
                                <div style="font-size: 1.3rem; font-weight: 800; color: {COLORS['safe_green']}; letter-spacing: -0.02em;">
                                    CLASSIFIED AS NOT SPAM (LEGITIMATE / HAM)
                                </div>
                                <div style="font-size: 0.82rem; color: #A1A1AA;">
                                    Linguistic structure matches benign interpersonal communication
                                </div>
                            </div>
                        </div>
                        <div>
                            <span class="pill-status-ham" style="font-size: 0.85rem; padding: 4px 12px;">Confidence: {conf_pct}%</span>
                        </div>
                    </div>
                    <div style="background-color: #211E29; border-radius: 8px; padding: 0.85rem 1rem; border: 1px solid rgba(34, 197, 94, 0.2);">
                        <div style="font-size: 0.85rem; color: #F8FAFC; line-height: 1.5;">
                            <b>Security Advisory & Limitation:</b> The model evaluated this message as benign with <b>{conf_pct}%</b> confidence. 
                            <i>Machine learning predictions are statistical assessments, not a warranty of security. Always verify sender identity when sensitive credentials or financial actions are requested.</i>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Heuristic Analysis Cards
        h_col1, h_col2 = st.columns(2)

        with h_col1:
            st.markdown("""
                <div class="saas-card">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #A78BFA;">🔍</span>
                            <span class="saas-card-title">Heuristic Threat Signals</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)

            if heuristics["has_indicators"]:
                for category, cues in heuristics["detected_triggers"].items():
                    cues_str = ", ".join([f"<code>{c}</code>" for c in cues[:4]])
                    st.markdown(f"""
                        <div style="margin-bottom: 0.5rem; font-size: 0.84rem;">
                            <b style="color: #F8FAFC;">{category}:</b> {cues_str}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="color: #71717A; font-size: 0.84rem; padding: 0.4rem 0;">
                        No aggressive phishing lures, financial baits, or low-reputation URLs detected.
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style="margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--border-subtle); font-size: 0.8rem; color: #A1A1AA;">
                    Heuristic Risk Index: <b style="color: {'#F05268' if heuristics['threat_score'] >= 50 else '#22C55E'};">{heuristics['threat_score']}/100</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with h_col2:
            st.markdown("""
                <div class="saas-card">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #8B5CF6;">🛡️</span>
                            <span class="saas-card-title">Protective Guidelines</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)

            for rec in heuristics["recommendations"][:3]:
                st.markdown(f"""
                    <div style="margin-bottom: 0.45rem; font-size: 0.83rem; color: #E2E8F0; display: flex; gap: 0.5rem;">
                        <span style="color: #8B5CF6;">▸</span>
                        <span>{rec}</span>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
