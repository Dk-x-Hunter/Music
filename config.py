

import os
from dotenv import load_dotenv

load_dotenv()


def get_int(name: str, default: int = 0) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{name} must be a number")


def get_int_list(name: str) -> list[int]:
    value = os.getenv(name, "").strip()

    if not value:
        return []

    result = []

    for item in value.split(","):
        item = item.strip()

        if item:
            try:
                result.append(int(item))
            except ValueError:
                raise ValueError(
                    f"{name} contains an invalid ID: {item}"
                )

    return result


# =========================
# Telegram
# =========================

API_ID = get_int("API_ID")
API_HASH = os.getenv("API_HASH", "").strip()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Pyrogram/Telethon assistant session string
ASSISTANT_SESSION = os.getenv("ASSISTANT_SESSION", "").strip()


# =========================
# Users
# =========================

OWNER_ID = get_int("OWNER_ID")

# Example:
# SUDO_USERS=123456789,987654321
SUDO_USERS = get_int_list("SUDO_USERS")


# =========================
# YouTube
# =========================

# Raw cookies URL
COOKIES_URL = os.getenv("COOKIES_URL", "").strip()


# =========================
# MongoDB (OPTIONAL)
# =========================

MONGO_URI = os.getenv("MONGO_URI", "").strip()

# MongoDB is optional.
MONGO_ENABLED = bool(MONGO_URI)


# =========================
# Logging
# =========================

LOGGER_ID = get_int("LOGGER_ID", 0)


# =========================
# Bot settings
# =========================

BOT_NAME = os.getenv("BOT_NAME", "Music Bot").strip()

DEFAULT_VOLUME = get_int("DEFAULT_VOLUME", 100)

MAX_QUEUE_SIZE = get_int("MAX_QUEUE_SIZE", 50)


# =========================
# Validation
# =========================

if not API_ID:
    raise ValueError("API_ID is missing")

if not API_HASH:
    raise ValueError("API_HASH is missing")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

if not ASSISTANT_SESSION:
    raise ValueError("ASSISTANT_SESSION is missing")

if not OWNER_ID:
    raise ValueError("OWNER_ID is missing")