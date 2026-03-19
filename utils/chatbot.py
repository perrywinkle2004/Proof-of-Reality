"""
TruthBot — Global AI chatbot for Proof-of-Reality
Renders as a floating-style expandable chat at the bottom of every page (except landing).
"""

import streamlit as st


def _truthbot_respond(user_msg: str, stats: dict, avg_score: float, chain_stats: dict) -> str:
    """Generate a contextual response based on system data."""
    msg = user_msg.lower().strip()

    if any(w in msg for w in ["hello", "hi", "hey", "greet"]):
        return (
            "👋 Hello! I'm **TruthBot** — your AI verification assistant.\n\n"
            "Ask me about:\n"
            "- Proof authenticity scores\n"
            "- How verification works\n"
            "- System statistics\n"
            "- Blockchain storage\n"
            "- Tampering detection"
        )

    if any(w in msg for w in ["stats", "statistics", "numbers", "how many", "total"]):
        return (
            f"📊 **System Statistics:**\n\n"
            f"- **Total Proofs:** {stats['total']}\n"
            f"- **Verified:** {stats['verified']} ({stats['success_rate']}%)\n"
            f"- **Suspicious:** {stats['suspicious']} ({stats['fraud_rate']}%)\n"
            f"- **Needs Review:** {stats['needs_review']}\n"
            f"- **Avg Score:** {avg_score}/100\n"
            f"- **On-chain Blocks:** {chain_stats.get('total_blocks', 0)}"
        )

    if any(w in msg for w in ["score", "authenticity", "scoring", "how score"]):
        return (
            "🎯 **Authenticity Score:**\n\n"
            "1. **Pixel Forensics** — noise, edge, color\n"
            "2. **EXIF Metadata** — camera, software\n"
            "3. **Compression** — re-save artifacts\n"
            "4. **Filename** — suspicious keywords\n"
            "5. **Duplicate Check** — SHA-256\n\n"
            "**75-100** → ✅ VERIFIED\n"
            "**45-74** → ⚠️ NEEDS REVIEW\n"
            "**0-44** → ❌ SUSPICIOUS"
        )

    if any(w in msg for w in ["blockchain", "chain", "block", "on-chain", "immutable"]):
        valid = chain_stats.get("chain_valid", True)
        return (
            f"⛓️ **Blockchain Info:**\n\n"
            f"- SHA-256 hash stored on **immutable ledger**\n"
            f"- Total blocks: **{chain_stats.get('total_blocks', 0)}**\n"
            f"- Status: **{'INTACT ✅' if valid else 'ERROR ❌'}**\n\n"
            f"_\"If it's not on-chain, it isn't verified.\"_"
        )

    if any(w in msg for w in ["tamper", "fake", "detect", "fraud", "suspicious"]):
        return (
            "🔍 **Tampering Detection:**\n\n"
            "- Noise Inconsistency\n"
            "- Edge Anomaly\n"
            "- Color Anomaly\n"
            "- Compression Artifacts\n"
            "- Resolution Issues\n\n"
            "Keywords like `fake`, `edited`, `modified` → auto-penalized."
        )

    if any(w in msg for w in ["verify", "verification", "check", "how to verify"]):
        return (
            "🔍 **Verification Process:**\n\n"
            "1. **Submit Proof** → upload file\n"
            "2. AI runs 6-stage analysis\n"
            "3. SHA-256 hash → stored on-chain\n"
            "4. Get **Proof ID** + **hash**\n"
            "5. **Verify** → paste ID or hash\n"
            "6. System retrieves from blockchain"
        )

    if any(w in msg for w in ["trust", "trust score", "reputation"]):
        return (
            "⭐ **Trust Score:**\n\n"
            "- VERIFIED proofs → increase score\n"
            "- SUSPICIOUS proofs → decrease score\n"
            "- Range: 0-100\n"
            "- Used for reputation weighting"
        )

    if any(w in msg for w in ["help", "what can you do", "command", "options"]):
        return (
            "🤖 **TruthBot can help with:**\n\n"
            "- `stats` — System statistics\n"
            "- `score` — How scoring works\n"
            "- `blockchain` — On-chain storage\n"
            "- `tamper` — Fraud detection\n"
            "- `verify` — Verification process\n"
            "- `trust` — Trust scores\n\n"
            "Just type naturally! 💬"
        )

    return (
        "🤔 Try asking about:\n\n"
        "- **stats** · **score** · **blockchain**\n"
        "- **tamper** · **verify** · **help**"
    )


