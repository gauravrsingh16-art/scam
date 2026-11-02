"""
PAGE 9: SYSTEM SETTINGS & PREFERENCES
Centralized configuration, privacy controls, ML pipeline specifications,
theme palettes, SQLite database optimization, and system diagnostics.
"""

import streamlit as st
import sys
import platform
import sklearn
import pandas
import numpy
import sqlite3

from config import COLORS, HISTORY_DB_PATH, MODEL_FILE, VECTORIZER_FILE, RAW_DATASET_CSV
from src.database import (
    is_history_enabled,
    set_history_enabled,
    is_preview_storage_enabled,
    set_preview_storage_enabled,
    get_db_file_size,
    reindex_database,
    clear_history,
    get_dashboard_stats
)
from src.model_training import load_saved_metrics
from src.prediction import SpamClassifierService


def render_settings():
    """Render Page 9: System Settings and Preferences."""
    st.markdown(f"""
        <div class="welcome-section" style="margin-bottom: 1rem;">
            <div>
                <div class="welcome-title">System <span class="welcome-gradient-text">Settings</span></div>
                <div class="welcome-subtitle">Configure privacy preferences, machine learning parameters, and database operations</div>
            </div>
            <div class="model-active-pill">
                <div class="model-active-header">
                    <span class="status-dot-active"></span> v1.0.0 Production
                </div>
                <div class="model-active-sub">
                    Security Defense Engine
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    metrics = load_saved_metrics()
    stats = get_dashboard_stats()
    classifier = SpamClassifierService.get_instance()

    # Section 1: Privacy & History Preferences
    st.markdown("""
        <div class="saas-card" style="margin-bottom: 1.25rem;">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="font-size: 1.1rem;">🔒</span>
                    <span class="saas-card-title">Privacy & Classification Storage Preferences</span>
                </div>
                <span class="saas-card-action">Data Governance</span>
            </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        hist_active = is_history_enabled()
        new_hist = st.toggle("Enable Classification Logging", value=hist_active, help="Persist prediction metadata in local SQLite database for analytics.")
        if new_hist != hist_active:
            set_history_enabled(new_hist)
            st.toast("History logging setting updated!", icon="✅")
            st.rerun()

        st.caption("When enabled, message timestamp, prediction type, and confidence are recorded. Turning this off provides 100% ephemeral processing.")

    with c2:
        prev_active = is_preview_storage_enabled()
        new_prev = st.toggle("Store Message Previews (Sanitized)", value=prev_active, help="Save the first 60 characters of analyzed messages for audit review.")
        if new_prev != prev_active:
            set_preview_storage_enabled(new_prev)
            st.toast("Message preview storage updated!", icon="✅")
            st.rerun()

        st.caption("When disabled, message text is strictly sanitized and discarded immediately after classification.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section 2: Machine Learning Model & Vectorizer Information
    st.markdown("""
        <div class="saas-card" style="margin-bottom: 1.25rem;">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="font-size: 1.1rem;">🧠</span>
                    <span class="saas-card-title">Machine Learning Model Specifications</span>
                </div>
                <span class="pill-status-ham" style="font-size: 0.72rem;">Active Pipeline</span>
            </div>
    """, unsafe_allow_html=True)

    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.76rem; color: #B9B1C8;">Model Class</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">MultinomialNB</div>
                <div style="font-size: 0.74rem; color: #16D98B; margin-top: 4px;">Alpha: 0.1 (Laplace)</div>
            </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.76rem; color: #B9B1C8;">Vectorizer</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">TF-IDF Matrix</div>
                <div style="font-size: 0.74rem; color: #C084FC; margin-top: 4px;">N-Grams: (1, 2)</div>
            </div>
        """, unsafe_allow_html=True)
    with mcol3:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.76rem; color: #B9B1C8;">Max Features</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-top: 2px;">5,000 Terms</div>
                <div style="font-size: 0.74rem; color: #A855F7; margin-top: 4px;">Min DF: 2</div>
            </div>
        """, unsafe_allow_html=True)
    with mcol4:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 0.75rem; border-radius: 8px;">
                <div style="font-size: 0.76rem; color: #B9B1C8;">Pipeline Status</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #16D98B; margin-top: 2px;">
                    {"Ready (In-Memory)" if classifier.is_ready() else "Not Loaded"}
                </div>
                <div style="font-size: 0.74rem; color: #B9B1C8; margin-top: 4px;">Artifacts Validated</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Section 3: Database & Storage Management
    st.markdown("""
        <div class="saas-card" style="margin-bottom: 1.25rem;">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="font-size: 1.1rem;">🗄️</span>
                    <span class="saas-card-title">Database Storage & Maintenance</span>
                </div>
                <span class="saas-card-action">SQLite Local Engine</span>
            </div>
    """, unsafe_allow_html=True)

    db_col1, db_col2, db_col3 = st.columns([1, 1, 1])
    with db_col1:
        st.markdown(f"""
            <div style="font-size: 0.82rem; color: #B9B1C8;">Database Path:</div>
            <div style="font-family: var(--font-family-mono); font-size: 0.8rem; color: #FFFFFF; word-break: break-all;">
                {HISTORY_DB_PATH.name}
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.82rem; color: #B9B1C8;">File Size:</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #A855F7;">{get_db_file_size()}</div>
        """, unsafe_allow_html=True)

    with db_col2:
        st.markdown(f"""
            <div style="font-size: 0.82rem; color: #B9B1C8;">Total Records:</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">{stats['total_processed']:,}</div>
            <div style="margin-top: 0.5rem; font-size: 0.82rem; color: #B9B1C8;">Spam Ratio:</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #FF536B;">{stats['spam_rate']}%</div>
        """, unsafe_allow_html=True)

    with db_col3:
        if st.button("⚡ Optimize & Vacuum Database", use_container_width=True):
            reindex_database()
            st.success("Database vacuumed and index statistics analyzed.")

        if st.button("🗑 Wipe History Database", use_container_width=True):
            cleared = clear_history()
            st.warning(f"Classification history purged ({cleared} records removed).")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Section 4: Design & Palette Specifications
    st.markdown("""
        <div class="saas-card" style="margin-bottom: 1.25rem;">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="font-size: 1.1rem;">🎨</span>
                    <span class="saas-card-title">Design System & Color Tokens</span>
                </div>
                <span class="saas-card-action">Reference Specification</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.75rem; margin-top: 0.5rem;">
    """, unsafe_allow_html=True)

    color_tokens = [
        ("Background", COLORS["bg"]),
        ("Sidebar", COLORS["sidebar"]),
        ("Topbar", COLORS.get("topbar", "#100D19")),
        ("Card BG", COLORS["card_bg"]),
        ("Border", COLORS["card_border"]),
        ("Primary Purple", COLORS["primary_purple"]),
        ("Bright Purple", COLORS.get("bright_purple", "#A855F7")),
        ("Success Green", COLORS["safe_green"]),
        ("Danger Red", COLORS["spam_red"]),
    ]

    token_html = "".join([
        f"""<div style="background: {cval}; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 0.6rem; text-align: center;">
            <div style="font-size: 0.72rem; font-weight: 600; color: #FFFFFF; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">{cname}</div>
            <div style="font-size: 0.7rem; font-family: var(--font-family-mono); color: #E2E8F0; margin-top: 2px;">{cval}</div>
        </div>""" for cname, cval in color_tokens
    ])

    st.markdown(token_html + "</div></div>", unsafe_allow_html=True)

    # Section 5: Environment & Diagnostics
    st.markdown("""
        <div class="saas-card">
            <div class="saas-card-header">
                <div class="saas-card-title-group">
                    <span style="font-size: 1.1rem;">💻</span>
                    <span class="saas-card-title">System Runtime & Diagnostics</span>
                </div>
                <span class="pill-type-email" style="font-size: 0.72rem;">Environment</span>
            </div>
            <table class="custom-saas-table" style="margin-top: 0.5rem;">
                <thead>
                    <tr>
                        <th>Component</th>
                        <th>Version / Value</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="color: #FFFFFF; font-weight: 600;">Spam Intelligence Core</td>
                        <td style="color: #A78BFA; font-family: var(--font-family-mono);">v1.0.0 Production</td>
                        <td><span class="pill-status-ham">Operational</span></td>
                    </tr>
                    <tr>
                        <td style="color: #FFFFFF; font-weight: 600;">Python Runtime</td>
                        <td style="color: #B9B1C8; font-family: var(--font-family-mono);">{platform.python_version()} ({platform.system()})</td>
                        <td><span class="pill-status-ham">Supported</span></td>
                    </tr>
                    <tr>
                        <td style="color: #FFFFFF; font-weight: 600;">Scikit-learn</td>
                        <td style="color: #B9B1C8; font-family: var(--font-family-mono);">{sklearn.__version__}</td>
                        <td><span class="pill-status-ham">Compatible</span></td>
                    </tr>
                    <tr>
                        <td style="color: #FFFFFF; font-weight: 600;">Pandas & NumPy</td>
                        <td style="color: #B9B1C8; font-family: var(--font-family-mono);">{pandas.__version__} / {numpy.__version__}</td>
                        <td><span class="pill-status-ham">Healthy</span></td>
                    </tr>
                    <tr>
                        <td style="color: #FFFFFF; font-weight: 600;">SQLite Engine</td>
                        <td style="color: #B9B1C8; font-family: var(--font-family-mono);">{sqlite3.sqlite_version}</td>
                        <td><span class="pill-status-ham">Thread-Safe</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    """.format(
        platform=platform,
        sklearn=sklearn,
        pandas=pandas,
        numpy=numpy,
        sqlite3=sqlite3
    ), unsafe_allow_html=True)
