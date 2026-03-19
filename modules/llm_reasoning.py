"""
LLM Reasoning Layer for Proof-of-Reality
Generates human-readable explanations from validation results.
Rule-based explanation generator (simulates LLM output).
"""

from typing import Any


def generate_explanation(validation_result: dict) -> str:
    """
    Generate a detailed, human-readable explanation of the validation result.
    Simulates LLM reasoning with structured rule-based logic.
    """
    score = validation_result.get("authenticity_score", 0)
    tampering_prob = validation_result.get("tampering_probability", 0)
    confidence = validation_result.get("confidence", "LOW")
    status = validation_result.get("status", "SUSPICIOUS")
    is_duplicate = validation_result.get("is_duplicate", False)
    metadata_check = validation_result.get("metadata_check", {})
    tampering_details = validation_result.get("tampering_details", {})
    active_indicators = validation_result.get("active_indicators", 0)

    indicators = tampering_details.get("indicators", {})
    details = tampering_details.get("details", {})
    metadata_issues = metadata_check.get("issues", [])

    # Opening verdict
    if score >= 85:
        opening = (
            f"✅ **Verification Passed** — This proof demonstrates strong authenticity indicators "
            f"with an Authenticity Score of **{score}/100** and {confidence} confidence."
        )
    elif score >= 70:
        opening = (
            f"✅ **Likely Authentic** — This proof passes core validation checks "
            f"with a score of **{score}/100**. Minor anomalies detected but within acceptable range."
        )
    elif score >= 50:
        opening = (
            f"⚠️ **Needs Review** — This proof shows mixed signals. "
            f"Score: **{score}/100**. Human review is recommended before approval."
        )
    else:
        opening = (
            f"❌ **Verification Failed** — This proof has been flagged as likely inauthentic. "
            f"Authenticity Score: **{score}/100**. High tampering probability detected."
        )

    reasons = []

    # Tampering analysis reasoning
    if tampering_prob < 0.15:
        reasons.append(
            "🔬 **Image Forensics**: No significant tampering signatures detected. "
            "Pixel-level analysis, noise distribution, and edge consistency all appear natural."
        )
    elif tampering_prob < 0.40:
        reasons.append(
            f"🔬 **Image Forensics**: Minor anomalies detected (tampering probability: {tampering_prob:.0%}). "
            "Could be due to compression or standard photo editing."
        )
    else:
        reasons.append(
            f"🔬 **Image Forensics**: Significant tampering indicators found (probability: {tampering_prob:.0%}). "
            "Pixel patterns suggest possible post-capture manipulation."
        )

    # Specific indicator reasoning
    if indicators.get("noise_inconsistency"):
        reasons.append(
            "📊 **Noise Analysis**: Inconsistent noise distribution across color channels detected. "
            "This is a common signature of composite images or selective editing."
        )

    if indicators.get("edge_anomaly"):
        reasons.append(
            "📐 **Edge Analysis**: Unusual sharpness patterns found. "
            "May indicate blurring, content-aware fill, or digital generation artifacts."
        )

    if indicators.get("color_anomaly"):
        reasons.append(
            "🎨 **Color Analysis**: Histogram anomalies detected. "
            "The color distribution is inconsistent with typical natural photography."
        )

    if indicators.get("compression_artifact"):
        reasons.append(
            "💾 **Compression Analysis**: Image editing software artifacts detected in metadata. "
            "File may have been processed in Photoshop, GIMP, or similar tools."
        )

    if indicators.get("resolution_inconsistency"):
        reasons.append(
            "📏 **Resolution Check**: Unusually small image dimensions detected. "
            "Low-resolution images may indicate cropping to remove context."
        )

    # EXIF metadata
    if details.get("has_exif") is True:
        reasons.append(
            "📋 **EXIF Metadata**: Camera metadata present and consistent with original capture. "
            "Timestamp, GPS, and device information appear unmodified."
        )
    elif details.get("has_exif") is False:
        reasons.append(
            "📋 **EXIF Metadata**: No EXIF data found. Metadata may have been stripped — "
            "this can be a sign of processing, though some platforms remove metadata by default."
        )

    # Duplicate detection
    if is_duplicate:
        dup_info = validation_result.get("duplicate_info", {})
        orig_id = dup_info.get("original_proof_id", "unknown")
        reasons.append(
            f"🔁 **Duplicate Detection**: ⚠️ This file matches an existing proof ({orig_id}). "
            "Submitting duplicate evidence constitutes potential fraud."
        )
    else:
        reasons.append(
            "🔁 **Duplicate Detection**: No matching records found in the database. "
            "This appears to be a unique, previously unsubmitted proof."
        )

    # Metadata consistency
    if metadata_check.get("is_consistent"):
        reasons.append(
            "🕐 **Metadata Consistency**: Timestamp and filename pass consistency checks. "
            "Temporal markers align with the claimed incident window."
        )
    else:
        for issue in metadata_issues:
            reasons.append(f"🕐 **Metadata Warning**: {issue}.")

    # Software detection
    if details.get("software_detected"):
        reasons.append(
            f"🖥️ **Software Detection**: Editing software signature found: `{details['software_detected']}`. "
            "This strongly suggests post-capture modification."
        )

    # Closing recommendation
    if status == "VERIFIED":
        closing = (
            "\n\n**Recommendation**: This proof meets the authenticity threshold for blockchain storage. "
            "It has been hashed and recorded on the verification ledger. The insurer may proceed with confidence."
        )
    elif status == "NEEDS_REVIEW":
        closing = (
            "\n\n**Recommendation**: This proof requires manual review by a human assessor before approval. "
            "It has been flagged in the system but NOT automatically approved. "
            "Additional documentation may be requested."
        )
    else:
        closing = (
            "\n\n**Recommendation**: This proof has been **rejected** due to authenticity concerns. "
            "It has been logged as a suspicious submission. Repeated suspicious submissions will "
            "significantly reduce the user's Trust Score and may trigger a fraud investigation."
        )

    # Assemble final explanation
    explanation = opening + "\n\n"
    explanation += "---\n\n"
    explanation += "**Detailed Analysis:**\n\n"
    for r in reasons:
        explanation += f"- {r}\n"
    explanation += closing

    return explanation


def generate_short_summary(validation_result: dict) -> str:
    """Generate a one-line summary for dashboard display."""
    score = validation_result.get("authenticity_score", 0)
    status = validation_result.get("status", "SUSPICIOUS")

    if status == "VERIFIED":
        return f"Proof verified ✅ — Authenticity Score {score}/100. Stored on blockchain."
    elif status == "NEEDS_REVIEW":
        return f"Proof needs review ⚠️ — Score {score}/100. Manual assessment required."
    else:
        return f"Proof suspicious ❌ — Score {score}/100. Flagged for fraud investigation."


def generate_blockchain_note(hash_str: str, proof_id: str) -> str:
    """Generate the blockchain storage confirmation note."""
    return (
        f"🔗 **On-Chain Record Created**\n\n"
        f"The SHA-256 hash of this proof has been written to the verification ledger.\n\n"
        f"- **Proof ID**: `{proof_id}`\n"
        f"- **Hash**: `{hash_str[:32]}...`\n"
        f"- **Immutability**: This record cannot be altered or deleted.\n"
        f"- **Verification**: Anyone can verify this proof using the hash in the Verification Portal."
    )
