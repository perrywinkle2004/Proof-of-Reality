"""
SHA-256 Hash Generator for Proof-of-Reality
Generates deterministic hashes for uploaded proof files.
"""

import hashlib
import json
from datetime import datetime


def generate_file_hash(file_bytes: bytes) -> str:
    """Generate SHA-256 hash from raw file bytes."""
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()


def generate_proof_hash(file_bytes: bytes, user_id: str, timestamp: str) -> str:
    """
    Generate a composite SHA-256 hash combining:
    - File content
    - User ID
    - Timestamp
    This ensures two identical files from different users/times get different hashes.
    """
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    sha256.update(user_id.encode("utf-8"))
    sha256.update(timestamp.encode("utf-8"))
    return sha256.hexdigest()


def generate_metadata_hash(metadata: dict) -> str:
    """Generate hash from a metadata dictionary (JSON-serialized)."""
    sha256 = hashlib.sha256()
    serialized = json.dumps(metadata, sort_keys=True).encode("utf-8")
    sha256.update(serialized)
    return sha256.hexdigest()


def verify_hash(file_bytes: bytes, expected_hash: str) -> bool:
    """Verify that file bytes match an expected hash."""
    actual = generate_file_hash(file_bytes)
    return actual == expected_hash


def format_hash_display(hash_str: str) -> str:
    """Format hash in groups of 8 for readability."""
    chunks = [hash_str[i:i+8] for i in range(0, len(hash_str), 8)]
    return " ".join(chunks)
