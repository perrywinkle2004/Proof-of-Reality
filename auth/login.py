"""
Login module for Proof-of-Reality auth system.
"""

import streamlit as st
from utils.helpers import load_users
from utils.theme import glass_card


def render_login_form() -> bool:
    """
    Render the login form and handle authentication.
    Returns True if login was successful.
    """
    st.markdown("""<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7c3aed, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    ">Welcome Back</h2>
    <p style="color: var(--text-muted); font-size: 0.9rem;">Sign in to your PoR account</p>
</div>
""", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username", key="login_username")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

    col1, col2 = st.columns([1, 1])
    with col1:
        login_btn = st.button("🔓 Sign In", use_container_width=True)
    with col2:
        demo_btn = st.button("🚀 Demo Login", use_container_width=True)

    if demo_btn:
        username = "demo_user"
        password = "demo1234"
        login_btn = True

    if login_btn:
        if not username or not password:
            st.error("Please enter username and password.")
            return False

        users = load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user["user_id"]
                st.session_state["username"] = user["username"]
                st.session_state["current_page"] = "dashboard"
                return True

        st.error("❌ Invalid username or password.")
        return False

    return False
