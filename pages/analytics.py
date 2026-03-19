"""
Intelligence Layer — Proof-of-Reality Analytics
AI Insights · System Analysis · Input Predictor
NO charts here — charts live in Dashboard only.
Chatbot moved to global sidebar (utils/chatbot.py).
"""

import streamlit as st
from collections import Counter
from utils.helpers import load_records
from analytics.tracker import (
    get_verification_stats,
    get_average_authenticity_score,
    get_per_user_stats,
    get_blockchain_stats,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT RISK ANALYZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _analyze_input_risk(text: str) -> tuple:
    """Predict risk level from text/filename input."""
    text_lower = text.lower().strip()

    suspicious_keywords = ["fake", "edited", "copy", "modified", "tampered",
                           "deepfake", "photoshop", "altered", "generated"]
    safe_keywords = ["original", "real", "clean", "raw", "unedited",
                     "authentic", "camera", "capture"]

    found_suspicious = [k for k in suspicious_keywords if k in text_lower]
    found_safe = [k for k in safe_keywords if k in text_lower]

    risk_score = 50
    risk_score += len(found_suspicious) * 18
    risk_score -= len(found_safe) * 15

    if any(text_lower.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".bmp"]):
        risk_score -= 5
    if any(text_lower.endswith(ext) for ext in [".tiff", ".raw"]):
        risk_score -= 10

    risk_score = max(5, min(95, risk_score))

    if risk_score >= 65:
        level = "HIGH RISK"; color = "#ef4444"; icon = "🔴"
    elif risk_score >= 40:
        level = "MEDIUM RISK"; color = "#f59e0b"; icon = "🟡"
    else:
        level = "LOW RISK"; color = "#10b981"; icon = "🟢"

    reasons = []
    if found_suspicious:
        reasons.append(f"Suspicious keywords detected: **{', '.join(found_suspicious)}**")
    if found_safe:
        reasons.append(f"Authenticity signals present: **{', '.join(found_safe)}**")
    if not found_suspicious and not found_safe:
        reasons.append("No strong signals detected — neutral assessment")
    if len(text_lower) < 5:
        reasons.append("Input too short for reliable analysis")

    explanation = "\n".join(f"- {r}" for r in reasons)
    return risk_score, level, color, icon, explanation


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN RENDER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_analytics():

    # ── PAGE STYLES ──────────────────────────────────────
    st.markdown("""
    <style>
    @keyframes fadeUp {
        0%  { opacity: 0; transform: translateY(16px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    .intel-header {
        animation: fadeUp 0.5s ease both;
        margin-bottom: 2rem;
    }
    .intel-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeUp 0.5s ease both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .intel-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(124,58,237,0.2);
        border-color: rgba(124,58,237,0.45);
    }
    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .section-divider {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #6b7280;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }
    </style>

    <div class="intel-header">
        <h2 style="font-family:'Orbitron',monospace;font-size:1.8rem;font-weight:800;
            background:linear-gradient(90deg,#7c3aed,#06b6d4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            🧠 Intelligence Center
        </h2>
        <p style="color:#6b7280;font-size:0.9rem;margin-top:0.25rem;">
            AI-powered insights · Pattern analysis · Risk prediction
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    stats       = get_verification_stats()
    avg_score   = get_average_authenticity_score()
    chain_stats = get_blockchain_stats()
    records     = load_records()
    total       = stats["total"]

    # ── EMPTY STATE ──────────────────────────────────────
    if total == 0:
        st.markdown("""
        <div style="
            text-align:center;padding:5rem 2rem;
            animation:fadeUp 0.5s ease both;
        ">
            <div style="font-size:4rem;margin-bottom:1rem;opacity:0.5">📭</div>
            <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;
                        color:#a78bfa;margin-bottom:0.75rem">
                Nothing here to see
            </div>
            <div style="color:#6b7280;font-size:0.95rem;max-width:400px;margin:0 auto">
                Please upload a doc for verification to see intelligence insights here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    col_refresh, _ = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 Refresh Data", use_container_width=True, key="analytics_refresh"):
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: AI INSIGHTS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-divider">🔬 AI INSIGHTS</div>', unsafe_allow_html=True)

    indicator_counts = Counter()
    confidence_values = []

    for r in records:
        score = r.get("authenticity_score", 0)
        status = r.get("status", "")

        if score >= 75:
            confidence_values.append("HIGH")
        elif score >= 45:
            confidence_values.append("MEDIUM")
        else:
            confidence_values.append("LOW")

        fname = r.get("filename", "").lower()
        if any(k in fname for k in ["fake", "edited", "modified", "copy", "tampered"]):
            indicator_counts["Suspicious Filename"] += 1
        elif any(k in fname for k in ["original", "real", "clean", "raw", "unedited", "authentic", "camera"]):
            indicator_counts["Authentic Filename"] += 1
            
        if score < 45:
            indicator_counts["Low Score Detection"] += 1
        elif score >= 75:
            indicator_counts["High Confidence"] += 1
            
        if status == "SUSPICIOUS":
            indicator_counts["AI Flagged"] += 1
        elif status == "NEEDS_REVIEW":
            indicator_counts["Needs Review"] += 1
        elif status == "VERIFIED":
            indicator_counts["Verified"] += 1

    col_i1, col_i2, col_i3 = st.columns(3)

    with col_i1:
        top_indicators = indicator_counts.most_common(4) if indicator_counts else [("No data", 0)]
        indicators_html = ""
        for name, count in top_indicators:
            indicators_html += f"""
<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.85rem">
    <span style="color:#f0eaff">{name}</span>
    <span style="font-family:'Orbitron',monospace;color:#a78bfa;font-weight:700">{count}</span>
</div>"""
        st.markdown(f"""
        <div class="intel-card">
            <div class="section-title" style="color:#7c3aed">🔍 Top Indicators</div>
            {indicators_html}
        </div>
        """, unsafe_allow_html=True)

    with col_i2:
        conf_counts = Counter(confidence_values) if confidence_values else {"No data": 0}
        total_proofs = len(confidence_values) if confidence_values else 1
        high_pct = round(conf_counts.get("HIGH", 0) / total_proofs * 100, 1)
        med_pct  = round(conf_counts.get("MEDIUM", 0) / total_proofs * 100, 1)
        low_pct  = round(conf_counts.get("LOW", 0) / total_proofs * 100, 1)

        st.markdown(f"""
        <div class="intel-card">
            <div class="section-title" style="color:#3b82f6">📊 Confidence Levels</div>
            <div style="display:grid;gap:0.6rem;margin-top:0.5rem">
                <div style="display:flex;justify-content:space-between;font-size:0.85rem">
                    <span style="color:#10b981">✅ HIGH</span>
                    <span style="font-family:'Orbitron',monospace;color:#10b981;font-weight:700">{high_pct}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.85rem">
                    <span style="color:#f59e0b">⚠️ MEDIUM</span>
                    <span style="font-family:'Orbitron',monospace;color:#f59e0b;font-weight:700">{med_pct}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.85rem">
                    <span style="color:#ef4444">❌ LOW</span>
                    <span style="font-family:'Orbitron',monospace;color:#ef4444;font-weight:700">{low_pct}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_i3:
        susp_files = [r.get("filename", "?") for r in records if r.get("status") == "SUSPICIOUS"]
        recent_susp = susp_files[-3:] if susp_files else ["None detected"]
        susp_html = "".join(
            f'<div style="padding:0.3rem 0;font-size:0.82rem;color:#ef4444;'
            f'border-bottom:1px solid rgba(239,68,68,0.15)">🚨 {f[:30]}</div>'
            for f in recent_susp
        )

        st.markdown(f"""
        <div class="intel-card">
            <div class="section-title" style="color:#ef4444">⚠️ Suspicious Patterns</div>
            {susp_html}
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: OVERALL ANALYSIS (Dynamic Text)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-divider">📝 OVERALL ANALYSIS</div>', unsafe_allow_html=True)

    v_rate = stats["success_rate"]
    f_rate = stats["fraud_rate"]

    if v_rate >= 80:
        opener = f"The system shows strong verification performance with **{v_rate}%** of proofs passing AI validation."
    elif v_rate >= 50:
        opener = f"Verification rates are moderate at **{v_rate}%**, indicating a mix of authentic and questionable submissions."
    else:
        opener = f"Verification rates are concerning at only **{v_rate}%** — a significant portion shows signs of tampering."

    if f_rate >= 30:
        fraud_line = f"Fraud detection is active: **{f_rate}%** flagged as suspicious. Enhanced scrutiny is recommended."
    elif f_rate >= 10:
        fraud_line = f"The fraud rate of **{f_rate}%** is within expected range. Continuous monitoring is in place."
    else:
        fraud_line = f"The fraud rate is low at **{f_rate}%**, suggesting high-quality submissions."

    if avg_score >= 75:
        score_line = f"Average authenticity score of **{avg_score}/100** indicates high system confidence."
    elif avg_score >= 50:
        score_line = f"Average score at **{avg_score}/100** — acceptable but trending toward review territory."
    else:
        score_line = f"Average score of **{avg_score}/100** is below threshold. Most submissions require review."

    chain_valid = chain_stats.get("chain_valid", True)
    chain_line = (
        f"Blockchain integrity is **verified** across **{chain_stats.get('total_blocks', 0)}** blocks."
        if chain_valid else
        "⚠️ **Blockchain integrity issue detected.**"
    )

    summary = f"{opener}\n\n{fraud_line}\n\n{score_line}\n\n{chain_line}"

    st.markdown(f"""
    <div class="intel-card" style="border-color:rgba(59,130,246,0.3)">
        <div class="section-title" style="color:#3b82f6">🧠 AI System Analysis</div>
        <div style="color:#d1d5db;font-size:0.9rem;line-height:1.7">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: AI INPUT ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-divider">🔮 AI INPUT ANALYSIS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="intel-card" style="border-color:rgba(124,58,237,0.35)">
        <div class="section-title" style="color:#a78bfa">🧪 Predictive Risk Analyzer</div>
        <div style="color:#6b7280;font-size:0.82rem;margin-bottom:0.5rem">
            Enter a file name or text description to predict authenticity risk before submission.
        </div>
    </div>
    """, unsafe_allow_html=True)

    input_text = st.text_input(
        "Enter filename or description",
        placeholder="e.g. edited_photo_v2.jpg or 'original camera capture from site visit'",
        label_visibility="collapsed",
        key="ai_input_analysis"
    )

    if input_text:
        risk_score, level, color, icon, explanation = _analyze_input_risk(input_text)

        st.markdown(f"""
        <div style="
            background:{color}10;border:1px solid {color}50;
            border-radius:14px;padding:1.3rem;margin-top:0.5rem;margin-bottom:1rem;
            animation:fadeUp 0.4s ease both
        ">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem">
                <span style="font-size:1.8rem">{icon}</span>
                <div>
                    <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:900;color:{color}">
                        {risk_score}/100
                    </div>
                    <div style="font-size:0.75rem;font-family:'JetBrains Mono',monospace;color:{color};
                                letter-spacing:1.5px">{level}</div>
                </div>
            </div>
            <div style="color:#d1d5db;font-size:0.85rem;line-height:1.6">
                {explanation.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
