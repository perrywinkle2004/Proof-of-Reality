"""
Analytics Tracker for Proof-of-Reality
Computes stats from proof records for dashboard charts.
"""

from collections import Counter, defaultdict
from datetime import datetime
from utils.helpers import load_records, load_users


def get_verification_stats() -> dict:
    """Compute overall verification statistics."""
    records = load_records()
    if not records:
        return {
            "total": 0, "verified": 0, "suspicious": 0,
            "needs_review": 0, "fraud_rate": 0.0, "success_rate": 0.0
        }

    total = len(records)
    verified = sum(1 for r in records if r.get("status") == "VERIFIED")
    suspicious = sum(1 for r in records if r.get("status") == "SUSPICIOUS")
    needs_review = sum(1 for r in records if r.get("status") == "NEEDS_REVIEW")

    return {
        "total": total,
        "verified": verified,
        "suspicious": suspicious,
        "needs_review": needs_review,
        "fraud_rate": round(suspicious / total * 100, 1) if total else 0.0,
        "success_rate": round(verified / total * 100, 1) if total else 0.0,
    }


def get_score_distribution() -> dict:
    """Get distribution of authenticity scores in buckets."""
    records = load_records()
    buckets = {
        "0-20": 0, "21-40": 0, "41-60": 0,
        "61-80": 0, "81-100": 0
    }
    for r in records:
        s = r.get("authenticity_score", 0)
        if s <= 20:
            buckets["0-20"] += 1
        elif s <= 40:
            buckets["21-40"] += 1
        elif s <= 60:
            buckets["41-60"] += 1
        elif s <= 80:
            buckets["61-80"] += 1
        else:
            buckets["81-100"] += 1
    return buckets


def get_trust_score_distribution() -> list:
    """Get list of all user trust scores."""
    users = load_users()
    return [u.get("trust_score", 50) for u in users]


def get_time_trends() -> dict:
    """
    Get monthly submission counts by status.
    Returns dict of {month_str: {verified, suspicious, needs_review}}
    """
    records = load_records()
    monthly = defaultdict(lambda: {"VERIFIED": 0, "SUSPICIOUS": 0, "NEEDS_REVIEW": 0})

    for r in records:
        try:
            dt = datetime.fromisoformat(r.get("timestamp", "2024-01-01"))
            month_key = dt.strftime("%b %Y")
            status = r.get("status", "NEEDS_REVIEW")
            if status in monthly[month_key]:
                monthly[month_key][status] += 1
        except Exception:
            pass

    # Sort by date
    sorted_months = sorted(
        monthly.keys(),
        key=lambda m: datetime.strptime(m, "%b %Y")
    )
    return {m: monthly[m] for m in sorted_months}


def get_per_user_stats() -> list:
    """Get per-user submission statistics."""
    records = load_records()
    user_data = defaultdict(lambda: {"verified": 0, "suspicious": 0, "total": 0})

    for r in records:
        uid = r.get("user_id", "unknown")
        status = r.get("status", "")
        user_data[uid]["total"] += 1
        if status == "VERIFIED":
            user_data[uid]["verified"] += 1
        elif status == "SUSPICIOUS":
            user_data[uid]["suspicious"] += 1

    result = []
    for uid, stats in user_data.items():
        result.append({
            "user_id": uid,
            "total": stats["total"],
            "verified": stats["verified"],
            "suspicious": stats["suspicious"],
            "accuracy": round(stats["verified"] / stats["total"] * 100, 1) if stats["total"] else 0,
        })
    return sorted(result, key=lambda x: x["total"], reverse=True)


def get_average_authenticity_score() -> float:
    """Compute average authenticity score across all records."""
    records = load_records()
    if not records:
        return 0.0
    scores = [r.get("authenticity_score", 0) for r in records]
    return round(sum(scores) / len(scores), 1)


def get_blockchain_stats() -> dict:
    """Get blockchain layer statistics."""
    try:
        from modules.blockchain import get_chain_stats
        return get_chain_stats()
    except Exception:
        return {"total_blocks": 0, "total_proofs": 0, "chain_valid": True}
