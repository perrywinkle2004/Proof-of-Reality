"""
Upload & Verify page for Proof-of-Reality
Main proof submission and AI validation workflow.
"""

import streamlit as st
import time
from datetime import datetime
from utils.helpers import (
    get_user_records, add_record, generate_proof_id,
    load_records, simulated_gps, now_iso
)
from modules.ai_validator import run_full_validation
from modules.llm_reasoning import generate_explanation
from modules.hash_generator import generate_proof_hash, format_hash_display
from modules.blockchain import add_to_blockchain
from modules.trust_score import update_trust_score
from utils.theme import score_color, status_color


def render_upload_verify():
    user_id = st.session_state.get("user_id", "demo_user")

    # 🔥 AI GLOW ANIMATION + UPLOAD PAGE POLISH
    st.markdown("""
    <style>
    @keyframes aiGlow {
        0%  { box-shadow: 0 0 10px rgba(124,58,237,0.3), 0 0 20px rgba(59,130,246,0.1); }
        33% { box-shadow: 0 0 25px rgba(124,58,237,0.7), 0 0 50px rgba(59,130,246,0.3); }
        66% { box-shadow: 0 0 18px rgba(6,182,212,0.5),  0 0 35px rgba(124,58,237,0.4); }
        100%{ box-shadow: 0 0 10px rgba(124,58,237,0.3), 0 0 20px rgba(59,130,246,0.1); }
    }
    @keyframes gradWave {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes pageSlideUp {
        0%  { opacity: 0; transform: translateY(16px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    @keyframes stepPulse {
        0%,100% { opacity: 0.4; transform: scale(1); }
        50%      { opacity: 1;   transform: scale(1.05); }
    }
    @keyframes shimmerSlide {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }
    .ai-glow {
        animation: aiGlow 3s ease-in-out infinite;
        border-radius: 16px;
    }
    .upload-header {
        animation: pageSlideUp 0.5s ease both;
    }
    .pipeline-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 14px;
        padding: 1.2rem;
        animation: pageSlideUp 0.5s ease 0.15s both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        line-height: 2.2;
    }
    .pipeline-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.2);
    }
    .ai-step-card {
        background: rgba(124,58,237,0.08);
        border: 1px solid rgba(124,58,237,0.25);
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        margin-bottom: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #a78bfa;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .ai-step-card.active {
        border-color: rgba(124,58,237,0.7);
        background: rgba(124,58,237,0.15);
        color: #f0eaff;
        animation: stepPulse 1s ease-in-out infinite;
    }
    .ai-step-card.done {
        border-color: rgba(16,185,129,0.4);
        background: rgba(16,185,129,0.07);
        color: #10b981;
    }
    .shimmer-bar {
        height: 4px;
        border-radius: 4px;
        background: linear-gradient(90deg,
            rgba(124,58,237,0.15) 0%,
            rgba(124,58,237,0.7) 40%,
            rgba(59,130,246,0.8) 60%,
            rgba(124,58,237,0.15) 100%);
        background-size: 400px 100%;
        animation: shimmerSlide 1.2s linear infinite;
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="upload-header" style="margin-bottom: 2rem;">
    <h2 style="font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 800; color: #f0eaff;">
    📤 Submit Proof</h2>
    <p style="color: #6b7280;">Upload evidence for AI validation and blockchain storage</p>
    <p style="color: #a78bfa; font-style: italic; font-size: 0.85rem; margin-top: 0.3rem;">
        "If it's not on-chain, it isn't verified."
    </p>
</div>
""", unsafe_allow_html=True)

    col_upload, col_info = st.columns([2, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Drop your proof here",
            type=["jpg", "jpeg", "png", "pdf", "bmp", "tiff"],
            label_visibility="collapsed",
        )

        if uploaded_file:
            if uploaded_file.type.startswith("image/"):
                st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
            else:
                st.write(uploaded_file.name)

    with col_info:
        st.markdown("### ⚙️ Pipeline")
        st.markdown("""
        🔍 AI  
        📋 Metadata  
        🔁 Duplicate  
        🔐 Hash  
        ⛓️ Blockchain  
        ⭐ Trust  
        """)

    col1, col2 = st.columns(2)

    with col1:
        verify_btn = st.button("🔬 Validate & Store", use_container_width=True)

    with col2:
        demo_btn = st.button("🧪 Demo Run", use_container_width=True)

    if verify_btn and uploaded_file:
        file_bytes = uploaded_file.getvalue()
        _run_validation_pipeline(file_bytes, uploaded_file.name, user_id)

    elif demo_btn:
        _run_validation_pipeline(b"demo_fake", "fake_proof.jpg", user_id)

    elif verify_btn:
        st.warning("Upload a file first")


def _run_validation_pipeline(file_bytes, filename, user_id):

    # ── ANIMATED AI THINKING STATE ──────────────────────
    st.markdown('<div class="shimmer-bar"></div>', unsafe_allow_html=True)

    steps = [
        ("🤖", "AI Forensic Analysis", "Scanning pixel patterns, edge anomalies, noise distribution..."),
        ("📋", "Metadata Consistency Check", "Validating timestamps, filename integrity, EXIF data..."),
        ("🔁", "Duplicate Detection", "Cross-referencing SHA-256 hash against all stored proofs..."),
        ("🔐", "SHA-256 Hashing", "Generating cryptographic proof hash..."),
        ("⛓️", "Blockchain Entry", "Writing immutable block to the verification ledger..."),
        ("⭐", "Trust Score Update", "Recalculating user trust coefficient..."),
    ]

    step_container = st.empty()

    def render_steps(done_up_to: int):
        html = ""
        for i, (icon, title, desc) in enumerate(steps):
            if i < done_up_to:
                css_class = "ai-step-card done"
                status_icon = "✅"
            elif i == done_up_to:
                css_class = "ai-step-card active"
                status_icon = "⟳"
            else:
                css_class = "ai-step-card"
                status_icon = "○"
            html += (
                f'<div class="{css_class}">'
                f'<span style="font-size:1.2rem">{icon}</span>'
                f'<div><strong>{status_icon} {title}</strong>'
                f'<div style="font-size:0.75rem;opacity:0.7;margin-top:2px">{desc}</div>'
                f'</div></div>'
            )
        step_container.markdown(html, unsafe_allow_html=True)

    # ── RUN PIPELINE WITH ANIMATED STEP REVEALS ─────────
    render_steps(0); time.sleep(0.6)
    timestamp = now_iso()
    gps = simulated_gps()
    existing_records = load_records()
    validation = run_full_validation(file_bytes, filename, timestamp, existing_records)

    render_steps(1); time.sleep(0.5)
    explanation = generate_explanation(validation)

    render_steps(2); time.sleep(0.4)

    render_steps(3); time.sleep(0.4)
    proof_hash = generate_proof_hash(file_bytes, user_id, timestamp)
    proof_id = generate_proof_id()

    render_steps(4); time.sleep(0.5)
    block_data = add_to_blockchain(proof_id, proof_hash, user_id)

    render_steps(5); time.sleep(0.4)
    update_trust_score(
        user_id,
        validation["authenticity_score"],
        validation["status"]
    )

    # ✅ CRITICAL FIX: store status, user_id, timestamp so analytics work
    add_record({
        "proof_id":           proof_id,
        "filename":           filename,
        "authenticity_score": validation["authenticity_score"],
        "status":             validation["status"],
        "user_id":            user_id,
        "timestamp":          timestamp,
        "hash":               proof_hash,
        "file_hash":          proof_hash,   # 🔥 REQUIRED FOR VERIFICATION
        "gps":                gps,
    })

    render_steps(6)  # all done
    time.sleep(0.3)
    step_container.empty()

    # ── OUTPUT ──────────────────────────────────────────
    score   = validation["authenticity_score"]
    vstatus = validation["status"]

    if vstatus == "VERIFIED":
        s_color = "#10b981"; s_icon = "✅"
    elif vstatus == "NEEDS_REVIEW":
        s_color = "#f59e0b"; s_icon = "⚠️"
    else:
        s_color = "#ef4444"; s_icon = "❌"

    st.markdown(f"""
    <div style="
        background:{s_color}12;border:1px solid {s_color}55;
        border-radius:16px;padding:1.5rem;
        text-align:center;margin-bottom:1.5rem;
    ">
        <div style="font-size:2.2rem">{s_icon}</div>
        <div style="font-size:1.3rem;font-weight:800;color:{s_color};
                    font-family:'Orbitron',monospace;margin-top:0.4rem">
            {vstatus.replace('_', ' ')}
        </div>
        <div style="font-size:2rem;font-weight:900;color:#f0eaff;margin-top:0.5rem">
            {score}<span style="font-size:1rem;color:#a78bfa"> / 100</span>
        </div>
        <div style="font-size:0.8rem;color:#a78bfa;margin-top:0.4rem;
                    font-family:'JetBrains Mono',monospace;letter-spacing:1px">
            AUTHENTICITY SCORE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cryptographic integrity + on-chain badge
    block_index = block_data.get("index", "?") if block_data else "?"
    st.markdown(f"""
    <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap">
        <div style="
            background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.4);
            border-radius:10px;padding:0.6rem 1rem;font-size:0.8rem;
            font-family:'JetBrains Mono',monospace;color:#a78bfa;
            display:flex;align-items:center;gap:0.5rem
        ">
            🔐 <strong style="color:#f0eaff">Cryptographic Integrity Verified</strong>
            &nbsp;·&nbsp; SHA-256
        </div>
        <div style="
            background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.4);
            border-radius:10px;padding:0.6rem 1rem;font-size:0.8rem;
            font-family:'JetBrains Mono',monospace;color:#06b6d4;
            display:flex;align-items:center;gap:0.5rem
        ">
            ⛓️ <strong style="color:#f0eaff">Stored On-Chain</strong>
            &nbsp;·&nbsp; Block #{block_index}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🆔 Proof ID")
        st.code(proof_id)
    with col2:
        st.markdown("### 📍 GPS Location")
        st.code(gps)

    st.markdown("### 🔗 Blockchain Hash (Copy to verify)")
    st.code(proof_hash)

    st.markdown("#### Display Format")
    st.code(format_hash_display(proof_hash))

    st.markdown("### 🧠 AI Core Analysis Summary")
    with st.expander("View Full AI Analysis", expanded=True):
        st.markdown(explanation)