def render_floating_chatbot():
    """Render the TruthBot natively in the bottom corner using st.popover and CSS.
    Called from app.py ONLY on non-landing logged-in pages."""

    # ── FLOATING BUBBLE CSS (transforms st.popover into floating widget) ──
    st.markdown("""
    <style>
    /* Pin the popover container to bottom right */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 99999 !important;
    }
    /* Style the popover trigger button as a round floating action button */
    div[data-testid="stPopover"] > button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 50%, #06b6d4 100%) !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 4px 20px rgba(124,58,237,0.5) !important;
        color: white !important;
        padding: 0 !important;
        margin: 0 !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.08) !important;
        box-shadow: 0 6px 28px rgba(6,182,212,0.6) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    /* Increase emoji size inside the button */
    div[data-testid="stPopover"] > button p {
        font-size: 1.8rem !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "truthbot_history" not in st.session_state:
        st.session_state["truthbot_history"] = [
            {"role": "bot", "msg": (
                "👋 Hey! I'm **TruthBot**.\n\n"
                "Ask me about scores, blockchain, tampering, or type `help`!"
            )}
        ]

    # Load live data
    from analytics.tracker import (
        get_verification_stats,
        get_average_authenticity_score,
        get_blockchain_stats,
    )
    stats       = get_verification_stats()
    avg_score   = get_average_authenticity_score()
    chain_stats = get_blockchain_stats()

    # The actual native popover
    with st.popover("🤖", help="Open TruthBot AI Assistant"):
        st.markdown("""
        <div style="font-family:'Orbitron',monospace;font-size:1.1rem;font-weight:700;
                    background:linear-gradient(90deg,#7c3aed,#06b6d4);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;text-align:center;margin-bottom:0.2rem">
            TruthBot
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#6b7280;
                    letter-spacing:1px;text-transform:uppercase;text-align:center;
                    margin-bottom:1rem;border-bottom:1px solid rgba(124,58,237,0.2);padding-bottom:0.5rem">
            AI Verification Assistant
        </div>
        """, unsafe_allow_html=True)

        # We wrap chat in a fixed-height container so it is scrollable
        chat_container = st.container(height=350, border=False)
        with chat_container:
            for entry in st.session_state["truthbot_history"]:
                if entry["role"] == "user":
                    st.markdown(f"""<div style="
                        background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.35);
                        border-radius:12px 12px 2px 12px;padding:0.6rem 0.8rem;margin:0.3rem 0 0.3rem 15%;
                        font-size:0.85rem;color:#f0eaff;
                    "><span style="font-size:0.6rem;color:#6b7280;font-family:'JetBrains Mono',monospace">YOU</span><br>{entry['msg']}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style="
                        background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.2);
                        border-radius:12px 12px 12px 2px;padding:0.6rem 0.8rem;margin:0.3rem 15% 0.3rem 0;
                        font-size:0.85rem;color:#d1d5db;
                    "><span style="font-size:0.6rem;color:#6b7280;font-family:'JetBrains Mono',monospace">🤖 TRUTHBOT</span><br>{entry['msg']}</div>""", unsafe_allow_html=True)

        # Input row
        user_input = st.text_input(
            "Ask TruthBot...",
            placeholder="Type your message...",
            key="truthbot_chat_input",
            label_visibility="collapsed",
        )

        col_send, col_clear = st.columns([2, 1])
        with col_send:
            send_btn = st.button("📨 Send", use_container_width=True, key="truthbot_send_btn")
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True, key="truthbot_clear_btn"):
                st.session_state["truthbot_history"] = [
                    {"role": "bot", "msg": "💬 Chat cleared! Ask me anything."}
                ]
                st.rerun()

        if send_btn and user_input:
            st.session_state["truthbot_history"].append({"role": "user", "msg": user_input})
            response = _truthbot_respond(user_input, stats, avg_score, chain_stats)
            st.session_state["truthbot_history"].append({"role": "bot", "msg": response})
            st.rerun()
