"""
config/settings.py
Central configuration — edit this file to change pins, timing, and GitHub details.
"""

from pathlib import Path

# ── GPIO pin numbers (BCM numbering) ──────────────────────────────────────────
MOTION_PIN = 17          # PIR motion sensor digital output
AUDIO_PIN  = 27          # Sound/audio sensor digital output
DHT_PIN    = 4           # DHT22 data pin (also set on board.D4)

# ── Sampling ───────────────────────────────────────────────────────────────────
SAMPLE_INTERVAL_SEC = 30 * 60   # 30 minutes
TOTAL_SAMPLES       = 48        # 48 × 30 min = 24 hours (adjust as needed)

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR     = PROJECT_ROOT / "data-test"
LOG_DIR      = PROJECT_ROOT / "logs-test"

# ── GitHub ─────────────────────────────────────────────────────────────────────
# Set these as environment variables or fill them in directly (not recommended for secrets).
GITHUB_TOKEN  = ""   # or set env var GITHUB_TOKEN
GITHUB_USER   = ""   # e.g. "your-username"
GITHUB_REPO   = ""   # e.g. "rpi-sensor-data"
GITHUB_BRANCH = "main"
GITHUB_REMOTE_PATH = "data-test/"  # folder inside the repo where CSVs are stored