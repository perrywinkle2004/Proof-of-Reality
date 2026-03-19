"""
Verification Portal — Proof-of-Reality
Search by Proof ID or Blockchain Hash
"""

import streamlit as st
from utils.helpers import load_records, truncate_hash
from modules.blockchain import verify_hash_on_chain


def render_verification():

    st.markdown("""
    <style>
    @keyframes verifyReveal {
        0%  { opacity: 0; transform: translateY(18px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    @keyframes bannerPop {
        0%  { opacity: 0; transform: scale(0.95); }
        100%{ opacity: 1; transform: scale(1); }
    }
    .verify-header {
        animation: verifyReveal 0.5s ease both;
        margin-bottom: 2rem;
    }
    .result-banner {
        animation: bannerPop 0.4s ease both;
        transition: transform 0.3s ease;
    }
    .result-banner:hover {
        transform: scale(1.01);
    }
    .not-found-card {
        animation: bannerPop 0.4s ease both;
    }
    </style>
    <div class="verify-header">
        <h2 style="font-family:'Orbitron',monospace;
            background:linear-gradient(90deg,#7c3aed,#3b82f6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        🔍 Verification Portal</h2>
        <p style="color:#6b7280;">
        Search any proof using Proof ID or SHA-256 hash
        </p>
        <p style="color:#a78bfa;font-style:italic;font-size:0.85rem;margin-top:0.3rem;">
        "If it's not on-chain, it isn't verified."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── INPUT ─────────────────────────────────────
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input(
            "Enter Proof ID or Hash",
            placeholder="POR-001 or full hash...",
            label_visibility="collapsed"
        )

    with col2:
        search_btn = st.button("🔍 Verify", use_container_width=True)

    # ── QUICK BUTTONS ─────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    records = load_records()
    quick_ids = [r["proof_id"] for r in records[-5:]]

    if quick_ids:
        cols = st.columns(len(quick_ids))
        for i, pid in enumerate(quick_ids):
            with cols[i]:
                if st.button(pid, key=f"quick_{pid}"):
                    st.session_state["verify_query"] = pid
                    st.rerun()

    # ── HANDLE SEARCH ─────────────────────────────
    query = st.session_state.pop("verify_query", query)

    if search_btn or query:
        if not query:
            st.warning("Enter a Proof ID or hash")
            return

        record = _find_record(query, records)

        if record:
            _show_result(record)
        else:
            _show_not_found()


# ────────────────────────────────────────────────
# 🔍 SEARCH LOGIC
# ────────────────────────────────────────────────
def _find_record(query, records):
    query = query.strip()

    for r in records:
        if query == r.get("proof_id"):
            return r
        if query == r.get("hash") or query == r.get("file_hash"):
            return r

    return None


# ────────────────────────────────────────────────
# ✅ RESULT UI (FIXED — NO HTML BUG)
# ────────────────────────────────────────────────
def _show_result(record):

    score = record.get("authenticity_score", 0)

    # Status mapping
    if score >= 75:
        status = "VERIFIED"
        color = "#10b981"
        icon = "✅"
    elif score >= 50:
        status = "PENDING REVIEW"
        color = "#f59e0b"
        icon = "⚠️"
    else:
        status = "SUSPICIOUS"
        color = "#ef4444"
        icon = "❌"

    # Banner (original preserved)
    st.markdown(f"""
    <div class="result-banner" style="
        background: {color}15;
        border: 1px solid {color}55;
        border-radius: 16px;
        padding: 1.5rem;
        text-align:center;
        margin-top:1rem;
    ">
        <div style="font-size:2rem;">{icon}</div>
        <div style="color:{color};font-weight:700;">
            PROOF FOUND — {status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ── BLOCKCHAIN LOOKUP ────────────────────────────────
    proof_hash = record.get("hash", "")
    block = verify_hash_on_chain(proof_hash) if proof_hash else None

    if block:
        block_ts = block.get("timestamp", "")[:16].replace("T", " · ")
        block_idx = block.get("index", "?")
        block_hash_short = block.get("block_hash", "")[:20] + "..."
        st.markdown(f"""
        <div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin-bottom:1rem">
            <div style="
                background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.45);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#06b6d4;
                display:flex;align-items:center;gap:0.5rem
            ">
                ⛓️ <strong style="color:#f0eaff">Verified on Blockchain</strong>
                &nbsp;·&nbsp; Block #{block_idx}
            </div>
            <div style="
                background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.35);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#a78bfa;
                display:flex;align-items:center;gap:0.5rem
            ">
                🕐 Anchored: {block_ts}
            </div>
            <div style="
                background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#10b981;
                display:flex;align-items:center;gap:0.5rem
            ">
                🔐 Cryptographic Integrity Verified
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);
            border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
            font-family:'JetBrains Mono',monospace;color:#f59e0b;
            margin-bottom:1rem;display:inline-flex;align-items:center;gap:0.5rem
        ">
            ⚠️ Hash not found in current blockchain snapshot
        </div>
        """, unsafe_allow_html=True)

    # ── CLEAN UI — original preserved ────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🆔 Proof ID")
        st.code(record.get("proof_id"))

        st.markdown("### 📄 Filename")
        st.code(record.get("filename", "unknown"))

        if record.get("gps"):
            st.markdown("### 📍 GPS")
            st.code(record.get("gps"))

    with col2:
        st.markdown("### 🎯 Authenticity Score")
        st.metric("", f"{score}%")

        st.markdown("### 🔗 Hash")
        st.code(truncate_hash(record.get("hash", "")))

        if record.get("user_id"):
            st.markdown("### 👤 Submitted By")
            st.code(record.get("user_id"))

    # Full hash (original preserved)
    st.markdown("### 🔐 Full Blockchain Hash")
    st.code(record.get("hash", ""))

    if block:
        st.markdown("### ⛓️ Block Hash")
        st.code(block.get("block_hash", ""))



# ────────────────────────────────────────────────
# ❌ NOT FOUND UI
# ────────────────────────────────────────────────
def _show_not_found():

    st.markdown("""
    <div class="not-found-card" style="
        background:#ef444415;
        border:1px solid #ef444455;
        border-radius:16px;
        padding:2rem;
        text-align:center;
        margin-top:1rem;
    ">
        <div style="font-size:2rem;">❌</div>
        <div style="color:#ef4444;font-weight:700;">
            NOT FOUND
        </div>
        <div style="color:#6b7280;margin-top:0.5rem;">
            No proof exists for this ID or hash.
        </div>
    </div>
    """, unsafe_allow_html=True)
"""
Verification Portal — Proof-of-Reality
Search by Proof ID or Blockchain Hash
"""

import streamlit as st
from utils.helpers import load_records, truncate_hash
from modules.blockchain import verify_hash_on_chain


def render_verification():

    st.markdown("""
    <style>
    @keyframes verifyReveal {
        0%  { opacity: 0; transform: translateY(18px); }
        100%{ opacity: 1; transform: translateY(0); }
    }
    @keyframes bannerPop {
        0%  { opacity: 0; transform: scale(0.95); }
        100%{ opacity: 1; transform: scale(1); }
    }
    .verify-header {
        animation: verifyReveal 0.5s ease both;
        margin-bottom: 2rem;
    }
    .result-banner {
        animation: bannerPop 0.4s ease both;
        transition: transform 0.3s ease;
    }
    .result-banner:hover {
        transform: scale(1.01);
    }
    .not-found-card {
        animation: bannerPop 0.4s ease both;
    }
    </style>
    <div class="verify-header">
        <h2 style="font-family:'Orbitron',monospace;
            background:linear-gradient(90deg,#7c3aed,#3b82f6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        🔍 Verification Portal</h2>
        <p style="color:#6b7280;">
        Search any proof using Proof ID or SHA-256 hash
        </p>
        <p style="color:#a78bfa;font-style:italic;font-size:0.85rem;margin-top:0.3rem;">
        "If it's not on-chain, it isn't verified."
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── INPUT ─────────────────────────────────────
    col1, col2 = st.columns([4, 1])

    with col1:
        query = st.text_input(
            "Enter Proof ID or Hash",
            placeholder="POR-001 or full hash...",
            label_visibility="collapsed"
        )

    with col2:
        search_btn = st.button("🔍 Verify", use_container_width=True)

    # ── QUICK BUTTONS ─────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    records = load_records()
    quick_ids = [r["proof_id"] for r in records[-5:]]

    if quick_ids:
        cols = st.columns(len(quick_ids))
        for i, pid in enumerate(quick_ids):
            with cols[i]:
                if st.button(pid, key=f"quick_{pid}"):
                    st.session_state["verify_query"] = pid
                    st.rerun()

    # ── HANDLE SEARCH ─────────────────────────────
    query = st.session_state.pop("verify_query", query)

    if search_btn or query:
        if not query:
            st.warning("Enter a Proof ID or hash")
            return

        record = _find_record(query, records)

        if record:
            _show_result(record)
        else:
            _show_not_found()


# ────────────────────────────────────────────────
# 🔍 SEARCH LOGIC
# ────────────────────────────────────────────────
def _find_record(query, records):
    query = query.strip()

    for r in records:
        if query == r.get("proof_id"):
            return r
        if query == r.get("hash") or query == r.get("file_hash"):
            return r

    return None


# ────────────────────────────────────────────────
# ✅ RESULT UI (FIXED — NO HTML BUG)
# ────────────────────────────────────────────────
def _show_result(record):

    score = record.get("authenticity_score", 0)

    # Status mapping
    if score >= 75:
        status = "VERIFIED"
        color = "#10b981"
        icon = "✅"
    elif score >= 50:
        status = "PENDING REVIEW"
        color = "#f59e0b"
        icon = "⚠️"
    else:
        status = "SUSPICIOUS"
        color = "#ef4444"
        icon = "❌"

    # Banner (original preserved)
    st.markdown(f"""
    <div class="result-banner" style="
        background: {color}15;
        border: 1px solid {color}55;
        border-radius: 16px;
        padding: 1.5rem;
        text-align:center;
        margin-top:1rem;
    ">
        <div style="font-size:2rem;">{icon}</div>
        <div style="color:{color};font-weight:700;">
            PROOF FOUND — {status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ── BLOCKCHAIN LOOKUP ────────────────────────────────
    proof_hash = record.get("hash", "")
    block = verify_hash_on_chain(proof_hash) if proof_hash else None

    if block:
        block_ts = block.get("timestamp", "")[:16].replace("T", " · ")
        block_idx = block.get("index", "?")
        block_hash_short = block.get("block_hash", "")[:20] + "..."
        st.markdown(f"""
        <div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin-bottom:1rem">
            <div style="
                background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.45);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#06b6d4;
                display:flex;align-items:center;gap:0.5rem
            ">
                ⛓️ <strong style="color:#f0eaff">Verified on Blockchain</strong>
                &nbsp;·&nbsp; Block #{block_idx}
            </div>
            <div style="
                background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.35);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#a78bfa;
                display:flex;align-items:center;gap:0.5rem
            ">
                🕐 Anchored: {block_ts}
            </div>
            <div style="
                background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.3);
                border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
                font-family:'JetBrains Mono',monospace;color:#10b981;
                display:flex;align-items:center;gap:0.5rem
            ">
                🔐 Cryptographic Integrity Verified
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);
            border-radius:10px;padding:0.55rem 1rem;font-size:0.8rem;
            font-family:'JetBrains Mono',monospace;color:#f59e0b;
            margin-bottom:1rem;display:inline-flex;align-items:center;gap:0.5rem
        ">
            ⚠️ Hash not found in current blockchain snapshot
        </div>
        """, unsafe_allow_html=True)

    # ── CLEAN UI — original preserved ────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🆔 Proof ID")
        st.code(record.get("proof_id"))

        st.markdown("### 📄 Filename")
        st.code(record.get("filename", "unknown"))

        if record.get("gps"):
            st.markdown("### 📍 GPS")
            st.code(record.get("gps"))

    with col2:
        st.markdown("### 🎯 Authenticity Score")
        st.metric("", f"{score}%")

        st.markdown("### 🔗 Hash")
        st.code(truncate_hash(record.get("hash", "")))

        if record.get("user_id"):
            st.markdown("### 👤 Submitted By")
            st.code(record.get("user_id"))

    # Full hash (original preserved)
    st.markdown("### 🔐 Full Blockchain Hash")
    st.code(record.get("hash", ""))

    if block:
        st.markdown("### ⛓️ Block Hash")
        st.code(block.get("block_hash", ""))



# ────────────────────────────────────────────────
# ❌ NOT FOUND UI
# ────────────────────────────────────────────────
def _show_not_found():

    st.markdown("""
    <div class="not-found-card" style="
        background:#ef444415;
        border:1px solid #ef444455;
        border-radius:16px;
        padding:2rem;
        text-align:center;
        margin-top:1rem;
    ">
        <div style="font-size:2rem;">❌</div>
        <div style="color:#ef4444;font-weight:700;">
            NOT FOUND
        </div>
        <div style="color:#6b7280;margin-top:0.5rem;">
            No proof exists for this ID or hash.
        </div>
    </div>
    """, unsafe_allow_html=True)