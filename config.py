import os

# =========================
# Required configuration
# =========================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# =========================
# Ownership / access control
# =========================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Comma-separated Telegram user IDs
# Example: SUDO_USERS="123456789,987654321"
SUDO_USERS = [
    int(user_id.strip())
    for user_id in os.getenv("SUDO_USERS", "").split(",")
    if user_id.strip()
]

# =========================
# Storage
# =========================

DB_FILE = os.path.join(
    os.path.dirname(__file__),
    "data.json"
)

# =========================
# Clone system
# =========================

CLONE_ONLY_OWNER = os.getenv(
    "CLONE_ONLY_OWNER",
    "true"
).lower() == "true"


# =========================
# Configuration validation
# =========================

required_values = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "SESSION_STRING": SESSION_STRING,
    "OWNER_ID": OWNER_ID,
}

missing = [
    name for name, value in required_values.items()
    if not value
]

if missing:
    raise RuntimeError(
        "Missing required environment variables: "
        + ", ".join(missing)
    )