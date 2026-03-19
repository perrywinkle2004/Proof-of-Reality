import streamlit as st
import base64

def render_landing():
    
    # ── LOAD LOGO ────────────────────────────────────────
    st.set_option('client.showErrorDetails', False)

    # ── AI BACKGROUND + ANIMATIONS ───────────────────────
    st.markdown("""
    <style>

    @keyframes float1 {
        0%,100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(-30px,30px) scale(1.1); }
    }

    @keyframes float2 {
        0%,100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(30px,-25px) scale(1.08); }
    }

    @keyframes float3 {
        0%,100% { transform: translate(-50%,-50%) scale(1); }
        50% { transform: translate(-50%,-50%) scale(1.05) rotate(10deg); }
    }

    @keyframes orbPulse {
        0%,100% { opacity: 0.4; }
        50% { opacity: 0.8; }
    }

    @keyframes heroFadeUp {
        0%  { opacity: 0; transform: translateY(30px); }
        100%{ opacity: 1; transform: translateY(0); }
    }

    @keyframes taglineShimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes titleGlow {
        0%,100% { filter: drop-shadow(0 0 8px rgba(124,58,237,0.4)); }
        50%     { filter: drop-shadow(0 0 20px rgba(59,130,246,0.7)); }
    }

    @keyframes cardReveal {
        0%  { opacity: 0; transform: translateY(24px); }
        100%{ opacity: 1; transform: translateY(0); }
    }

    .ai-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
        pointer-events: none;
    }

    .orb1, .orb2, .orb3 {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
    }

    .orb1 {
        width: 350px;
        height: 350px;
        background: rgba(124,58,237,0.28);
        top: 8%;
        left: 8%;
        animation: float1 10s infinite ease-in-out;
    }

    .orb2 {
        width: 280px;
        height: 280px;
        background: rgba(59,130,246,0.28);
        bottom: 10%;
        right: 8%;
        animation: float2 13s infinite ease-in-out;
    }

    .orb3 {
        width: 200px;
        height: 200px;
        background: rgba(6,182,212,0.2);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: float3 16s infinite ease-in-out;
    }

    .hero {
        text-align: center;
        padding: 4rem 2rem 3rem;
        animation: heroFadeUp 0.7s ease both;
    }

    .title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #3b82f6, #06b6d4, #7c3aed);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: taglineShimmer 6s linear infinite, titleGlow 4s ease-in-out infinite;
    }

    .subtitle {
        color: #a78bfa;
        font-size: 1.25rem;
        margin-top: 0.75rem;
        animation: heroFadeUp 0.7s ease 0.15s both;
    }

    .tagline {
        display: inline-block;
        margin-top: 0.75rem;
        font-size: 0.95rem;
        font-style: italic;
        font-weight: 600;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399, #a78bfa);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: taglineShimmer 5s linear infinite, heroFadeUp 0.7s ease 0.3s both;
        letter-spacing: 1px;
    }

    .glass-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(124,58,237,0.2);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        animation: cardReveal 0.6s ease both;
    }

    .glass-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 48px rgba(124,58,237,0.35);
        border-color: rgba(124,58,237,0.5);
    }

    .feature-title {
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: #a78bfa;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    </style>

    <div class="ai-bg">
        <div class="orb1"></div>
        <div class="orb2"></div>
        <div class="orb3"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── LOGO & HERO ──────────────────────────────────────
    with open("assets/logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div class="hero">
        <img src="data:image/png;base64,{logo_b64}" width="120" style="margin-bottom: 20px; display: inline-block;">
        <div class="title">Proof-of-Reality</div>
        <div class="subtitle">A Trust Layer for the Real World</div>
        <div class="tagline">"If it's not on-chain, it isn't verified."</div>
    </div>
    """, unsafe_allow_html=True)

    # ── BUTTONS (Login + Sign Up only) ───────────────────
    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

    with col2:
        if st.button("🔑 Login", use_container_width=True, key="landing_login"):
            st.session_state["auth_mode"] = "login"
            st.session_state["current_page"] = "auth"
            st.rerun()

    with col3:
        if st.button("🚀 Sign Up", use_container_width=True, key="landing_signup"):
            st.session_state["auth_mode"] = "signup"
            st.session_state["current_page"] = "auth"
            st.rerun()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── FEATURES ─────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2rem;">🤖</div>
            <div class="feature-title" style="color:#7c3aed;">AI Validation</div>
            <div class="feature-desc">
                Detect tampering, analyze metadata, and verify authenticity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2rem;">⛓️</div>
            <div class="feature-title" style="color:#3b82f6;">Blockchain Security</div>
            <div class="feature-desc">
                Immutable SHA-256 hashing ensures data cannot be altered.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:2rem;">⚡</div>
            <div class="feature-title" style="color:#06b6d4;">Real-Time Verification</div>
            <div class="feature-desc">
                Instant scoring and trust validation in seconds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── CTA ──────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card">
        <h3 style="font-family:'Orbitron',monospace;">
            Build Trust in a Noisy World
        </h3>
        <p style="color:#a78bfa;">
            "If it's not on-chain, it isn't verified."
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,1,2])

    with col2:
        if st.button("✨ Try Demo", use_container_width=True, key="landing_demo"):
            st.session_state["auth_mode"] = "login"
            st.session_state["current_page"] = "auth"
            st.rerun()