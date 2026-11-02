"""
PAGE 6: DATASET MANAGEMENT
Redesigned to match the enterprise SaaS design system (Image 2).
Corpus health diagnostics, schema inspection, class distribution visualizations,
and hyperparameter retraining workstation.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from config import COLORS, RAW_DATASET_CSV
from src.data_loader import load_default_dataset, read_data_file, detect_columns, get_dataset_summary
from src.model_training import train_model
from src.prediction import SpamClassifierService


def render_dataset_management():
    """Render Page 6: Dataset Management & Retraining."""
    st.markdown("""
        <div class="welcome-section">
            <div>
                <div class="welcome-title">Dataset Management & <span class="welcome-gradient-text">Retraining</span> 🗄</div>
                <div class="welcome-subtitle">Corpus integrity diagnostics, multi-schema mapping, and ML model retraining workstation</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    df = load_default_dataset()
    det_label, det_text = detect_columns(df)
    label_col = det_label or "v1"
    text_col = det_text or "v2"
    summary = get_dataset_summary(df, label_col=label_col, text_col=text_col)

    # Health Statistics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-purple">🗄</div>
                    <div class="kpi-title">Total Records</div>
                </div>
                <div class="kpi-metric-val">{summary['total_rows']:,}</div>
                <div class="trend-desc">Raw corpus rows</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-red">🛡️</div>
                    <div class="kpi-title">Spam Records</div>
                </div>
                <div class="kpi-metric-val">{summary['spam_records']:,}</div>
                <div class="trend-desc">{summary['spam_percentage']}% of corpus</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-green">✓</div>
                    <div class="kpi-title">Legitimate Records</div>
                </div>
                <div class="kpi-metric-val">{summary['ham_records']:,}</div>
                <div class="trend-desc">{summary['ham_percentage']}% of corpus</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-purple">⚠️</div>
                    <div class="kpi-title">Missing Values</div>
                </div>
                <div class="kpi-metric-val">{summary['missing_text_values'] + summary['missing_label_values']}</div>
                <div class="trend-desc">Null entries</div>
            </div>
        """, unsafe_allow_html=True)
    with m5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-top-row">
                    <div class="kpi-icon-box kpi-icon-purple">📑</div>
                    <div class="kpi-title">Duplicate Texts</div>
                </div>
                <div class="kpi-metric-val">{summary['duplicate_records']:,}</div>
                <div class="trend-desc">Repeated messages</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Corpus Diagnostics & Preview", "⚙️ Retrain / Ingest Custom Corpus"])

    with tab1:
        dcol1, dcol2 = st.columns([1, 1])

        with dcol1:
            st.markdown("""
                <div class="saas-card" style="padding-bottom: 0.5rem;">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #A78BFA;">📊</span>
                            <span class="saas-card-title">Class Distribution (Imbalance Profile)</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            dist_df = pd.DataFrame({
                "Category": ["Legitimate (Ham)", "Spam"],
                "Count": [summary["ham_records"], summary["spam_records"]]
            })
            bar_dist_fig = px.bar(
                dist_df,
                x="Category",
                y="Count",
                color="Category",
                color_discrete_map={"Spam": COLORS["spam_red"], "Legitimate (Ham)": COLORS["safe_green"]},
                text="Count"
            )
            bar_dist_fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
                showlegend=False,
                height=260,
                margin=dict(l=30, r=20, t=20, b=30),
                yaxis=dict(gridcolor="rgba(255, 255, 255, 0.05)")
            )
            st.plotly_chart(bar_dist_fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with dcol2:
            st.markdown("""
                <div class="saas-card">
                    <div class="saas-card-header">
                        <div class="saas-card-title-group">
                            <span style="color: #8B5CF6;">ℹ️</span>
                            <span class="saas-card-title">Corpus Schema Specification</span>
                        </div>
                    </div>
                    <div style="font-size: 0.85rem; line-height: 1.8; color: #A1A1AA;">
            """, unsafe_allow_html=True)
            st.markdown(f"""
                - **Primary Benchmark:** `UCI Machine Learning Repository — SMS Spam Collection`
                - **Target Label Column:** `'{label_col}'` (Normalized: <code>ham</code> → 0, <code>spam</code> → 1)
                - **Text Message Column:** `'{text_col}'`
                - **Supported Aliases:** `v1/v2`, `label/text`, `category/message`, `type/sms`
                - **Storage Path:** `data/raw/sms_spam_collection.csv`
            """)
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class="saas-card">
                <div class="saas-card-header">
                    <div class="saas-card-title-group">
                        <span style="color: #A78BFA;">📋</span>
                        <span class="saas-card-title">Raw Corpus Records Preview (First 10 Rows)</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
            <div class="saas-card">
                <div class="saas-card-header">
                    <div class="saas-card-title-group">
                        <span style="color: #8B5CF6;">⚙️</span>
                        <span class="saas-card-title">Model Retraining & Hyperparameter Engineering</span>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        custom_file = st.file_uploader(
            "Upload Custom Training Corpus (Optional)",
            type=["csv", "tsv"],
            key="train_file_uploader",
            help="Upload custom CSV/TSV with label and text columns. If omitted, default UCI benchmark dataset is used."
        )

        custom_df = None
        if custom_file is not None:
            try:
                custom_df = read_data_file(custom_file)
                st.info(f"Loaded custom dataset '{custom_file.name}' ({len(custom_df)} rows).")
            except Exception as e:
                st.error(f"Failed to read custom file: {str(e)}")

        target_df = custom_df if custom_df is not None else load_default_dataset()

        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            vec_type = st.selectbox(
                "Feature Extraction Method",
                options=["tfidf", "count"],
                format_func=lambda x: "TF-IDF Vectorizer (Sublinear TF)" if x == "tfidf" else "CountVectorizer (Bag-of-Words)"
            )
            ngram_opt = st.selectbox(
                "N-gram Range",
                options=[(1, 1), (1, 2), (1, 3)],
                index=1,
                format_func=lambda x: f"Unigrams ({x[0]},{x[1]})" if x == (1,1) else f"Unigrams + Bigrams ({x[0]},{x[1]})" if x == (1,2) else f"Unigrams to Trigrams ({x[0]},{x[1]})"
            )

        with h_col2:
            max_feats = st.select_slider(
                "Max Vocabulary Dimension",
                options=[1000, 2500, 5000, 7500, 10000],
                value=5000
            )
            min_df_val = st.slider("Min Document Frequency (min_df)", min_value=1, max_value=5, value=2)

        with h_col3:
            alpha_val = st.slider("Laplace Smoothing (α)", min_value=0.01, max_value=2.0, value=0.1, step=0.05)
            drop_dups = st.checkbox("Drop Duplicate Message Texts", value=False)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Retrain Model Pipeline with Parameters", type="primary", use_container_width=True):
            with st.spinner("Executing training pipeline and evaluating test set..."):
                try:
                    result = train_model(
                        df=target_df,
                        vectorizer_type=vec_type,
                        ngram_range=ngram_opt,
                        max_features=max_feats,
                        min_df=min_df_val,
                        alpha=alpha_val,
                        drop_duplicates=drop_dups
                    )
                    SpamClassifierService.get_instance(force_reload=True)

                    st.success(f"""
                        🎉 Model Retrained Successfully!
                        - **New Test Accuracy:** {result['test_metrics']['accuracy'] * 100:.2f}%
                        - **Spam Precision:** {result['test_metrics']['precision'] * 100:.2f}%
                        - **Spam Recall:** {result['test_metrics']['recall'] * 100:.2f}%
                        - **Vocabulary Size:** {result['hyperparameters']['vocabulary_size']} tokens
                    """)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Training failed: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)
