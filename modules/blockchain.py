"""
Simulated Blockchain Layer for Proof-of-Reality
Stores only SHA-256 hashes. Immutable once written.
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Optional

CHAIN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "blockchain.json")


class Block:
    """Represents a single block in the chain."""

    def __init__(self, index: int, proof_id: str, proof_hash: str,
                 user_id: str, timestamp: str, previous_hash: str):
        self.index = index
        self.proof_id = proof_id
        self.proof_hash = proof_hash
        self.user_id = user_id
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.block_hash = self._compute_block_hash()

    def _compute_block_hash(self) -> str:
        content = f"{self.index}{self.proof_id}{self.proof_hash}{self.user_id}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "proof_id": self.proof_id,
            "proof_hash": self.proof_hash,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "block_hash": self.block_hash,
        }


def load_chain() -> list:
    """Load the blockchain from JSON file."""
    try:
        with open(CHAIN_FILE, "r") as f:
            data = json.load(f)
            return data.get("chain", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_chain(chain: list) -> None:
    """Save the blockchain to JSON file."""
    os.makedirs(os.path.dirname(CHAIN_FILE), exist_ok=True)
    with open(CHAIN_FILE, "w") as f:
        json.dump({"chain": chain, "length": len(chain)}, f, indent=2)


def get_genesis_block() -> dict:
    """Create or return the genesis block."""
    return {
        "index": 0,
        "proof_id": "GENESIS",
        "proof_hash": "0" * 64,
        "user_id": "SYSTEM",
        "timestamp": "2024-01-01T00:00:00",
        "previous_hash": "0" * 64,
        "block_hash": hashlib.sha256(b"GENESIS_PROOF_OF_REALITY").hexdigest(),
    }


def add_to_blockchain(proof_id: str, proof_hash: str, user_id: str) -> dict:
    """
    Add a new hash entry to the blockchain.
    Returns the new block data.
    """
    chain = load_chain()

    # Initialize with genesis block if empty
    if not chain:
        chain = [get_genesis_block()]

    prev_block = chain[-1]
    new_index = len(chain)
    timestamp = datetime.now().isoformat()

    block = Block(
        index=new_index,
        proof_id=proof_id,
        proof_hash=proof_hash,
        user_id=user_id,
        timestamp=timestamp,
        previous_hash=prev_block["block_hash"],
    )

    block_dict = block.to_dict()
    chain.append(block_dict)
    save_chain(chain)

    return block_dict


def verify_hash_on_chain(proof_hash: str) -> Optional[dict]:
    """
    Search the blockchain for a given proof hash.
    Returns the block if found, None otherwise.
    """
    chain = load_chain()
    for block in chain:
        if block.get("proof_hash") == proof_hash:
            return block
    return None


def verify_chain_integrity() -> dict:
    """Verify the entire chain for tampering."""
    chain = load_chain()
    if not chain:
        return {"valid": True, "length": 0, "issues": []}

    issues = []
    for i in range(1, len(chain)):
        curr = chain[i]
        prev = chain[i - 1]

        # Check previous_hash linkage
        if curr["previous_hash"] != prev["block_hash"]:
            issues.append(f"Block {i}: broken chain link (previous_hash mismatch)")

        # Re-verify block hash
        content = (
            f"{curr['index']}{curr['proof_id']}{curr['proof_hash']}"
            f"{curr['user_id']}{curr['timestamp']}{curr['previous_hash']}"
        )
        expected_hash = hashlib.sha256(content.encode()).hexdigest()
        if curr["block_hash"] != expected_hash:
            issues.append(f"Block {i}: hash integrity failure")

    return {
        "valid": len(issues) == 0,
        "length": len(chain),
        "issues": issues,
    }


def get_chain_stats() -> dict:
    """Return summary statistics of the blockchain."""
    chain = load_chain()
    if not chain:
        return {"total_blocks": 0, "total_proofs": 0, "latest_timestamp": "N/A"}

    non_genesis = [b for b in chain if b["proof_id"] != "GENESIS"]
    return {
        "total_blocks": len(chain),
        "total_proofs": len(non_genesis),
        "latest_timestamp": chain[-1]["timestamp"] if chain else "N/A",
        "chain_valid": verify_chain_integrity()["valid"],
    }
