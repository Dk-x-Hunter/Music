import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Telegram User Session String
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Your Telegram user ID
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


# Basic validation
if not API_ID:
    raise RuntimeError("API_ID is missing")

if not API_HASH:
    raise RuntimeError("API_HASH is missing")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not SESSION_STRING:
    raise RuntimeError("SESSION_STRING is missing")

if not OWNER_ID:
    raise RuntimeError("OWNER_ID is missing")