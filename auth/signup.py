"""
Signup module for Proof-of-Reality auth system.
"""

import streamlit as st
from datetime import datetime
from utils.helpers import load_users, save_users
import random


AVATAR_COLORS = ["#7c3aed", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4"]


def render_signup_form() -> bool:
    """
    Render the signup form and handle registration.
    Returns True if signup was successful.
    """
    st.markdown("""<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7c3aed, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    ">Create Account</h2>
    <p style="color: var(--text-muted); font-size: 0.9rem;">Join the Proof-of-Reality network</p>
</div>
""", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
    email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="signup_password")
    confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="signup_confirm")

    signup_btn = st.button("🚀 Create Account", use_container_width=True)

    if signup_btn:
        # Validation
        if not username or not email or not password:
            st.error("All fields are required.")
            return False
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return False
        if password != confirm:
            st.error("Passwords do not match.")
            return False

        users = load_users()
        # Check username taken
        for u in users:
            if u["username"] == username:
                st.error(f"Username '{username}' is already taken.")
                return False
            if u["email"] == email:
                st.error("Email already registered.")
                return False

        # Create user
        new_user = {
            "user_id": username,
            "username": username,
            "email": email,
            "password": password,
            "trust_score": 50,
            "verified_proofs": 0,
            "suspicious_proofs": 0,
            "joined": datetime.now().isoformat(),
            "avatar_color": random.choice(AVATAR_COLORS),
            "notifications": [
                {
                    "id": 1,
                    "msg": "Welcome to Proof-of-Reality! 🎉 Your account is ready.",
                    "read": False,
                    "time": datetime.now().isoformat(),
                }
            ],
        }
        users.append(new_user)
        save_users(users)

        st.success(f"✅ Account created! Welcome, {username}!")
        st.session_state["logged_in"] = True
        st.session_state["user_id"] = username
        st.session_state["username"] = username
        st.session_state["current_page"] = "dashboard"
        return True

    return False
