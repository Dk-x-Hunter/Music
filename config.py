import os


def get_env(name: str, required: bool = True, default: str = "") -> str:
    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


# Telegram
API_ID = int(get_env("API_ID"))
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")

# Owner
OWNER_ID = int(get_env("OWNER_ID"))

# Pyrogram assistant account
SESSION_STRING = get_env("SESSION_STRING")

# MongoDB
MONGO_DB_URI = get_env("MONGO_DB_URI")

# Logging
LOGGER_ID = int(get_env("LOGGER_ID"))

# YouTube cookies
COOKIES_URL = get_env("COOKIES_URL", required=False)

# Database name
MONGO_DB_NAME = get_env(
    "MONGO_DB_NAME",
    required=False,
    default="TelegramMusicBot",
)