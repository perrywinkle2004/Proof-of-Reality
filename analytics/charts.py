"""
Chart generation for Proof-of-Reality Analytics Dashboard
Uses matplotlib/seaborn for all visualizations.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from analytics.tracker import (
    get_verification_stats,
    get_score_distribution,
    get_trust_score_distribution,
    get_time_trends,
    get_per_user_stats,
)

# ── Global style setup ──────────────────────────────────────────────────────

DARK_BG = "#06010f"
CARD_BG = "#0d0820"
PURPLE = "#7c3aed"
BLUE = "#3b82f6"
CYAN = "#06b6d4"
GREEN = "#10b981"
RED = "#ef4444"
ORANGE = "#f59e0b"
TEXT_COLOR = "#f0eaff"
MUTED_COLOR = "#a78bfa"
GRID_COLOR = "#1a1035"


def _setup_dark_style():
    plt.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor": CARD_BG,
        "axes.edgecolor": "#1a1035",
        "axes.labelcolor": TEXT_COLOR,
        "xtick.color": MUTED_COLOR,
        "ytick.color": MUTED_COLOR,
        "text.color": TEXT_COLOR,
        "grid.color": GRID_COLOR,
        "grid.linewidth": 0.5,
        "font.family": "sans-serif",
        "font.size": 11,
    })


def chart_verification_donut() -> plt.Figure:
    """Donut chart: Verified vs Suspicious vs Needs Review."""
    stats = get_verification_stats()
    _setup_dark_style()

    labels = ["Verified ✅", "Suspicious ❌", "Needs Review ⚠️"]
    values = [stats["verified"], stats["suspicious"], stats["needs_review"]]
    colors = [GREEN, RED, ORANGE]

    # Avoid empty chart
    if sum(values) == 0:
        values = [1, 0, 0]

    fig, ax = plt.subplots(figsize=(5, 5), facecolor=DARK_BG)
    wedges, texts, autotexts = ax.pie(
        values, labels=None, colors=colors,
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2),
        pctdistance=0.75,
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)
        at.set_fontweight("bold")

    # Center text
    ax.text(0, 0.1, str(sum(values)), ha="center", va="center",
            fontsize=22, fontweight="bold", color=TEXT_COLOR)
    ax.text(0, -0.2, "TOTAL", ha="center", va="center",
            fontsize=9, color=MUTED_COLOR, fontfamily="monospace")

    legend_patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
    ax.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.12),
              ncol=3, fontsize=8, frameon=False, labelcolor=TEXT_COLOR)

    ax.set_title("Verification Distribution", color=TEXT_COLOR, fontsize=13, pad=15)
    fig.tight_layout()
    return fig


def chart_authenticity_bar() -> plt.Figure:
    """Bar chart: Authenticity score distribution by bucket."""
    dist = get_score_distribution()
    _setup_dark_style()

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=DARK_BG)

    labels = list(dist.keys())
    values = list(dist.values())
    bar_colors = [RED, ORANGE, ORANGE, BLUE, GREEN]

    bars = ax.bar(labels, values, color=bar_colors, edgecolor=DARK_BG,
                  linewidth=1.5, width=0.65)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    str(val), ha="center", va="bottom", fontsize=10,
                    fontweight="bold", color=TEXT_COLOR)

    ax.set_xlabel("Authenticity Score Range", labelpad=10)
    ax.set_ylabel("Number of Proofs", labelpad=10)
    ax.set_title("Authenticity Score Distribution", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def chart_trust_score_hist() -> plt.Figure:
    """Histogram: User trust score distribution."""
    scores = get_trust_score_distribution()
    _setup_dark_style()

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=DARK_BG)

    if scores:
        n, bins, patches = ax.hist(scores, bins=10, range=(0, 100),
                                    color=PURPLE, edgecolor=DARK_BG, linewidth=1.5, alpha=0.85)
        # Color gradient on bars
        for patch, val in zip(patches, bins):
            if val < 33:
                patch.set_facecolor(RED)
            elif val < 66:
                patch.set_facecolor(ORANGE)
            else:
                patch.set_facecolor(GREEN)
    else:
        ax.text(0.5, 0.5, "No data yet", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)

    ax.set_xlabel("Trust Score", labelpad=10)
    ax.set_ylabel("Number of Users", labelpad=10)
    ax.set_title("User Trust Score Distribution", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.set_xlim(0, 100)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def chart_time_trends() -> plt.Figure:
    """Stacked bar chart: monthly submission trends."""
    trends = get_time_trends()
    _setup_dark_style()

    fig, ax = plt.subplots(figsize=(8, 4), facecolor=DARK_BG)

    if not trends:
        ax.text(0.5, 0.5, "No trend data yet", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        ax.set_title("Monthly Submission Trends", color=TEXT_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    months = list(trends.keys())
    verified_vals = [trends[m]["VERIFIED"] for m in months]
    suspicious_vals = [trends[m]["SUSPICIOUS"] for m in months]
    review_vals = [trends[m]["NEEDS_REVIEW"] for m in months]

    x = range(len(months))
    width = 0.6

    p1 = ax.bar(x, verified_vals, width, label="Verified", color=GREEN, edgecolor=DARK_BG)
    p2 = ax.bar(x, suspicious_vals, width, bottom=verified_vals,
                label="Suspicious", color=RED, edgecolor=DARK_BG)
    review_bottoms = [v + s for v, s in zip(verified_vals, suspicious_vals)]
    p3 = ax.bar(x, review_vals, width, bottom=review_bottoms,
                label="Needs Review", color=ORANGE, edgecolor=DARK_BG)

    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=30, ha="right", fontsize=9)
    ax.set_xlabel("Month", labelpad=10)
    ax.set_ylabel("Submissions", labelpad=10)
    ax.set_title("Monthly Submission Trends", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.legend(fontsize=9, frameon=False, labelcolor=TEXT_COLOR)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def chart_fraud_detection_gauge(fraud_rate: float) -> plt.Figure:
    """Gauge-style chart for fraud detection rate."""
    _setup_dark_style()
    fig, ax = plt.subplots(figsize=(5, 3), facecolor=DARK_BG, subplot_kw=dict(polar=False))

    # Half-donut gauge using wedges
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.axis("off")

    # Background arc
    theta = np.linspace(0, np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), color=GRID_COLOR, linewidth=20, solid_capstyle="round")

    # Filled arc (fraud rate)
    fill_end = np.pi * (1 - fraud_rate / 100)
    theta_fill = np.linspace(fill_end, np.pi, 100)
    color = RED if fraud_rate > 40 else ORANGE if fraud_rate > 20 else GREEN
    ax.plot(np.cos(theta_fill), np.sin(theta_fill), color=color,
            linewidth=20, solid_capstyle="round")

    # Center text
    ax.text(0, 0.1, f"{fraud_rate:.1f}%", ha="center", va="center",
            fontsize=24, fontweight="bold", color=color)
    ax.text(0, -0.1, "FRAUD RATE", ha="center", va="center",
            fontsize=9, color=MUTED_COLOR, fontfamily="monospace")

    ax.set_title("Fraud Detection Rate", color=TEXT_COLOR, fontsize=13, pad=10)
    fig.tight_layout()
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEW DASHBOARD CHARTS (added — original charts above are untouched)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chart_proofs_over_time() -> plt.Figure:
    """Cumulative line chart: total proofs over time."""
    from utils.helpers import load_records
    from datetime import datetime

    _setup_dark_style()
    records = load_records()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=DARK_BG)

    if not records:
        ax.text(0.5, 0.5, "No data yet", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        ax.set_title("Total Proofs Over Time", color=TEXT_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    # Parse dates and sort
    dated = []
    for r in records:
        try:
            dt = datetime.fromisoformat(r.get("timestamp", "2024-01-01"))
            dated.append(dt.strftime("%Y-%m-%d"))
        except Exception:
            pass

    if not dated:
        ax.text(0.5, 0.5, "No timestamps", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    from collections import Counter
    daily = Counter(dated)
    sorted_days = sorted(daily.keys())
    cumulative = []
    running = 0
    for d in sorted_days:
        running += daily[d]
        cumulative.append(running)

    ax.plot(range(len(sorted_days)), cumulative, color=PURPLE, linewidth=2.5,
            marker="o", markersize=5, markerfacecolor=CYAN, markeredgecolor=DARK_BG)
    ax.fill_between(range(len(sorted_days)), cumulative, alpha=0.15, color=PURPLE)

    # Show only a few labels
    step = max(1, len(sorted_days) // 6)
    ax.set_xticks(range(0, len(sorted_days), step))
    ax.set_xticklabels([sorted_days[i][5:] for i in range(0, len(sorted_days), step)],
                       rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Cumulative Proofs", labelpad=10)
    ax.set_title("Total Proofs Over Time", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def chart_verified_vs_suspicious() -> plt.Figure:
    """Grouped bar chart: verified vs suspicious per month."""
    trends = get_time_trends()
    _setup_dark_style()

    fig, ax = plt.subplots(figsize=(6, 4), facecolor=DARK_BG)

    if not trends:
        ax.text(0.5, 0.5, "No data yet", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        ax.set_title("Verified vs Suspicious", color=TEXT_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    months = list(trends.keys())
    x = np.arange(len(months))
    w = 0.35
    v_vals = [trends[m]["VERIFIED"] for m in months]
    s_vals = [trends[m]["SUSPICIOUS"] for m in months]

    ax.bar(x - w/2, v_vals, w, color=GREEN, edgecolor=DARK_BG, label="Verified")
    ax.bar(x + w/2, s_vals, w, color=RED, edgecolor=DARK_BG, label="Suspicious")

    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Count", labelpad=10)
    ax.set_title("Verified vs Suspicious", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.legend(fontsize=9, frameon=False, labelcolor=TEXT_COLOR)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def chart_daily_submissions() -> plt.Figure:
    """Bar chart: submissions per day."""
    from utils.helpers import load_records
    from datetime import datetime
    from collections import Counter

    _setup_dark_style()
    records = load_records()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor=DARK_BG)

    if not records:
        ax.text(0.5, 0.5, "No data yet", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        ax.set_title("Daily Submissions", color=TEXT_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    dates = []
    for r in records:
        try:
            dt = datetime.fromisoformat(r.get("timestamp", "2024-01-01"))
            dates.append(dt.strftime("%Y-%m-%d"))
        except Exception:
            pass

    if not dates:
        ax.text(0.5, 0.5, "No timestamps", transform=ax.transAxes,
                ha="center", va="center", color=MUTED_COLOR, fontsize=13)
        fig.tight_layout()
        return fig

    daily = Counter(dates)
    sorted_days = sorted(daily.keys())
    vals = [daily[d] for d in sorted_days]

    # Gradient colors
    bar_colors = [CYAN if v <= 2 else BLUE if v <= 5 else PURPLE for v in vals]
    ax.bar(range(len(sorted_days)), vals, color=bar_colors, edgecolor=DARK_BG, linewidth=1)

    step = max(1, len(sorted_days) // 6)
    ax.set_xticks(range(0, len(sorted_days), step))
    ax.set_xticklabels([sorted_days[i][5:] for i in range(0, len(sorted_days), step)],
                       rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Submissions", labelpad=10)
    ax.set_title("Daily Submission Count", color=TEXT_COLOR, fontsize=13, pad=15)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig

