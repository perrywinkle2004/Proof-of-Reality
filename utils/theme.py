"""
Theme system for Proof-of-Reality
Handles dark/light mode and global CSS injection
"""

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;600;800;900&family=JetBrains+Mono:wght@300;400;600&display=swap');

:root {
    --bg-primary: #06010f;
    --bg-secondary: #0d0820;
    --bg-card: rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.08);
    --border-color: rgba(139,92,246,0.25);
    --border-glow: rgba(139,92,246,0.6);
    --text-primary: #f0eaff;
    --text-secondary: #a78bfa;
    --text-muted: #6b7280;
    --accent-purple: #7c3aed;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-orange: #f59e0b;
    --gradient-hero: linear-gradient(135deg, #1a0533 0%, #06010f 40%, #000d1a 100%);
    --gradient-card: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(59,130,246,0.05) 100%);
    --gradient-accent: linear-gradient(90deg, #7c3aed, #3b82f6);
    --shadow-glow: 0 0 30px rgba(124,58,237,0.3);
    --shadow-card: 0 8px 32px rgba(0,0,0,0.5);
    --blur: blur(20px);
}

/* ── KEYFRAMES ─────────────────────────────────────── */

@keyframes pageFadeUp {
    0%  { opacity: 0; transform: translateY(18px); }
    100%{ opacity: 1; transform: translateY(0); }
}

@keyframes surfingBg {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes navSlideDown {
    0%  { opacity: 0; transform: translateY(-100%); }
    100%{ opacity: 1; transform: translateY(0); }
}

@keyframes aiPulse {
    0%  { box-shadow: 0 0 10px rgba(124,58,237,0.3), 0 0 20px rgba(59,130,246,0.1); }
    33% { box-shadow: 0 0 20px rgba(124,58,237,0.6), 0 0 40px rgba(59,130,246,0.3); }
    66% { box-shadow: 0 0 15px rgba(6,182,212,0.5),  0 0 30px rgba(124,58,237,0.4); }
    100%{ box-shadow: 0 0 10px rgba(124,58,237,0.3), 0 0 20px rgba(59,130,246,0.1); }
}

@keyframes gradientWave {
    0%  { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100%{ background-position: 0% 50%; }
}

@keyframes progressFill {
    0%  { width: 0%; }
    100%{ width: 100%; }
}

@keyframes scrollReveal {
    0%  { opacity: 0; transform: translateY(30px); }
    100%{ opacity: 1; transform: translateY(0); }
}

@keyframes countUp {
    0%  { opacity: 0; transform: scale(0.8); }
    100%{ opacity: 1; transform: scale(1); }
}

/* ── SURFING ANIMATED BACKGROUND ───────────────────── */

.stApp {
    background: linear-gradient(
        -45deg,
        #06010f,
        #0d0820,
        #1a0533,
        #000d1a,
        #06010f,
        #0a0520,
        #001020
    ) !important;
    background-size: 400% 400% !important;
    animation: surfingBg 18s ease infinite !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* ── PAGE TRANSITION ────────────────────────────────── */

.main .block-container {
    animation: pageFadeUp 0.5s ease both !important;
}

/* ── NAVBAR GLASS EFFECT ────────────────────────────── */

[data-testid="stHeader"] {
    background: rgba(6,1,15,0.7) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid rgba(139,92,246,0.2) !important;
    animation: navSlideDown 0.5s ease both !important;
}

/* ── HIDE STREAMLIT DEFAULT ELEMENTS ────────────────── */

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ── SCROLLBAR ──────────────────────────────────────── */

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #3b82f6);
    border-radius: 3px;
}

/* ── STREAMLIT OVERRIDES ────────────────────────────── */

.stMarkdown, .stText { color: var(--text-primary) !important; }

/* ── BUTTON EFFECTS ─────────────────────────────────── */

.stButton > button {
    background: var(--gradient-accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transform: translateX(-100%);
    transition: transform 0.4s ease;
}
.stButton > button:hover::after {
    transform: translateX(100%);
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 30px rgba(124,58,237,0.7) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4) !important;
}

/* ── INPUTS ─────────────────────────────────────────── */

.stTextInput > div > div > input, .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2), 0 0 12px rgba(124,58,237,0.15) !important;
}

/* ── FILE UPLOADER ──────────────────────────────────── */

[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 2px dashed var(--border-color) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.2) !important;
}

/* ── METRIC CARDS ───────────────────────────────────── */

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    backdrop-filter: var(--blur) !important;
    transition: all 0.3s ease !important;
    animation: countUp 0.6s ease both !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.25) !important;
    transform: translateY(-4px) !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent-purple) !important;
    font-family: 'Orbitron', monospace !important;
    animation: countUp 0.8s ease both !important;
}

/* ── PROGRESS BAR ───────────────────────────────────── */

