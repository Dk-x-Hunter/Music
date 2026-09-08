import os

from pyrogram import Client
from pytgcalls import PyTgCalls


API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")


if not API_ID or not API_HASH:
    raise RuntimeError("API_ID or API_HASH is missing")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")

if not SESSION_STRING:
    raise RuntimeError("SESSION_STRING is missing")


# Bot account
app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# User account used for voice chat
user = Client(
    "music_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

# PyTgCalls uses the user account
call = PyTgCalls(user)