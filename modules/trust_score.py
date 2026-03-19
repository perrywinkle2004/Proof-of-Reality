"""
Trust Score System for Proof-of-Reality
Each user starts at 50. Score increases for valid proofs, decreases for suspicious ones.
"""

from utils.helpers import get_user_by_id, update_user


def calculate_trust_delta(authenticity_score: int, status: str) -> int:
    """
    Calculate how much the trust score should change based on submission result.
    Verified: +2 to +8 depending on score
    Suspicious: -5 to -15 depending on severity
    Needs Review: +1 (slight positive, awaiting review)
    """
    if status == "VERIFIED":
        if authenticity_score >= 90:
            return 8
        elif authenticity_score >= 80:
            return 5
        else:
            return 2
    elif status == "SUSPICIOUS":
        if authenticity_score < 30:
            return -15
        elif authenticity_score < 50:
            return -10
        else:
            return -5
    elif status == "NEEDS_REVIEW":
        return 1
    return 0


def update_trust_score(user_id: str, authenticity_score: int, status: str) -> dict:
    """
    Update a user's trust score after a proof submission.
    Returns dict with old score, delta, new score.
    """
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}

    old_score = user.get("trust_score", 50)
    delta = calculate_trust_delta(authenticity_score, status)
    new_score = max(0, min(100, old_score + delta))

    # Update user record
    user["trust_score"] = new_score
    if status == "VERIFIED":
        user["verified_proofs"] = user.get("verified_proofs", 0) + 1
    elif status == "SUSPICIOUS":
        user["suspicious_proofs"] = user.get("suspicious_proofs", 0) + 1

    # Add notification
    notifications = user.get("notifications", [])
    if delta > 0:
        msg = f"Trust score increased by +{delta} → {new_score} ⭐"
    elif delta < 0:
        msg = f"Trust score decreased by {delta} → {new_score} ⚠️"
    else:
        msg = f"Proof submitted for review. Score unchanged: {new_score}"

    notifications.insert(0, {
        "id": len(notifications) + 1,
        "msg": msg,
        "read": False,
        "time": __import__("utils.helpers", fromlist=["now_iso"]).now_iso()
            if hasattr(__import__("utils.helpers", fromlist=["now_iso"]), "now_iso")
            else "now",
    })
    user["notifications"] = notifications[:20]  # Keep last 20

    update_user(user)

    return {
        "old_score": old_score,
        "delta": delta,
        "new_score": new_score,
        "status": status,
    }


def get_trust_level(score: int) -> dict:
    """Return trust level label and color for a given score."""
    if score >= 90:
        return {"label": "ELITE", "color": "#10b981", "emoji": "🏆"}
    elif score >= 75:
        return {"label": "TRUSTED", "color": "#3b82f6", "emoji": "✅"}
    elif score >= 55:
        return {"label": "MODERATE", "color": "#f59e0b", "emoji": "⚡"}
    elif score >= 35:
        return {"label": "CAUTIOUS", "color": "#f97316", "emoji": "⚠️"}
    else:
        return {"label": "FLAGGED", "color": "#ef4444", "emoji": "🚨"}


def trust_score_bar_html(score: int) -> str:
    """Return HTML for a stylized trust score progress bar."""
    level = get_trust_level(score)
    color = level["color"]
    pct = score

    return f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--text-muted);">
                TRUST SCORE
            </span>
            <span style="font-family: 'Orbitron', monospace; font-size: 1.1rem; font-weight: 700; color: {color};">
                {score} {level['emoji']}
            </span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 999px; height: 8px; overflow: hidden;">
            <div style="
                width: {pct}%;
                height: 100%;
                background: linear-gradient(90deg, {color}, {color}aa);
                border-radius: 999px;
                transition: width 0.8s ease;
                box-shadow: 0 0 8px {color}88;
            "></div>
        </div>
        <div style="text-align: right; margin-top: 4px;">
            <span style="
                background: {color}22;
                color: {color};
                border: 1px solid {color}44;
                border-radius: 20px;
                padding: 2px 10px;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 1px;
            ">{level['label']}</span>
        </div>
    </div>
    """
