import os

from pyrogram import Client
from pytgcalls import PyTgCalls


API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")


if not API_ID or not API_HASH or not BOT_TOKEN or not SESSION_STRING:
    raise RuntimeError(
        "Missing required environment variables: "
        "API_ID, API_HASH, BOT_TOKEN, SESSION_STRING"
    )


# Telegram bot
app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Telegram user account
user = Client(
    "music_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

# Voice-chat client
call = PyTgCalls(user)


async def start_clients():
    await app.start()
    await user.start()
    await call.start()


async def stop_clients():
    await call.stop()
    await user.stop()
    await app.stop()