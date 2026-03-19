"""
Power BI-Style Dashboard for Proof-of-Reality
6 real-data charts + 4 KPI cards — visual analytics ONLY.
"""

import streamlit as st
from utils.helpers import get_user_by_id, get_user_records, load_records
from analytics.tracker import (
    get_verification_stats,
    get_average_authenticity_score,
    get_blockchain_stats,
)
from analytics.charts import (
    chart_verification_donut,
    chart_authenticity_bar,
    chart_trust_score_hist,
    chart_time_trends,
    chart_proofs_over_time,
    chart_verified_vs_suspicious,
    chart_daily_submissions,
)


def render_dashboard():

    user_id = st.session_state.get("user_id", "demo_user")
    user    = get_user_by_id(user_id)

    # ── DASHBOARD ANIMATIONS (preserved from original) ──────────────────────
    st.markdown("""
    <style>
    @keyframes dashReveal {
        0%  { opacity: 0; transform: translateY(20px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    @keyframes kpiCount {
        0%  { opacity: 0; transform: translateY(8px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    @keyframes borderGlow {
        0%,100% { box-shadow: 0 4px 20px rgba(124,58,237,0.15); }
        50%      { box-shadow: 0 4px 32px rgba(124,58,237,0.4);  }
    }
    .dash-header {
        animation: dashReveal 0.5s ease both;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 16px;
        padding: 1.4rem 1rem;
        text-align: center;
        animation: kpiCount 0.5s ease both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 40px rgba(124,58,237,0.28);
        border-color: rgba(124,58,237,0.5);
    }
    .kpi-value {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #6b7280;
        letter-spacing: 1.5px;
        margin-top: 0.3rem;
        text-transform: uppercase;
    }
    .kpi-sub {
        font-size: 0.85rem;
        color: #a78bfa;
        margin-top: 0.2rem;
    }
    .chart-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(124,58,237,0.2);
        border-radius: 16px;
        padding: 1rem;
        animation: dashReveal 0.5s ease 0.15s both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .chart-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(124,58,237,0.2);
        border-color: rgba(124,58,237,0.45);
    }
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #6b7280;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
    }
    </style>

    <div class="dash-header">
        <h2 style="font-family:'Orbitron',monospace;font-size:1.8rem;font-weight:800;
            background:linear-gradient(90deg,#7c3aed,#3b82f6,#06b6d4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            📊 Analytics Dashboard
        </h2>
        <p style="color:#6b7280;font-size:0.9rem;margin-top:0.25rem;">
            Real-time verification metrics · Live blockchain data · Power BI View
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── LOAD REAL DATA ───────────────────────────────────────────────────────
    stats       = get_verification_stats()
    avg_score   = get_average_authenticity_score()
    chain_stats = get_blockchain_stats()
    user_records = get_user_records(user_id)

    total      = stats["total"]
    verified   = stats["verified"]
    suspicious = stats["suspicious"]
    verif_pct  = stats["success_rate"]
    susp_pct   = stats["fraud_rate"]

    # ── EMPTY STATE ──────────────────────────────────────────────────────────
    if total == 0:
        st.markdown("""
        <div style="
            text-align:center;padding:5rem 2rem;
            animation:dashReveal 0.5s ease both;
        ">
            <div style="font-size:4rem;margin-bottom:1rem;opacity:0.5">📭</div>
            <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;
                        color:#a78bfa;margin-bottom:0.75rem">
                Nothing here to see
            </div>
            <div style="color:#6b7280;font-size:0.95rem;max-width:400px;margin:0 auto">
                Please upload a doc for verification to see analytics here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── 4 KPI CARDS ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    kpi_data = [
        (k1, str(total),       "TOTAL PROOFS",    f"{chain_stats.get('total_proofs', 0)} on-chain"),
        (k2, f"{verif_pct}%",  "VERIFIED",        f"{verified} of {total}"),
        (k3, f"{susp_pct}%",   "SUSPICIOUS",      f"{suspicious} flagged"),
        (k4, f"{avg_score}",   "AVG AUTH SCORE",  "out of 100"),
    ]

    for col, val, label, sub in kpi_data:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 1: Total Proofs Over Time (Line) + Verification Status (Pie)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">VERIFICATION OVERVIEW</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_proofs_over_time()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_verification_donut()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 2: Score Distribution (Histogram) + Trust Score Trend (Histogram)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">SCORE DISTRIBUTIONS</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_authenticity_bar()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_trust_score_hist()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ROW 3: Verified vs Suspicious (Bar) + Daily Submission Count (Bar)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-label">COMPARISON & ACTIVITY</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)

    with c5:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_verified_vs_suspicious()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            fig = chart_daily_submissions()
            st.pyplot(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Chart unavailable: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