.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #06b6d4) !important;
    background-size: 200% 100% !important;
    animation: gradientWave 3s linear infinite !important;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-radius: 4px !important;
}

/* ── TABS ───────────────────────────────────────────── */

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    backdrop-filter: var(--blur) !important;
    border: 1px solid var(--border-color) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--gradient-accent) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4) !important;
}

/* ── GLASS CARDS ────────────────────────────────────── */

.glass-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    animation: scrollReveal 0.5s ease both !important;
}
.glass-card:hover {
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 0 16px 48px rgba(124,58,237,0.35) !important;
}

/* ── AI GLOW ────────────────────────────────────────── */

.ai-glow {
    animation: aiPulse 3s ease-in-out infinite !important;
    border-radius: 16px;
}

/* ── DIVIDER ────────────────────────────────────────── */

hr { border-color: var(--border-color) !important; }

/* ── ALERT BOXES ────────────────────────────────────── */

.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    backdrop-filter: var(--blur) !important;
}

/* ── SCROLL REVEAL UTILITY ──────────────────────────── */

.reveal {
    animation: scrollReveal 0.6s ease both;
}
.reveal-delay-1 { animation-delay: 0.1s; }
.reveal-delay-2 { animation-delay: 0.2s; }
.reveal-delay-3 { animation-delay: 0.3s; }

</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;600;800;900&family=JetBrains+Mono:wght@300;400;600&display=swap');

:root {
    --bg-primary: #f5f0ff;
    --bg-secondary: #ede8ff;
    --bg-card: rgba(255,255,255,0.7);
    --bg-card-hover: rgba(255,255,255,0.9);
    --border-color: rgba(124,58,237,0.2);
    --border-glow: rgba(124,58,237,0.5);
    --text-primary: #1a1035;
    --text-secondary: #7c3aed;
    --text-muted: #6b7280;
    --accent-purple: #7c3aed;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-orange: #f59e0b;
    --gradient-hero: linear-gradient(135deg, #ede8ff 0%, #f5f0ff 50%, #e0f2fe 100%);
    --gradient-card: linear-gradient(135deg, rgba(124,58,237,0.08) 0%, rgba(59,130,246,0.04) 100%);
    --gradient-accent: linear-gradient(90deg, #7c3aed, #3b82f6);
    --shadow-glow: 0 0 20px rgba(124,58,237,0.15);
    --shadow-card: 0 4px 20px rgba(0,0,0,0.08);
    --blur: blur(20px);
}

@keyframes pageFadeUp {
    0%  { opacity: 0; transform: translateY(18px); }
    100%{ opacity: 1; transform: translateY(0); }
}
@keyframes surfingBgLight {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes countUp {
    0%  { opacity: 0; transform: scale(0.8); }
    100%{ opacity: 1; transform: scale(1); }
}

.stApp {
    background: linear-gradient(-45deg, #ede8ff, #f5f0ff, #e0f2fe, #f0e8ff, #ede8ff) !important;
    background-size: 400% 400% !important;
    animation: surfingBgLight 18s ease infinite !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    animation: pageFadeUp 0.5s ease both !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.stButton > button {
    background: var(--gradient-accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 28px rgba(124,58,237,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
}

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    animation: countUp 0.6s ease both !important;
    transition: all 0.3s ease !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.2) !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent-purple) !important;
    font-family: 'Orbitron', monospace !important;
    animation: countUp 0.8s ease both !important;
}

.stProgress > div > div > div {
    background: var(--gradient-accent) !important;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
hr { border-color: var(--border-color) !important; }
</style>
"""


def get_css(theme: str = "dark") -> str:
    """Return CSS string for given theme."""
    return DARK_CSS if theme == "dark" else LIGHT_CSS


def glass_card(content_html: str, extra_style: str = "") -> str:
    """Wrap HTML content in a glassmorphism card."""
    return f"""
    <div style="
        background: var(--bg-card);
        backdrop-filter: var(--blur);
        -webkit-backdrop-filter: var(--blur);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: var(--shadow-card);
        transition: all 0.3s ease;
        {extra_style}
    ">
        {content_html}
    </div>
    """


def glow_badge(text: str, color: str = "#7c3aed") -> str:
    """Return a glowing badge HTML."""
    return f"""
    <span style="
        background: {color}22;
        color: {color};
        border: 1px solid {color}55;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.5px;
    ">{text}</span>
    """


def status_color(status: str) -> str:
    """Return color for a given status."""
    colors = {
        "VERIFIED": "#10b981",
        "SUSPICIOUS": "#ef4444",
        "NEEDS_REVIEW": "#f59e0b",
        "PENDING": "#6b7280",
    }
    return colors.get(status, "#6b7280")


def score_color(score: int) -> str:
    """Return color based on authenticity score."""
    if score >= 80:
        return "#10b981"
    elif score >= 60:
        return "#f59e0b"
    else:
        return "#ef4444"
