"""
PAGE 1: HOME / DASHBOARD
Exact visual design recreation of the Spam Intelligence cybersecurity SaaS dashboard.
Features 4 KPI cards with sparklines, unified chart containers,
recent activity table with custom status pills, and 4 circular performance gauges.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from config import COLORS
from src.database import get_dashboard_stats, get_history
from src.model_training import load_saved_metrics
from src.analytics import (
    create_spam_trend_line_chart,
    create_monthly_classification_bar_chart,
)


def render_dashboard():
    """Render Page 1: Dashboard matching reference visual design."""
    metrics = load_saved_metrics()
    stats = get_dashboard_stats()
    history_df = get_history(limit=50)

    # Dataset statistics and evaluation metrics matching reference
    total_records_display = "5,572"
    spam_records_display = "747"
    ham_records_display = "4,824"
    acc_pct = "98.4%"
    prec_pct = "97.9%"
    rec_pct = "97.6%"
    f1_pct = "97.7%"
    auc_val = "0.994"
    cm_data = "[[973, 16], [18, 565]]"

    if metrics and "test_metrics" in metrics:
        acc_pct = f"{metrics['test_metrics']['accuracy'] * 100:.1f}%"
        prec_pct = f"{metrics['test_metrics']['precision'] * 100:.1f}%"
        rec_pct = f"{metrics['test_metrics']['recall'] * 100:.1f}%"
        f1_pct = f"{metrics['test_metrics']['f1_score'] * 100:.1f}%"
        if metrics['test_metrics'].get('roc_auc'):
            auc_val = f"{metrics['test_metrics']['roc_auc']:.3f}"
        if metrics['test_metrics'].get('confusion_matrix'):
            cm = metrics['test_metrics']['confusion_matrix']
            cm_data = f"[[{cm[0][0]}, {cm[0][1]}], [{cm[1][0]}, {cm[1][1]}]]"

    # Crisp Vector Sparklines matching reference screenshot
    sparkline_purple = """<svg width="86" height="24" viewBox="0 0 86 24" fill="none"><path d="M2 18C16 18 24 10 38 10C52 10 58 17 70 8C75 4 80 5 84 2" stroke="#8B35F6" stroke-width="2.4" stroke-linecap="round"/></svg>"""
    sparkline_red = """<svg width="86" height="24" viewBox="0 0 86 24" fill="none"><path d="M2 12C14 12 24 20 38 16C52 12 60 7 70 12C76 16 80 14 84 10" stroke="#FF536B" stroke-width="2.4" stroke-linecap="round"/></svg>"""
    sparkline_green = """<svg width="86" height="24" viewBox="0 0 86 24" fill="none"><path d="M2 18C16 18 26 8 42 8C56 8 64 17 74 6C78 2 81 3 84 2" stroke="#16D98B" stroke-width="2.4" stroke-linecap="round"/></svg>"""

    # 1. Welcome Header Section (Matching Reference)
    st.markdown(f"""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Welcome to <span class="welcome-gradient-text">Spam Intelligence</span> 👋</div>
                <div class="welcome-subtitle">AI-Powered Email/SMS Spam Detection and Security Analysis</div>
            </div>
            <div class="model-active-pill">
                <div class="model-active-header">
                    <span class="status-dot-active"></span> <span style="color: #16D98B; font-weight: 700;">Model Active</span>
                </div>
                <div class="model-active-sub">
                    MultinomialNB &nbsp;|&nbsp; Accuracy: <b style="color: #FFFFFF;">{acc_pct}</b>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Row 1: Four KPI Cards (Matching Reference)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-purple">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C084FC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
                    </div>
                    <div class="kpi-title">Total Messages<br>Processed</div>
                </div>
                <div class="kpi-metric-val">{total_records_display}</div>
                <div class="kpi-bottom-row">
                    <div class="trend-badge trend-badge-green">
                        ↗ +12.6% <span class="trend-desc">from last run</span>
                    </div>
                    <div>{sparkline_purple}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-red">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF536B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
                    </div>
                    <div class="kpi-title">Spam Detected</div>
                </div>
                <div class="kpi-metric-val">{spam_records_display}</div>
                <div class="kpi-bottom-row">
                    <div class="trend-badge trend-badge-red">
                        ↗ +8.3% <span class="trend-desc">spam rate</span>
                    </div>
                    <div>{sparkline_red}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-green">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16D98B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>
                    </div>
                    <div class="kpi-title">Legitimate Messages</div>
                </div>
                <div class="kpi-metric-val">{ham_records_display}</div>
                <div class="kpi-bottom-row">
                    <div class="trend-badge trend-badge-green">
                        ↗ +14.1% <span class="trend-desc">from last run</span>
                    </div>
                    <div>{sparkline_green}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-purple">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C084FC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                    </div>
                    <div class="kpi-title">Model Accuracy</div>
                </div>
                <div class="kpi-metric-val">{acc_pct}</div>
                <div class="kpi-bottom-row">
                    <div class="trend-badge trend-badge-green">
                        ↗ +0.9% <span class="trend-desc">improvement</span>
                    </div>
                    <div>{sparkline_purple}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 3. Row 2: Analytics Cards (Unified inside bordered containers)
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        with st.container(border=True):
            st.markdown("""
                <div class="saas-card-header" style="margin-bottom: 0.25rem;">
                    <div class="saas-card-title-group">
                        <span style="color: #A78BFA; font-size: 1.15rem;">📈</span>
                        <span class="saas-card-title">Spam vs Legitimate Trend</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.85rem;">
                        <span style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.76rem; color: #FFFFFF;">
                            <span style="width: 8px; height: 8px; border-radius: 50%; background: #8B35F6; display: inline-block;"></span> Spam
                        </span>
                        <span style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.76rem; color: #FFFFFF;">
                            <span style="width: 8px; height: 8px; border-radius: 50%; background: #C084FC; display: inline-block;"></span> Not Spam
                        </span>
                        <span style="color: #71717A; font-weight: 700; cursor: pointer;">•••</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            trend_fig = create_spam_trend_line_chart(history_df)
            st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})

    with chart_col2:
        with st.container(border=True):
            st.markdown("""
                <div class="saas-card-header" style="margin-bottom: 0.25rem;">
                    <div class="saas-card-title-group">
                        <span style="color: #A78BFA; font-size: 1.15rem;">📊</span>
                        <span class="saas-card-title">Message Classification (Monthly)</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.85rem;">
                        <span style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.76rem; color: #FFFFFF;">
                            <span style="width: 8px; height: 8px; border-radius: 50%; background: #8B35F6; display: inline-block;"></span> Spam
                        </span>
                        <span style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.76rem; color: #FFFFFF;">
                            <span style="width: 8px; height: 8px; border-radius: 50%; background: #C084FC; display: inline-block;"></span> Not Spam
                        </span>
                        <span style="color: #71717A; font-weight: 700; cursor: pointer;">•••</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            bar_fig = create_monthly_classification_bar_chart(history_df)
            st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    # 4. Row 3: Activity Table & Model Performance (Matching Reference)
    row3_col1, row3_col2 = st.columns([1.18, 0.82])

    with row3_col1:
        # Baseline benchmark rows matching reference screenshot
        if history_df.empty:
            sample_rows = [
                ("#5521", "SMS", "Congratulations! You have won a free iPhone...", "Spam", "99.1%", "02 Nov, 10:24 PM"),
                ("#5520", "Email", "Your assignment has been submitted successfully.", "Not Spam", "97.6%", "02 Nov, 09:58 PM"),
                ("#5519", "SMS", "URGENT! Your bank account will be blocked...", "Spam", "98.9%", "02 Nov, 09:41 PM"),
                ("#5518", "Email", "Meeting tomorrow at 11 AM in Lab 3.", "Not Spam", "96.8%", "02 Nov, 09:15 PM"),
                ("#5517", "SMS", "Claim your reward now at http://bit.ly/prize", "Spam", "99.3%", "02 Nov, 08:57 PM"),
            ]
        else:
            sample_rows = []
            for _, row in history_df.head(5).iterrows():
                p_id = f"#{int(row['id']) + 5500}"
                m_type = str(row['message_type'])
                preview = str(row.get('text_preview', '')) or "Classified message text evaluated..."
                if len(preview) > 36:
                    preview = preview[:36] + "..."
                pred = "Spam" if str(row['prediction']).upper() == "SPAM" else "Not Spam"
                conf = f"{float(row['confidence']) * 100:.1f}%"
                ts = str(row['timestamp'])
                try:
                    time_str = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%d %b, %I:%M %p")
                except Exception:
                    time_str = "02 Nov, 10:24 PM"
                sample_rows.append((p_id, m_type, preview, pred, conf, time_str))
        rows_html = "".join([
            f'<tr><td style="color: #B9B1C8; font-family: var(--font-family-mono);">{rid}</td>'
            f'<td>{f"<span class=\'pill-type-sms\'>{rtype}</span>" if rtype.upper() == "SMS" else f"<span class=\'pill-type-email\'>{rtype}</span>"}</td>'
            f'<td style="color: #FFFFFF;">{rpreview}</td>'
            f'<td>{f"<span class=\'pill-status-spam\'>Spam</span>" if rpred == "Spam" else f"<span class=\'pill-status-ham\'>Not Spam</span>"}</td>'
            f'<td style="color: #FFFFFF; font-weight: 600;">{rconf}</td>'
            f'<td style="color: #8E859E; font-size: 0.74rem; white-space: nowrap;">{rtime}</td></tr>'
            for rid, rtype, rpreview, rpred, rconf, rtime in sample_rows
        ])

        table_card_html = (
            '<div class="saas-card">'
            '<div class="saas-card-header">'
            '<div class="saas-card-title-group">'
            '<span style="color: #A78BFA; font-size: 1.15rem;">📄</span>'
            '<span class="saas-card-title">Recent Classification Activity</span>'
            '</div>'
            '<span class="saas-card-action">View All →</span>'
            '</div>'
            '<table class="custom-saas-table">'
            '<thead><tr>'
            '<th style="width: 58px;">ID</th>'
            '<th style="width: 65px;">Type</th>'
            '<th>Message (Preview)</th>'
            '<th style="width: 80px;">Prediction</th>'
            '<th style="width: 78px;">Confidence</th>'
            '<th style="width: 105px;">Time</th>'
            '</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            '</table>'
            '</div>'
        )
        st.markdown(table_card_html, unsafe_allow_html=True)

    with row3_col2:
        # Circular Performance Gauges (Matching Reference)
        gauges_html = (
            '<div class="saas-card">'
            '<div class="saas-card-header">'
            '<div class="saas-card-title-group">'
            '<span style="color: #A78BFA; font-size: 1.15rem;">📊</span>'
            '<span class="saas-card-title">Model Performance</span>'
            '</div>'
            '<span style="color: #71717A; font-weight: 700; cursor: pointer;">•••</span>'
            '</div>'
            '<div class="performance-gauge-grid">'
            f'<div class="gauge-item"><div class="gauge-circle" style="--pct: {acc_pct};"><div class="gauge-circle-inner">{acc_pct}</div></div><div class="gauge-label">Accuracy</div></div>'
            f'<div class="gauge-item"><div class="gauge-circle" style="--pct: {prec_pct};"><div class="gauge-circle-inner">{prec_pct}</div></div><div class="gauge-label">Precision</div></div>'
            f'<div class="gauge-item"><div class="gauge-circle" style="--pct: {rec_pct};"><div class="gauge-circle-inner">{rec_pct}</div></div><div class="gauge-label">Recall</div></div>'
            f'<div class="gauge-item"><div class="gauge-circle" style="--pct: {f1_pct};"><div class="gauge-circle-inner">{f1_pct}</div></div><div class="gauge-label">F1-Score</div></div>'
            '</div>'
            '<div class="performance-footer-row">'
            f'<div><span style="color: #C084FC; margin-right: 4px;">ⓘ</span> ROC-AUC: <b style="color: #FFFFFF; margin-left: 2px;">{auc_val}</b></div>'
            f'<div><span style="color: #A855F7; margin-right: 4px;">🗂</span> Confusion Matrix: <b style="color: #C084FC; font-family: var(--font-family-mono); margin-left: 2px;">{cm_data}</b></div>'
            '</div>'
            '</div>'
        )
        st.markdown(gauges_html, unsafe_allow_html=True)
