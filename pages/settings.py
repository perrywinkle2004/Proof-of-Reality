"""
Settings page for Proof-of-Reality
Theme toggle, reset data, user preferences.
"""

import streamlit as st
import json
import os
from utils.helpers import get_user_by_id, update_user, load_records, save_records, load_users, save_users


def render_settings():
    user_id = st.session_state.get("user_id", "demo_user")
    user = get_user_by_id(user_id)
    if not user:
        st.error("User not found.")
        return

    st.markdown("""<div style="margin-bottom: 2rem;">
    <h2 style="
        font-family: 'Orbitron', monospace; font-size: 1.6rem;
        font-weight: 800; color: #f0eaff;
    ">⚙️ Settings</h2>
    <p style="color: #6b7280; font-size: 0.9rem;">
        Customize your Proof-of-Reality experience
    </p>
</div>
""", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    # ── Appearance ────────────────────────────────────────────────────────────
    with col_left:
        st.markdown("""<div style="
    background:rgba(255,255,255,0.03);border:1px solid rgba(124,58,237,0.25);
    border-radius:20px;padding:1.5rem;margin-bottom:1.25rem;
">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
        color:#6b7280;letter-spacing:2px;margin-bottom:1rem;">🎨 APPEARANCE</div>
""", unsafe_allow_html=True)

        current_theme = st.session_state.get("theme", "dark")
        theme_label = "🌙 Dark Mode" if current_theme == "dark" else "☀️ Light Mode"

        st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
    padding:0.75rem 0;border-bottom:1px solid rgba(255,255,255,0.06);">
    <span style="color:#a78bfa;">Current Theme</span>
    <span style="font-weight:600;color:#f0eaff;">{theme_label}</span>
</div>
""", unsafe_allow_html=True)

        col_dark, col_light = st.columns(2)
        with col_dark:
            if st.button("🌙 Dark Mode", use_container_width=True,
                         type="primary" if current_theme == "dark" else "secondary"):
                st.session_state["theme"] = "dark"
                st.rerun()
        with col_light:
            if st.button("☀️ Light Mode", use_container_width=True,
                         type="primary" if current_theme == "light" else "secondary"):
                st.session_state["theme"] = "light"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Account Info ──────────────────────────────────────────────────────
        st.markdown("""<div style="
    background:rgba(255,255,255,0.03);border:1px solid rgba(124,58,237,0.25);
    border-radius:20px;padding:1.5rem;margin-bottom:1.25rem;
">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
        color:#6b7280;letter-spacing:2px;margin-bottom:1rem;">👤 ACCOUNT INFO</div>
""", unsafe_allow_html=True)

        rows = [
            ("Username", user.get("username", "—")),
            ("Email", user.get("email", "—")),
            ("Trust Score", f"{user.get('trust_score', 50)}/100"),
            ("Verified Proofs", str(user.get("verified_proofs", 0))),
            ("Suspicious Proofs", str(user.get("suspicious_proofs", 0))),
            ("Member Since", user.get("joined", "—")[:10]),
        ]

        for label, val in rows:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:0.5rem 0;
    border-bottom:1px solid rgba(255,255,255,0.04);">
    <span style="color:#6b7280;font-size:0.85rem;">{label}</span>
    <span style="color:#f0eaff;font-weight:600;font-size:0.85rem;
        font-family:'JetBrains Mono',monospace;">{val}</span>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Preferences & Data Management ─────────────────────────────────────────
    with col_right:
        st.markdown("""<div style="
    background:rgba(255,255,255,0.03);border:1px solid rgba(124,58,237,0.25);
    border-radius:20px;padding:1.5rem;margin-bottom:1.25rem;
">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
        color:#6b7280;letter-spacing:2px;margin-bottom:1rem;">🔔 NOTIFICATIONS</div>
""", unsafe_allow_html=True)

        notif_pref = st.session_state.get("notif_pref", True)
        new_notif = st.toggle("Enable notifications", value=notif_pref)
        if new_notif != notif_pref:
            st.session_state["notif_pref"] = new_notif

        email_alerts = st.session_state.get("email_alerts", False)
        new_email = st.toggle("Email alerts for suspicious proofs", value=email_alerts)
        if new_email != email_alerts:
            st.session_state["email_alerts"] = new_email

        auto_bc = st.session_state.get("auto_blockchain", True)
        new_bc = st.toggle("Auto store to blockchain on verify", value=auto_bc)
        if new_bc != auto_bc:
            st.session_state["auto_blockchain"] = new_bc

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Data Management ────────────────────────────────────────────────────
        st.markdown("""<div style="
    background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.2);
    border-radius:20px;padding:1.5rem;
">
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
        color:#ef4444;letter-spacing:2px;margin-bottom:1rem;">⚠️ DANGER ZONE</div>
""", unsafe_allow_html=True)

        st.markdown("""<div style="color:#6b7280;font-size:0.82rem;margin-bottom:1rem;line-height:1.5;">
    These actions are irreversible. Reset operations will clear demo data
    and restore factory defaults for demonstration purposes.
</div>
""", unsafe_allow_html=True)

        if st.button("🔔 Mark All Notifications Read", use_container_width=True):
            notifications = user.get("notifications", [])
            for n in notifications:
                n["read"] = True
            user["notifications"] = notifications
            update_user(user)
            st.success("All notifications marked as read.")
            st.rerun()

        if st.button("🗑️ Clear My Proof History", use_container_width=True):
            records = load_records()
            records = [r for r in records if r.get("user_id") != user_id]
            save_records(records)
            st.success("Your proof history has been cleared.")
            st.rerun()

        if st.button("🔄 Reset My Trust Score to 50", use_container_width=True):
            user["trust_score"] = 50
            update_user(user)
            st.success("Trust score reset to 50.")
            st.rerun()

        # Logout
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["logged_in", "user_id", "username"]:
                st.session_state.pop(key, None)
            st.session_state["current_page"] = "landing"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ── About Section ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="
    background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
    border-radius:16px;padding:1.5rem;text-align:center;
">
    <div style="font-family:'Orbitron',monospace;font-weight:700;font-size:1.1rem;
        background:linear-gradient(90deg,#7c3aed,#3b82f6);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        margin-bottom:0.5rem;">
        Proof-of-Reality v2.0
    </div>
    <div style="color:#6b7280;font-size:0.8rem;line-height:1.6;">
        AI + Blockchain Powered Truth Verification System<br>
        Built for Hackathon Demo · Stack: Python · Streamlit · OpenCV · SHA-256 · Simulated Blockchain<br>
        <span style="color:#7c3aed;">Verify. Validate. Immutable.</span>
    </div>
</div>
""", unsafe_allow_html=True)
