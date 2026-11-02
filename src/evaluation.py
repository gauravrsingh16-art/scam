"""
Model Evaluation and Visualization Module
Computes rigorous classification metrics on held-out test data and generates cybersecurity-themed Plotly charts.
"""

from typing import Dict, Any, Optional, List
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    classification_report
)
from config import COLORS


def compute_metrics(
    y_true: Any,
    y_pred: Any,
    y_prob: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Compute actual evaluation metrics on test ground truth and predictions.
    """
    y_true = np.array(y_true, dtype=int)
    y_pred = np.array(y_pred, dtype=int)

    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, pos_label=1, zero_division=0))
    rec = float(recall_score(y_true, y_pred, pos_label=1, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, pos_label=1, zero_division=0))

    cm = confusion_matrix(y_true, y_pred).tolist()
    # cm layout: [[TN, FP], [FN, TP]]
    tn, fp = cm[0][0], cm[0][1]
    fn, tp = cm[1][0], cm[1][1]

    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0

    auc = None
    roc_data = None
    if y_prob is not None:
        try:
            # Probability for positive class (SPAM = 1)
            if len(y_prob.shape) > 1 and y_prob.shape[1] == 2:
                spam_probs = y_prob[:, 1]
            else:
                spam_probs = y_prob
            auc = float(roc_auc_score(y_true, spam_probs))
            fpr, tpr, thresholds = roc_curve(y_true, spam_probs)
            roc_data = {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
            }
        except Exception:
            auc = None

    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4) if auc is not None else None,
        "specificity": round(specificity, 4),
        "confusion_matrix": cm,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "test_samples_total": len(y_true),
        "roc_curve_data": roc_data,
        "classification_report": report,
    }


def create_confusion_matrix_fig(cm: List[List[int]]) -> go.Figure:
    """
    Generate an impressive cybersecurity-themed Confusion Matrix Heatmap using Plotly.
    """
    tn, fp = cm[0][0], cm[0][1]
    fn, tp = cm[1][0], cm[1][1]

    z = [[tn, fp], [fn, tp]]
    x_labels = ["Predicted NOT SPAM (Ham)", "Predicted SPAM"]
    y_labels = ["Actual NOT SPAM (Ham)", "Actual SPAM"]

    annotations = [
        [f"<b>TN</b><br>{tn}<br><span style='font-size:11px;color:#20C997;'>Correct Legit</span>",
         f"<b>FP</b><br>{fp}<br><span style='font-size:11px;color:#FF5263;'>False Alarm</span>"],
        [f"<b>FN</b><br>{fn}<br><span style='font-size:11px;color:#FF5263;'>Missed Spam</span>",
         f"<b>TP</b><br>{tp}<br><span style='font-size:11px;color:#7657FF;'>Spam Intercepted</span>"]
    ]

    custom_colorscale = [
        [0.0, "#211E29"],
        [0.5, "#4C1D95"],
        [1.0, "#8B5CF6"],
    ]

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x_labels,
        y=y_labels,
        colorscale=custom_colorscale,
        showscale=False,
        text=annotations,
        texttemplate="%{text}",
        textfont={"size": 14, "color": "#F8FAFC", "family": "Plus Jakarta Sans, sans-serif"},
    ))

    fig.update_layout(
        title={
            "text": "<b>Confusion Matrix — Holdout Test Set</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "color": "#F8FAFC"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC", "family": "Plus Jakarta Sans, sans-serif"},
        xaxis=dict(
            tickfont={"size": 12, "color": "#A1A1AA"},
            side="bottom",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            tickfont={"size": 12, "color": "#A1A1AA"},
            autorange="reversed",
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=30, r=30, t=50, b=30),
        height=340,
    )

    return fig


def create_roc_curve_fig(roc_data: Optional[Dict[str, List[float]]], auc_score: Optional[float]) -> go.Figure:
    """Generate interactive Plotly ROC curve with dark cybersecurity theme."""
    fig = go.Figure()

    # Diagonal random baseline
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        line=dict(color=COLORS["text_muted"], dash="dash", width=2),
        name="Random Chance (AUC = 0.50)",
        hoverinfo="none"
    ))

    if roc_data and "fpr" in roc_data and "tpr" in roc_data:
        auc_text = f"{auc_score:.4f}" if auc_score else "N/A"
        fig.add_trace(go.Scatter(
            x=roc_data["fpr"],
            y=roc_data["tpr"],
            mode="lines",
            line=dict(color="#8B5CF6", width=3),
            name=f"Naive Bayes ROC (AUC = {auc_text})",
            fill="tonexty",
            fillcolor="rgba(139, 92, 246, 0.14)",
            hovertemplate="FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>"
        ))

    fig.update_layout(
        title={
            "text": "<b>Receiver Operating Characteristic (ROC Curve)</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "color": "#F8FAFC"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC", "family": "Plus Jakarta Sans, sans-serif"},
        xaxis=dict(
            title="False Positive Rate (FPR)",
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            range=[-0.02, 1.02]
        ),
        yaxis=dict(
            title="True Positive Rate (Recall / TPR)",
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            range=[-0.02, 1.05]
        ),
        legend=dict(
            x=0.45,
            y=0.08,
            bgcolor="rgba(27, 25, 33, 0.8)",
            bordercolor="rgba(139, 92, 246, 0.3)",
            borderwidth=1,
            font={"size": 11, "color": "#F8FAFC"}
        ),
        margin=dict(l=40, r=30, t=50, b=40),
        height=340,
    )

    return fig


def create_metrics_bar_fig(metrics: Dict[str, Any]) -> go.Figure:
    """Generate comparative performance metric bars."""
    metric_names = ["Accuracy", "Precision", "Recall", "F1-Score", "Specificity"]
    metric_values = [
        metrics.get("accuracy", 0.0),
        metrics.get("precision", 0.0),
        metrics.get("recall", 0.0),
        metrics.get("f1_score", 0.0),
        metrics.get("specificity", 0.0),
    ]

    colors = ["#8B5CF6", "#A78BFA", "#F05268", "#22C55E", "#38BDF8"]

    fig = go.Figure(data=[
        go.Bar(
            x=metric_names,
            y=metric_values,
            text=[f"{v * 100:.1f}%" for v in metric_values],
            textposition="outside",
            textfont={"size": 12, "color": "#F8FAFC", "family": "Plus Jakarta Sans, sans-serif"},
            marker=dict(
                color=colors,
                line=dict(color="rgba(255, 255, 255, 0.1)", width=1)
            )
        )
    ])

    fig.update_layout(
        title={
            "text": "<b>Key Performance Indicators (Held-out Test Data)</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "color": "#F8FAFC"}
        },
        paper_bgcolor=COLORS["secondary_bg"],
        plot_bgcolor=COLORS["secondary_bg"],
        font={"color": COLORS["text_white"], "family": "Inter, sans-serif"},
        yaxis=dict(
            range=[0, 1.15],
            gridcolor="rgba(255, 255, 255, 0.08)",
            tickformat=".0%"
        ),
        xaxis=dict(
            tickfont={"size": 12, "color": COLORS["text_white"]},
            showgrid=False
        ),
        margin=dict(l=40, r=40, t=60, b=50),
        height=350,
    )

    return fig


def create_top_features_fig(top_spam: List[Tuple[str, float]], top_ham: List[Tuple[str, float]]) -> go.Figure:
    """
    Generate horizontal bar chart showing top keywords influencing SPAM vs HAM predictions.
    """
    fig = go.Figure()

    if top_spam:
        words = [item[0] for item in top_spam[:10]][::-1]
        scores = [item[1] for item in top_spam[:10]][::-1]
        fig.add_trace(go.Bar(
            y=words,
            x=scores,
            orientation="h",
            name="Top Spam Indicators",
            marker=dict(color=COLORS["spam_red"], line=dict(color="rgba(255, 82, 99, 0.5)", width=1)),
            hovertemplate="Word: %{y}<br>Spam Affinity: %{x:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title={
            "text": "<b>Top Vocabulary Indicators for Spam Detection</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 18, "color": COLORS["text_white"]}
        },
        paper_bgcolor=COLORS["secondary_bg"],
        plot_bgcolor=COLORS["secondary_bg"],
        font={"color": COLORS["text_white"], "family": "Inter, sans-serif"},
        xaxis=dict(
            title="Relative Feature Importance / Log Odds",
            gridcolor="rgba(255, 255, 255, 0.08)",
        ),
        yaxis=dict(
            tickfont={"size": 12, "color": COLORS["text_white"]},
            showgrid=False
        ),
        margin=dict(l=90, r=40, t=60, b=50),
        height=360,
    )

    return fig
