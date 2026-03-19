# ⛓️ Proof-of-Reality (PoR)
### AI + Blockchain Powered Truth Verification System

> *"If it's not verified and on-chain, it cannot be trusted."*

---

## 🌐 What is Proof-of-Reality?

**Proof-of-Reality** is a hackathon-ready, end-to-end trust verification system that combines AI-powered image forensics with a simulated immutable blockchain ledger. It solves the global **fake data crisis** — fake insurance claims, fake medical records, fake resumes — by creating a cryptographic paper trail for every submitted proof.

**Primary Demo Use Case: Insurance Claim Verification**

Upload an accident photo → AI validates authenticity → SHA-256 hash stored on-chain → Insurer verifies via portal.

---
## ▶️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Open in Browser

[Proof-of-Reality](https://proof-of-reality.streamlit.app/)
```
## 🎯 The Problem

Fake data exists everywhere:
- 🚗 Fake insurance claims
- 🎓 Fake internship certificates
- 🏥 Fake medical records
- 📦 Fake supply chain documents
- 📰 Fake media / deepfakes

**PoR solves this with a 3-layer trust architecture:**
1. **AI Validation** — Image forensics, tampering detection, metadata checks
2. **LLM Reasoning** — Human-readable explanation of why a proof passes or fails
3. **Blockchain Storage** — Immutable SHA-256 hash ledger, searchable by anyone

---

## 🏗️ System Architecture

User Upload
    ↓
AI Validation Engine (OpenCV + Heuristics)
    ↓
LLM Reasoning Layer (Rule-based explanation)
    ↓
Authenticity Score (0–100%) + Status
    ↓
SHA-256 Hash Generation
    ↓
Blockchain Storage (simulated ledger)
    ↓
Trust Score Update
    ↓
Dashboard + Verification Portal


---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (multi-page, custom CSS glassmorphism) |
| Backend | Python 3.10+ |
| AI/CV | OpenCV, Pillow |
| LLM | Rule-based reasoning engine (simulates LLM) |
| Blockchain | Simulated SHA-256 ledger (JSON-based, chain-linked) |
| Hashing | Python `hashlib` — SHA-256 |
| Storage | JSON files (no database required) |
| Charts | Matplotlib, Seaborn |
| Fonts | Orbitron, Space Grotesk, JetBrains Mono |

---

## 🗂️ Project Structure


proof_of_reality/
├── app.py                    # Main entry point + router + navbar
│
├── pages/
│   ├── landing.py            # Landing page (hero + features + CTA)
│   ├── dashboard.py          # User dashboard (trust score, recent proofs)
│   ├── upload_verify.py      # Proof upload + validation pipeline
│   ├── verification.py       # Public verification portal (search by hash)
│   ├── analytics.py          # Charts and fraud detection analytics
│   └── settings.py           # Theme toggle, account, data management
│
├── modules/
│   ├── ai_validator.py       # AI image forensics engine
│   ├── llm_reasoning.py      # LLM-style explanation generator
│   ├── hash_generator.py     # SHA-256 hashing utilities
│   ├── blockchain.py         # Simulated blockchain (chain-linked blocks)
│   └── trust_score.py        # User trust score system
│
├── auth/
│   ├── login.py              # Login form + session handling
│   └── signup.py             # Signup form + user creation
│
├── analytics/
│   ├── tracker.py            # Stats aggregation
│   └── charts.py             # Matplotlib/Seaborn chart generators
│
├── utils/
│   ├── helpers.py            # JSON I/O, data helpers
│   └── theme.py              # CSS injection, dark/light mode, UI components
│
├── data/
│   ├── records.json          # Proof records ledger
│   ├── users.json            # User accounts
│   └── blockchain.json       # Blockchain (auto-created on first run)
│
├── requirements.txt
└── README.md
```

---

---

## 🔐 Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| `demo_user` | `demo1234` | Primary demo account |
| `alice_smith` | `alice123` | High-trust user |
| `bob_jones` | `bob12345` | Mixed record user |

Or click **"🚀 Demo Login"** on the login screen for instant access.

---

## 🎬 Demo Walkthrough

### Scenario 1: Real Proof ✅
1. Login as `demo_user`
2. Go to **Submit Proof**
3. Click **"📋 Demo: Real Proof"**
4. Watch the pipeline: AI analysis → hash generation → blockchain storage
5. See: High authenticity score, VERIFIED status, trust score increase

### Scenario 2: Fake Proof ❌
1. Stay logged in
2. Click **"🧪 Demo: Fake Proof"**
3. Observe: Low authenticity score, SUSPICIOUS status, trust score decrease
4. Read the AI reasoning explaining why it was flagged

### Scenario 3: Verify by Hash
1. Go to **Verification Portal**
2. Click any quick-verify button (POR-001, POR-002, etc.)
3. See full proof details, blockchain record, and status

---

## 🤖 AI Validation Engine

The AI engine performs:

| Check | Method | Output |
|-------|--------|--------|
| Tampering Detection | OpenCV Laplacian variance, channel noise analysis | Tampering probability (0–1) |
| Edge Analysis | Sharpness scoring | Edge anomaly flag |
| Color Analysis | Histogram spike detection | Color anomaly flag |
| EXIF Metadata | PIL ExifTags parsing | Software detection |
| Duplicate Check | SHA-256 hash comparison | Duplicate flag + original ID |
| Metadata Consistency | Timestamp + filename heuristics | Consistency score |

**Authenticity Score formula:**
```
base = 100
− tampering_probability × 60
− duplicate_penalty (30)
− metadata_issues × 20
− active_indicator_count × 5
= Authenticity Score (clamped 5–99)
```

---

## ⛓️ Blockchain Layer

Each verified proof creates a **Block** containing:
```json
{
  "index": 6,
  "proof_id": "POR-006",
  "proof_hash": "sha256_of_file+userid+timestamp",
  "user_id": "demo_user",
  "timestamp": "2024-06-01T10:23:45",
  "previous_hash": "hash_of_previous_block",
  "block_hash": "sha256_of_all_above_fields"
}
```

- **Immutable**: Once written, blocks cannot be edited
- **Chain-linked**: Each block references the previous block's hash
- **Verifiable**: Anyone can verify a hash using the Verification Portal
- **Integrity-checked**: Full chain validation on every analytics load

---

## ⭐ Trust Score System

| Action | Score Delta |
|--------|------------|
| Proof verified (score 90+) | +8 |
| Proof verified (score 80+) | +5 |
| Proof verified (score 75+) | +2 |
| Proof flagged suspicious (low) | −15 |
| Proof flagged suspicious (medium) | −10 |
| Proof needs review | +1 |

| Score Range | Level | Badge |
|-------------|-------|-------|
| 90–100 | ELITE | 🏆 |
| 75–89 | TRUSTED | ✅ |
| 55–74 | MODERATE | ⚡ |
| 35–54 | CAUTIOUS | ⚠️ |
| 0–34 | FLAGGED | 🚨 |

---

## 🎨 UI/UX Design

- **Theme**: Glassmorphism + crypto-inspired dark mode
- **Color palette**: Deep purple/black/blue gradients
- **Fonts**: Orbitron (display) + Space Grotesk (body) + JetBrains Mono (code)
- **Effects**: Floating orbs, glow borders, shimmer text, progress animations
- **Light mode**: White/lavender gradient with soft glass cards
- **Responsive**: Works on desktop and tablet

---

## 📊 Analytics Dashboard

- Donut chart: Verification distribution
- Fraud detection gauge (half-donut)
- Authenticity score bar chart (buckets)
- Trust score histogram
- Monthly trends (stacked bar)
- Per-user performance table
- Blockchain layer stats

---

## 🔧 Extending the Project

### Connect to Real Blockchain (Polygon Testnet)
Replace `modules/blockchain.py` storage with `web3.py`:
```python
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://rpc-mumbai.maticvigil.com"))
# Store hash in a simple smart contract
```

### Connect Real LLM
Replace `modules/llm_reasoning.py` with actual API call:
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(model="claude-opus-4-6", ...)
```

### Add HuggingFace Model
```python
from transformers import pipeline
detector = pipeline("image-classification", model="umm-maybe/AI-image-detector")
```

---

## 🏆Pitch Points

1. **Real problem**: Insurance fraud costs $80B/year globally
2. **Working demo**: Upload → validate → blockchain in <3 seconds
3. **Clear differentiation**: AI reasoning layer explains every decision
4. **Scalable architecture**: Each layer is independently replaceable
5. **Trust layer vision**: Every domain with fake data can benefit

---

*Built with ⚡ for hackathon demo purposes. All blockchain operations are simulated locally.*
