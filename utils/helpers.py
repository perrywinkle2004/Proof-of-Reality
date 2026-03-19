"""
General utility helpers for Proof-of-Reality
"""

import json
import os
from datetime import datetime


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RECORDS_FILE = os.path.join(DATA_DIR, "records.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def load_records() -> list:
    """Load all proof records from JSON."""
    try:
        with open(RECORDS_FILE, "r") as f:
            data = json.load(f)
            return data.get("records", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_records(records: list) -> None:
    """Save proof records to JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RECORDS_FILE, "w") as f:
        json.dump({"records": records}, f, indent=2)


def load_users() -> list:
    """Load all users from JSON."""
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return data.get("users", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(users: list) -> None:
    """Save users to JSON."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2)


def get_user_by_id(user_id: str) -> dict | None:
    """Find user by user_id."""
    users = load_users()
    for u in users:
        if u["user_id"] == user_id:
            return u
    return None


def update_user(updated_user: dict) -> None:
    """Update a user record."""
    users = load_users()
    for i, u in enumerate(users):
        if u["user_id"] == updated_user["user_id"]:
            users[i] = updated_user
            break
    save_users(users)


def get_user_records(user_id: str) -> list:
    """Get all records for a specific user."""
    records = load_records()
    return [r for r in records if r.get("user_id") == user_id]


def add_record(record: dict) -> None:
    """Append a new record."""
    records = load_records()
    records.append(record)
    save_records(records)


def generate_proof_id() -> str:
    """Generate a sequential proof ID."""
    records = load_records()
    next_num = len(records) + 1
    return f"POR-{next_num:03d}"


def format_timestamp(ts_str: str) -> str:
    """Format ISO timestamp to readable form."""
    try:
        dt = datetime.fromisoformat(ts_str)
        return dt.strftime("%b %d, %Y · %H:%M")
    except Exception:
        return ts_str


def truncate_hash(hash_str: str, length: int = 16) -> str:
    """Truncate long hash for display."""
    if len(hash_str) > length:
        return hash_str[:8] + "..." + hash_str[-8:]
    return hash_str


def simulated_gps() -> str:
    """Return a random simulated GPS coordinate in India."""
    import random
    cities = [
        "28.6139° N, 77.2090° E",   # Delhi
        "19.0760° N, 72.8777° E",   # Mumbai
        "12.9716° N, 77.5946° E",   # Bangalore
        "22.5726° N, 88.3639° E",   # Kolkata
        "13.0827° N, 80.2707° E",   # Chennai
        "17.3850° N, 78.4867° E",   # Hyderabad
        "23.0225° N, 72.5714° E",   # Ahmedabad
        "18.5204° N, 73.8567° E",   # Pune
    ]
    return random.choice(cities)


def now_iso() -> str:
    """Return current datetime as ISO string."""
    return datetime.now().isoformat()
