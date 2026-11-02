"""
PAGE 4: BULK MESSAGE DETECTION
Redesigned to match the enterprise SaaS design system (Image 2).
High-speed batch processing for CSV files with dataset preview,
metric cards, filterable results table, and CSV export.
"""

import streamlit as st
import pandas as pd
import io
from config import COLORS, SAMPLE_BULK_CSV
from src.prediction import SpamClassifierService
from src.data_loader import read_data_file, detect_columns


def render_bulk_detection():
    """Render Page 4: Bulk Message Batch Detection."""
    st.markdown("""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Bulk Message <span class="welcome-gradient-text">Batch Processor</span> ▤</div>
                <div class="welcome-subtitle">High-speed batch classification, preview validation, and downloadable intelligence reports</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Card
    st.markdown("""
        <div class="saas-card">
            <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.85rem;">
                Batch Data Ingestion
            </div>
    """, unsafe_allow_html=True)

    col_up1, col_up2 = st.columns([3, 1])

    with col_up1:
        uploaded_file = st.file_uploader(
            "Upload Messages CSV / TSV",
            type=["csv", "tsv", "txt"],
            help="Upload a CSV or TSV file containing message rows. Max size: 15MB."
        )

    with col_up2:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        load_sample = st.button("🧪 Load Sample CSV (20 msgs)", use_container_width=True, help="Load pre-built test dataset with realistic spam and ham mix")

    st.markdown("</div>", unsafe_allow_html=True)

    df_to_process = None

    if load_sample:
        if SAMPLE_BULK_CSV.exists():
            df_to_process = pd.read_csv(SAMPLE_BULK_CSV)
            st.session_state["bulk_df"] = df_to_process
            st.session_state["bulk_source_name"] = "sample_bulk_messages.csv"
        else:
            st.error("Sample dataset file not found on disk.")
    elif uploaded_file is not None:
        try:
            if uploaded_file.size > 15 * 1024 * 1024:
                st.error("⚠️ File size exceeds 15MB limit. Please upload a smaller CSV file.")
                return

            df_to_process = read_data_file(uploaded_file)
            st.session_state["bulk_df"] = df_to_process
            st.session_state["bulk_source_name"] = uploaded_file.name
        except Exception as e:
            st.error(f"❌ Failed to parse uploaded file: {str(e)}")
            return
    elif "bulk_df" in st.session_state:
        df_to_process = st.session_state["bulk_df"]

    if df_to_process is None:
        st.markdown("""
            <div class="saas-card" style="text-align: center; padding: 3rem 1.5rem;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem; opacity: 0.6;">📁</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.4rem;">
                    No Ingestion File Loaded
                </div>
                <div style="font-size: 0.88rem; color: #A1A1AA; max-width: 450px; margin: 0 auto;">
                    Upload a CSV dataset or click <b>"Load Sample CSV"</b> above to test high-throughput batch classification immediately.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    # Dataset Preview & Column Configuration
    st.markdown("""
        <div class="saas-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <div style="font-weight: 700; font-size: 0.95rem;">Corpus Preview: <code>{}</code></div>
                <span class="pill-type-email">{} Rows Loaded</span>
            </div>
    """.format(st.session_state.get('bulk_source_name', 'data.csv'), len(df_to_process)), unsafe_allow_html=True)

    st.dataframe(df_to_process.head(5), use_container_width=True, hide_index=True)

    _, auto_text_col = detect_columns(df_to_process)
    default_index = 0
    col_options = list(df_to_process.columns)
    if auto_text_col and auto_text_col in col_options:
        default_index = col_options.index(auto_text_col)

    c_sel1, c_sel2 = st.columns([2, 1])
    with c_sel1:
        message_column = st.selectbox(
            "Select Message Column",
            options=col_options,
            index=default_index,
            help="Choose the column containing message payload text."
        )

    with c_sel2:
        log_to_history = st.checkbox("Log to Persistent History", value=False)

    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Process & Classify Batch", type="primary", use_container_width=True):
        service = SpamClassifierService.get_instance()
        with st.spinner(f"Vectorizing and classifying {len(df_to_process)} records..."):
            try:
                classified_df = service.predict_bulk(
                    df=df_to_process,
                    text_col=message_column,
                    log_to_db=log_to_history
                )
                st.session_state["classified_bulk_df"] = classified_df
                st.success(f"Classified {len(classified_df)} messages successfully!")
            except Exception as e:
                st.error(f"❌ Batch processing failed: {str(e)}")
                return

    st.markdown("</div>", unsafe_allow_html=True)

    # Batch Telemetry Cards & Results Table
    if "classified_bulk_df" in st.session_state:
        res_df = st.session_state["classified_bulk_df"]
        total_msgs = len(res_df)
        spam_count = int((res_df["Prediction"] == "SPAM").sum())
        ham_count = total_msgs - spam_count
        spam_pct = round((spam_count / total_msgs) * 100, 2) if total_msgs > 0 else 0.0

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top-row">
                        <div class="kpi-icon-box kpi-icon-purple">✉️</div>
                        <div class="kpi-title">Batch Total</div>
                    </div>
                    <div class="kpi-metric-val">{total_msgs:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top-row">
                        <div class="kpi-icon-box kpi-icon-red">🛡️</div>
                        <div class="kpi-title">Spam Intercepted</div>
                    </div>
                    <div class="kpi-metric-val">{spam_count:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top-row">
                        <div class="kpi-icon-box kpi-icon-green">✓</div>
                        <div class="kpi-title">Legitimate (Ham)</div>
                    </div>
                    <div class="kpi-metric-val">{ham_count:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-top-row">
                        <div class="kpi-icon-box kpi-icon-purple">📈</div>
                        <div class="kpi-title">Spam Rate</div>
                    </div>
                    <div class="kpi-metric-val">{spam_pct}%</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
            <div class="saas-card">
                <div class="saas-card-header">
                    <div class="saas-card-title-group">
                        <span style="color: #A78BFA;">📋</span>
                        <span class="saas-card-title">Classified Batch Records</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        filter_option = st.radio(
            "Filter Results View",
            options=["All Records", "Spam Only", "Legitimate (Ham) Only"],
            horizontal=True
        )

        filtered_df = res_df
        if filter_option == "Spam Only":
            filtered_df = res_df[res_df["Prediction"] == "SPAM"]
        elif filter_option == "Legitimate (Ham) Only":
            filtered_df = res_df[res_df["Prediction"] == "NOT SPAM"]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        csv_buffer = io.StringIO()
        res_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        st.download_button(
            label="📥 Download Classified Results as CSV",
            data=csv_bytes,
            file_name="spam_detection_results.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
