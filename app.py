"""
Master Application Controller
SPAM INTELLIGENCE — Production Cybersecurity SaaS Platform
Exact Visual Design Reference Implementation
"""

import streamlit as st
from pathlib import Path
import sys

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import STYLES_CSS_PATH, MODEL_FILE, VECTORIZER_FILE
from src.database import init_db
from src.model_training import train_model, load_saved_metrics
from src.prediction import SpamClassifierService

# Import Page Views
from views.dashboard import render_dashboard
from views.message_detection import render_message_detection
from views.email_analysis import render_email_analysis
from views.bulk_detection import render_bulk_detection
from views.model_performance import render_model_performance
from views.dataset_management import render_dataset_management
from views.history import render_history
from views.project_information import render_project_information
from views.settings import render_settings


# 1. Page Configuration
st.set_page_config(
    page_title="Spam Intelligence — AI-Powered Email/SMS Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. Inject SaaS CSS Design System
def inject_custom_css():
    """Inject custom SaaS CSS stylesheet."""
    if STYLES_CSS_PATH.exists():
        with open(STYLES_CSS_PATH, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# 3. System Initialization
def bootstrap_system():
    """Ensure database and machine learning artifacts are loaded."""
    init_db()
    if not MODEL_FILE.exists() or not VECTORIZER_FILE.exists():
        with st.spinner("Bootstrapping ML pipeline artifacts..."):
            train_model()
    SpamClassifierService.get_instance()


# 4. Top Navigation Bar (Shared across all pages)
# 4. Top Navigation Bar (Shared across all pages)
def render_top_navbar():
    """Render top horizontal navigation bar matching reference screenshot."""
    st.markdown("""
        <div class="top-header-bar">
            <div class="search-box-container">
                <span class="search-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8E859E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                </span>
                <span class="search-input-fake">Search anything...</span>
                <span class="search-kbd-badge">Ctrl + K</span>
            </div>
            <div class="header-right-actions">
                <div class="header-icon-btn" title="Notifications">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B9B1C8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    <span class="header-icon-badge"></span>
                </div>
                <div class="header-icon-btn" title="Settings">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#B9B1C8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
                </div>
                <div class="user-profile-badge">
                    <div class="user-avatar-circle">GS</div>
                    <div class="user-info-text">
                        <span class="user-name">Gaurav Singh</span>
                        <span class="user-role">IT Engineering</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def main():
    inject_custom_css()
    bootstrap_system()

    metrics = load_saved_metrics()

    # Initialize active navigation state
    if "active_nav" not in st.session_state:
        st.session_state["active_nav"] = "dashboard"

    # =========================================================================
    # SIDEBAR COMPONENT (Matching Reference)
    # =========================================================================
    with st.sidebar:
        # Brand Header with Exact Violet Shield Icon & Dual-line Title
        st.markdown("""
            <div class="sidebar-brand-box">
                <div class="brand-icon-shield">
                    <svg width="36" height="36" viewBox="0 0 40 40" fill="none">
                        <path d="M20 3L6 8V18C6 27.5 12 36 20 39C28 36 34 27.5 34 18V8L20 3Z" fill="url(#brand_shield_grad)" stroke="#A855F7" stroke-width="1.5"/>
                        <path d="M20 13V25M14 19H26" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
                        <defs>
                            <linearGradient id="brand_shield_grad" x1="6" y1="3" x2="34" y2="39" gradientUnits="userSpaceOnUse">
                                <stop stop-color="#8B5CF6"/>
                                <stop offset="1" stop-color="#4C1D95"/>
                            </linearGradient>
                        </defs>
                    </svg>
                </div>
                <div class="brand-text-container">
                    <div class="brand-title">SPAM<br>INTELLIGENCE</div>
                    <div class="brand-subtitle">Cybersecurity ML Defense Engine</div>
                    <div class="brand-badge">v1.0.0 Production</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Navigation Menu Items matching Reference Screenshot (9 items)
        nav_items = [
            ("dashboard", "⊞  Dashboard"),
            ("message_detection", "⚡  Message Detection"),
            ("email_analysis", "✉  Email Analysis"),
            ("bulk_detection", "▤  Bulk Detection"),
            ("model_performance", "📊  Model Performance"),
            ("dataset_management", "🗄  Dataset Management"),
            ("history", "🕒  Classification History"),
            ("project_information", "ⓘ  Project Information"),
            ("settings", "⚙  Settings"),
        ]

        for nav_key, nav_label in nav_items:
            is_active = (st.session_state["active_nav"] == nav_key)
            if st.button(
                nav_label,
                key=f"nav_btn_{nav_key}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                if not is_active:
                    st.session_state["active_nav"] = nav_key
                    st.rerun()

        # System Status Card (Matching Reference Screenshot)
        total_rows = metrics.get("dataset_statistics", {}).get("initial_rows", 5572) if metrics else 5572
        st.markdown(f"""
            <div class="sidebar-status-card">
                <div class="status-header-title">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#C084FC" stroke-width="2.2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                    <span>System Status</span>
                </div>
                <div class="status-row">
                    <div class="status-row-left">
                        <span class="status-dot-active"></span>
                        <span>ML Model</span>
                    </div>
                    <span class="status-row-val">MultinomialNB</span>
                </div>
                <div class="status-row">
                    <div class="status-row-left">
                        <span class="status-dot-active"></span>
                        <span>Vectorizer</span>
                    </div>
                    <span class="status-row-val">TF-IDF</span>
                </div>
                <div class="status-row">
                    <div class="status-row-left">
                        <span class="status-dot-active"></span>
                        <span>Database</span>
                    </div>
                    <span class="status-row-val">SQLite (Active)</span>
                </div>
                <div class="status-row">
                    <div class="status-row-left">
                        <span class="status-dot-active"></span>
                        <span>Dataset</span>
                    </div>
                    <span class="status-row-val">{total_rows:,} Records</span>
                </div>
                <div class="status-operational-pill">
                    <span>✓</span>
                    <span>All Systems Operational</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # =========================================================================
    # MAIN WORKSPACE
    # =========================================================================
    # Render Persistent SaaS Top Bar
    render_top_navbar()

    # Route Page Views
    current_page = st.session_state["active_nav"]

    if current_page == "dashboard":
        render_dashboard()
    elif current_page == "message_detection":
        render_message_detection()
    elif current_page == "email_analysis":
        render_email_analysis()
    elif current_page == "bulk_detection":
        render_bulk_detection()
    elif current_page == "model_performance":
        render_model_performance()
    elif current_page == "dataset_management":
        render_dataset_management()
    elif current_page == "history":
        render_history()
    elif current_page == "project_information":
        render_project_information()
    elif current_page == "settings":
        render_settings()


if __name__ == "__main__":
    main()
