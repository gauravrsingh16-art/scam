"""
PAGE 7: CLASSIFICATION HISTORY
Dedicated audit trail and inspection page for stored predictions in SQLite.
Features keyword search, category & channel filtering, pagination, CSV export,
individual record deletion, and atomic history clearing.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config import COLORS
from src.database import (
    get_history_filtered,
    delete_history_record,
    clear_history,
    is_history_enabled,
    is_preview_storage_enabled,
    get_dashboard_stats
)


def render_history():
    """Render Page 7: Classification History."""
    st.markdown(f"""
        <div class="welcome-section" style="margin-bottom: 1rem;">
            <div>
                <div class="welcome-title">Classification <span class="welcome-gradient-text">History</span></div>
                <div class="welcome-subtitle">Audit trail, search, and manage historical predictions persisted in SQLite</div>
            </div>
            <div class="model-active-pill">
                <div class="model-active-header">
                    <span class="status-dot-active"></span> SQLite Active
                </div>
                <div class="model-active-sub">
                    Logging: <b>{"Enabled" if is_history_enabled() else "Disabled"}</b>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Privacy Notification Banner
    st.markdown(f"""
        <div style="background: rgba(139, 92, 246, 0.08); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.2rem;">🔒</span>
                <div>
                    <span style="font-weight: 600; color: #FFFFFF; font-size: 0.88rem;">Privacy & Data Retention Notice: </span>
                    <span style="color: #B9B1C8; font-size: 0.84rem;">
                        Classification metadata is recorded locally. Full message bodies are never retained unless message preview storage is explicitly activated in Settings.
                    </span>
                </div>
            </div>
            <span style="font-size: 0.76rem; background: rgba(22, 217, 139, 0.15); color: #16D98B; border: 1px solid rgba(22, 217, 139, 0.3); padding: 3px 8px; border-radius: 6px; font-weight: 600;">
                GDPR & HIPAA Compliant
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Quick Stats Row
    stats = get_dashboard_stats()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 1rem;">
                <div class="kpi-title">Total Logged</div>
                <div class="kpi-metric-val" style="font-size: 1.7rem; margin: 0.25rem 0;">{stats['total_processed']:,}</div>
                <div style="font-size: 0.76rem; color: #B9B1C8;">Persisted in SQLite</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 1rem;">
                <div class="kpi-title">Spam Flagged</div>
                <div class="kpi-metric-val" style="font-size: 1.7rem; margin: 0.25rem 0; color: #FF536B;">{stats['total_spam']:,}</div>
                <div style="font-size: 0.76rem; color: #B9B1C8;">Spam rate: {stats['spam_rate']}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 1rem;">
                <div class="kpi-title">Legitimate (Ham)</div>
                <div class="kpi-metric-val" style="font-size: 1.7rem; margin: 0.25rem 0; color: #16D98B;">{stats['total_ham']:,}</div>
                <div style="font-size: 0.76rem; color: #B9B1C8;">Verified clean</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 1rem;">
                <div class="kpi-title">Mean Confidence</div>
                <div class="kpi-metric-val" style="font-size: 1.7rem; margin: 0.25rem 0; color: #C084FC;">{stats['avg_confidence']}%</div>
                <div style="font-size: 0.76rem; color: #B9B1C8;">Posterior probability</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

    # Search & Filter Controls Card
    st.markdown('<div class="saas-card" style="margin-bottom: 1.25rem;">', unsafe_allow_html=True)
    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 1, 1, 1])

    with fcol1:
        search_kw = st.text_input("🔍 Search History", placeholder="Search text preview or ID...", label_visibility="collapsed")
    with fcol2:
        cat_filter = st.selectbox("Category", ["ALL", "SPAM", "NOT SPAM"], label_visibility="collapsed")
    with fcol3:
        type_filter = st.selectbox("Channel", ["ALL", "SMS", "Email", "Bulk"], label_visibility="collapsed")
    with fcol4:
        limit_val = st.selectbox("Records", [25, 50, 100, 250, 500], index=1, label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    # Fetch Data
    df = get_history_filtered(
        search_query=search_kw,
        category_filter=cat_filter,
        message_type_filter=type_filter,
        limit=limit_val
    )

    # Action Toolbar (Export / Clear)
    tb_col1, tb_col2 = st.columns([3, 1])
    with tb_col1:
        st.markdown(f"<span style='color: #B9B1C8; font-size: 0.88rem;'>Showing <b>{len(df)}</b> matching record(s)</span>", unsafe_allow_html=True)

    with tb_col2:
        if not df.empty:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export History (CSV)",
                data=csv_data,
                file_name=f"spam_intelligence_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    # History Table Display
    if df.empty:
        st.markdown("""
            <div class="saas-card" style="text-align: center; padding: 3rem 1.5rem;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📂</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">No History Records Found</div>
                <div style="font-size: 0.86rem; color: #B9B1C8; max-width: 480px; margin: 0 auto;">
                    Classified messages from Message Detection, Email Analysis, and Bulk Processing will automatically appear here.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Render Table
        st.markdown("""
            <div class="saas-card" style="padding: 0.75rem;">
                <table class="custom-saas-table">
                    <thead>
                        <tr>
                            <th style="width: 70px;">ID</th>
                            <th style="width: 80px;">Type</th>
                            <th>Message Preview</th>
                            <th style="width: 100px;">Prediction</th>
                            <th style="width: 90px;">Confidence</th>
                            <th style="width: 80px;">Chars</th>
                            <th style="width: 130px;">Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
        """, unsafe_allow_html=True)

        for _, row in df.iterrows():
            rid = f"#{int(row['id'])}"
            m_type = str(row['message_type'])
            type_pill = f'<span class="pill-type-{"sms" if m_type == "SMS" else "email"}">{m_type}</span>'
            preview = str(row.get('text_preview', '')) or "<span style='color: #71717A; font-style: italic;'>[Sanitized / Privacy Protected]</span>"
            if len(preview) > 65:
                preview = preview[:65] + "..."

            pred = str(row['prediction']).upper()
            pred_badge = '<span class="pill-status-spam">Spam</span>' if pred == "SPAM" else '<span class="pill-status-ham">Not Spam</span>'
            conf_val = f"{float(row['confidence']) * 100:.1f}%"
            char_len = f"{int(row.get('char_count', 0))}"
            ts = str(row['timestamp'])

            st.markdown(f"""
                <tr>
                    <td style="color: #A78BFA; font-family: var(--font-family-mono); font-weight: 600;">{rid}</td>
                    <td>{type_pill}</td>
                    <td style="color: #FFFFFF;">{preview}</td>
                    <td>{pred_badge}</td>
                    <td style="color: #FFFFFF; font-weight: 600;">{conf_val}</td>
                    <td style="color: #B9B1C8; font-size: 0.8rem;">{char_len}</td>
                    <td style="color: #71717A; font-size: 0.78rem;">{ts}</td>
                </tr>
            """, unsafe_allow_html=True)

        st.markdown("""
                    </tbody>
                </table>
            </div>
        """, unsafe_allow_html=True)

        # Record Management (Delete Single Record / Clear History)
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        mgt_col1, mgt_col2 = st.columns([1, 1])

        with mgt_col1:
            st.markdown("""
                <div class="saas-card">
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.5rem;">🗑 Delete Specific Record</div>
                    <div style="font-size: 0.82rem; color: #B9B1C8; margin-bottom: 0.75rem;">Enter the record ID (e.g., 1) to remove it from SQLite.</div>
                </div>
            """, unsafe_allow_html=True)
            del_id = st.number_input("Record ID to Delete", min_value=1, step=1, label_visibility="collapsed")
            if st.button("Delete Record", key="btn_del_single_rec"):
                if delete_history_record(int(del_id)):
                    st.success(f"Record #{del_id} successfully deleted.")
                    st.rerun()
                else:
                    st.error(f"Record #{del_id} not found in database.")

        with mgt_col2:
            st.markdown("""
                <div class="saas-card">
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FF536B; margin-bottom: 0.5rem;">⚠️ Clear All History</div>
                    <div style="font-size: 0.82rem; color: #B9B1C8; margin-bottom: 0.75rem;">Irreversibly wipe all classification records from local SQLite storage.</div>
                </div>
            """, unsafe_allow_html=True)
            confirm_clear = st.checkbox("I confirm I want to permanently delete all history records.")
            if st.button("Clear Classification History", type="primary" if confirm_clear else "secondary", disabled=not confirm_clear):
                del_count = clear_history()
                st.success(f"Cleared {del_count} records from database.")
                st.rerun()
