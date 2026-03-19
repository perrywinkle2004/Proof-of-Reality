"""
Proof-of-Reality (PoR) — Main Application Entry Point
AI + Blockchain Powered Truth Verification System
"""

import streamlit as st
import sys
import os

# ── Path setup ─────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="PoR",
    page_icon="⛓️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Imports ────────────────────────────────────────────
from utils.theme import get_css
from pages.landing import render_landing
from pages.dashboard import render_dashboard
from pages.upload_verify import render_upload_verify
from pages.verification import render_verification
from pages.analytics import render_analytics
from pages.settings import render_settings
from auth.login import render_login_form
from auth.signup import render_signup_form

# ── Session defaults ───────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "user_id": None,
        "username": None,
        "current_page": "landing",
        "theme": "dark",
        "auth_mode": "login",
        "notif_pref": True,
        "email_alerts": False,
        "auto_blockchain": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ── Inject CSS ─────────────────────────────────────────
st.markdown(get_css(st.session_state["theme"]), unsafe_allow_html=True)

# Fix HTML rendering issue
st.markdown("""
<style>
div[data-testid="stMarkdownContainer"] > div {
    white-space: normal !important;
}
</style>
""", unsafe_allow_html=True)

# ── Navbar ─────────────────────────────────────────────
def render_navbar():
    from utils.helpers import get_user_by_id

    logged_in = st.session_state.get("logged_in", False)
    current_page = st.session_state.get("current_page", "landing")
    theme = st.session_state.get("theme", "dark")
    theme_icon = "☀️" if theme == "dark" else "🌙"

    notif_count = 0
    if logged_in:
        user = get_user_by_id(st.session_state.get("user_id", ""))
        if user:
            notif_count = sum(1 for n in user.get("notifications", []) if not n.get("read"))

    notif_label = f"🔔 {notif_count}" if notif_count > 0 else "🔔"

    # Header
    st.markdown("""
    <div style="
        padding: 1rem;
        border-bottom: 1px solid rgba(124,58,237,0.2);
        margin-bottom: 1rem;
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 1.2rem;
    ">
        ⛓️ Proof-of-Reality
    </div>
    """, unsafe_allow_html=True)

    # ── NAV BUTTONS ─────────────────────────
    if logged_in:
        nav_items = [
            ("🏠", "Home", "landing"),
            ("📊", "Dashboard", "dashboard"),
            ("📤", "Submit Proof", "upload"),
            ("🔍", "Verify", "verification"),
            ("📈", "Analytics", "analytics"),
            ("⚙️", "Settings", "settings"),
        ]

        cols = st.columns(len(nav_items) + 2)

        for i, (icon, label, page) in enumerate(nav_items):
            with cols[i]:
                if st.button(
                    f"{icon} {label}",
                    use_container_width=True,
                    key=f"nav_{page}"
                ):
                    st.session_state["current_page"] = page
                    st.rerun()

        # 🔔 Notification
        with cols[len(nav_items)]:
            if st.button(
                notif_label,
                use_container_width=True,
                key="nav_notif_btn"
            ):
                st.session_state["current_page"] = "dashboard"
                st.rerun()

        # 🌙 Theme toggle
        with cols[len(nav_items) + 1]:
            if st.button(
                theme_icon,
                use_container_width=True,
                key="nav_theme_btn"
            ):
                st.session_state["theme"] = "light" if theme == "dark" else "dark"
                st.rerun()

    else:
        col1, col2, col3, col4, _ = st.columns([1,1,1,1,4])

        with col1:
            if st.button("🏠 Home", use_container_width=True, key="guest_home"):
                st.session_state["current_page"] = "landing"
                st.rerun()

        with col2:
            if st.button("🔑 Login", use_container_width=True, key="guest_login"):
                st.session_state["auth_mode"] = "login"
                st.session_state["current_page"] = "auth"
                st.rerun()

        with col3:
            if st.button("🚀 Sign Up", use_container_width=True, key="guest_signup"):
                st.session_state["auth_mode"] = "signup"
                st.session_state["current_page"] = "auth"
                st.rerun()

        with col4:
            if st.button(theme_icon, use_container_width=True, key="guest_theme"):
                st.session_state["theme"] = "light" if theme == "dark" else "dark"
                st.rerun()

# ── Auth Page ──────────────────────────────────────────
def render_auth_page():
    st.subheader("Authentication")

    tab1, tab2 = st.tabs(["🔑 Login", "🚀 Sign Up"])

    with tab1:
        if render_login_form():
            st.rerun()

    with tab2:
        if render_signup_form():
            st.rerun()

    if st.button("← Back to Home", key="back_home_btn"):
        st.session_state["current_page"] = "landing"
        st.rerun()

# ── Router ─────────────────────────────────────────────
def main():
    render_navbar()

    current_page = st.session_state.get("current_page", "landing")
    logged_in = st.session_state.get("logged_in", False)

    protected = {"dashboard", "upload", "verification", "analytics", "settings"}

    if current_page == "landing":
        render_landing()

    elif current_page == "auth":
        render_auth_page()

    elif current_page in protected and not logged_in:
        st.warning("🔒 Please log in to access this page.")
        render_auth_page()

    elif current_page == "dashboard":
        render_dashboard()

    elif current_page == "upload":
        render_upload_verify()

    elif current_page == "verification":
        render_verification()

    elif current_page == "analytics":
        render_analytics()

    elif current_page == "settings":
        render_settings()

    else:
        render_landing()

    # ── FLOATING CHATBOT ───────────────────────────────────
    if logged_in and current_page not in ["landing", "auth"]:
        from utils.chatbot import render_floating_chatbot
        render_floating_chatbot()

# ── Run ────────────────────────────────────────────────
if __name__ == "__main__":
    main()