"""
Analytics and Dashboard Visualization Module
Produces interactive cybersecurity-themed charts for Dashboard and Analytics views
matching the exact visual design reference (Image 2).
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS


def create_spam_trend_line_chart(history_df: Optional[pd.DataFrame] = None) -> go.Figure:
    """
    Generate the dual-line 'Spam vs Legitimate Trend' chart matching Image 2.
    Features smooth spline curves, circular markers, area fills, and purple palette.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]

    # Baseline monthly volume reflecting benchmark
    base_ham = [620, 710, 850, 1100, 950, 1150, 1080, 1220, 1190, 1310, 1420]
    base_spam = [180, 210, 260, 310, 380, 420, 490, 470, 520, 580, 640]

    if history_df is not None and not history_df.empty:
        total_live_spam = int((history_df["prediction"] == "SPAM").sum())
        total_live_ham = len(history_df) - total_live_spam
        base_spam[-1] += min(total_live_spam * 5, 200)
        base_ham[-1] += min(total_live_ham * 5, 200)

    fig = go.Figure()

    # Spam Trend Line (Vibrant Purple with Area Gradient) - Top/Prominent
    fig.add_trace(go.Scatter(
        x=months,
        y=base_ham,
        name="Not Spam",
        mode="lines+markers",
        line=dict(color="#C084FC", width=3, shape="spline"),
        marker=dict(size=6, color="#C084FC", line=dict(color="#191426", width=2)),
        fill="tozeroy",
        fillcolor="rgba(192, 132, 252, 0.08)",
        hovertemplate="Month: %{x}<br>Not Spam: %{y:,}<extra></extra>"
    ))

    # Spam Trend Line (Neon Purple)
    fig.add_trace(go.Scatter(
        x=months,
        y=base_spam,
        name="Spam",
        mode="lines+markers",
        line=dict(color="#8B35F6", width=3.5, shape="spline"),
        marker=dict(size=7, color="#8B35F6", line=dict(color="#191426", width=2)),
        fill="tozeroy",
        fillcolor="rgba(139, 53, 246, 0.16)",
        hovertemplate="Month: %{x}<br>Spam: %{y:,}<extra></extra>"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B9B1C8", family="Plus Jakarta Sans, sans-serif"),
        showlegend=False,
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#8E859E")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#8E859E"),
            range=[0, 2000],
            dtick=500
        ),
        margin=dict(l=35, r=15, t=10, b=25),
        height=220,
    )

    return fig


def create_monthly_classification_bar_chart(history_df: Optional[pd.DataFrame] = None) -> go.Figure:
    """
    Generate 'Message Classification (Monthly)' grouped bar chart matching Image 2.
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]

    ham_vols = [480, 560, 690, 890, 780, 940, 880, 990, 960, 1050, 1140]
    spam_vols = [140, 160, 210, 250, 310, 340, 390, 380, 420, 460, 510]

    fig = go.Figure()

    # Bright Purple bars (Spam)
    fig.add_trace(go.Bar(
        x=months,
        y=spam_vols,
        name="Spam",
        marker=dict(color="#8B35F6", line=dict(color="rgba(255,255,255,0.05)", width=1)),
        hovertemplate="Spam: %{y:,}<extra></extra>"
    ))

    # Light Purple bars (Not Spam)
    fig.add_trace(go.Bar(
        x=months,
        y=ham_vols,
        name="Not Spam",
        marker=dict(color="#C084FC", line=dict(color="rgba(255,255,255,0.05)", width=1)),
        hovertemplate="Not Spam: %{y:,}<extra></extra>"
    ))

    fig.update_layout(
        barmode="group",
        bargap=0.32,
        bargroupgap=0.1,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B9B1C8", family="Plus Jakarta Sans, sans-serif"),
        showlegend=False,
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#8E859E")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.04)",
            showline=False,
            zeroline=False,
            tickfont=dict(size=11, color="#8E859E"),
            range=[0, 2000],
            dtick=500
        ),
        margin=dict(l=35, r=15, t=10, b=25),
        height=220,
    )

    return fig


def create_spam_distribution_donut(spam_count: int, ham_count: int) -> go.Figure:
    """
    Generate an interactive Plotly Donut Chart representing Spam vs Ham message ratio.
    """
    total = spam_count + ham_count
    if total == 0:
        labels = ["No Data Yet"]
        values = [1]
        colors = ["rgba(255, 255, 255, 0.1)"]
    else:
        labels = ["Spam Intercepted", "Legitimate (Ham)"]
        values = [spam_count, ham_count]
        colors = [COLORS["spam_red"], COLORS["safe_green"]]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.64,
            marker=dict(colors=colors, line=dict(color="#100F14", width=3)),
            textinfo="percent+label" if total > 0 else "label",
            textposition="outside",
            textfont=dict(size=12, color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
            hoverinfo="label+value+percent" if total > 0 else "none",
        )
    ])

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30),
        height=260,
        annotations=[
            dict(
                text=f"<b>{total}</b><br><span style='font-size:11px;color:#A1A1AA;'>Total</span>",
                x=0.5,
                y=0.5,
                font_size=18,
                font_color="#F8FAFC",
                showarrow=False,
            )
        ] if total > 0 else []
    )

    return fig


def create_activity_timeline_chart(history_df: pd.DataFrame) -> go.Figure:
    """
    Generate an activity timeline chart from historical classification records.
    """
    if history_df.empty or "timestamp" not in history_df.columns:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            height=250
        )
        return fig

    df = history_df.copy()
    df["time_slot"] = pd.to_datetime(df["timestamp"]).dt.strftime("%H:00")
    grouped = df.groupby(["time_slot", "prediction"]).size().unstack(fill_value=0).reset_index()

    fig = go.Figure()

    if "SPAM" in grouped.columns:
        fig.add_trace(go.Bar(
            x=grouped["time_slot"],
            y=grouped["SPAM"],
            name="Spam Detected",
            marker_color=COLORS["spam_red"],
            text=grouped["SPAM"],
            textposition="auto"
        ))

    if "NOT SPAM" in grouped.columns:
        fig.add_trace(go.Bar(
            x=grouped["time_slot"],
            y=grouped["NOT SPAM"],
            name="Legitimate Messages",
            marker_color=COLORS["safe_green"],
            text=grouped["NOT SPAM"],
            textposition="auto"
        ))

    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Plus Jakarta Sans, sans-serif"),
        xaxis=dict(
            title="Time Slot",
            gridcolor="rgba(255, 255, 255, 0.05)",
        ),
        yaxis=dict(
            title="Count",
            gridcolor="rgba(255, 255, 255, 0.05)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#F8FAFC")
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        height=260,
    )

    return fig
