import os

from pyrogram import Client
import pyrogram.errors


# ─────────────────────────────────────────────
# PyTgCalls compatibility fix
# ─────────────────────────────────────────────

# Some PyTgCalls versions expect the old spelling
# "GroupcallForbidden", while newer Pyrogram versions
# use "GroupCallForbidden".

if not hasattr(pyrogram.errors, "GroupcallForbidden"):
    if hasattr(pyrogram.errors, "GroupCallForbidden"):
        pyrogram.errors.GroupcallForbidden = (
            pyrogram.errors.GroupCallForbidden
        )


# Import PyTgCalls AFTER the compatibility fix
from pytgcalls import PyTgCalls


# ─────────────────────────────────────────────
# Environment variables
# ─────────────────────────────────────────────

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")


# ─────────────────────────────────────────────
# Validate configuration
# ─────────────────────────────────────────────

if not API_ID:
    raise RuntimeError("❌ API_ID is missing")

if not API_HASH:
    raise RuntimeError("❌ API_HASH is missing")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN is missing")

if not SESSION_STRING:
    raise RuntimeError("❌ SESSION_STRING is missing")


# ─────────────────────────────────────────────
# Smart Plugins
# ─────────────────────────────────────────────

plugins = {
    "root": "plugins"
}


# ─────────────────────────────────────────────
# Telegram Bot
# ─────────────────────────────────────────────

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins
)


# ─────────────────────────────────────────────
# Telegram User Account
# ─────────────────────────────────────────────

user = Client(
    "music_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


# ─────────────────────────────────────────────
# Voice Chat client
# ─────────────────────────────────────────────

call = PyTgCalls(user)