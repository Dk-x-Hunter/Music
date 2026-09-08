import asyncio
import os
import subprocess
import uuid

from pyrogram import filters
from pytgcalls import idle
from pytgcalls.types import MediaStream


# Import the clients
from client import app, call


# Store the current stream for each chat
active_streams = {}


async def download_audio(url: str):
    """
    Download audio using yt-dlp and return the local file path.
    """

    os.makedirs("downloads", exist_ok=True)

    filename = f"downloads/{uuid.uuid4()}.%(ext)s"

    process = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-x",
        "--audio-format",
        "mp3",
        "-o",
        filename,
        url,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(stderr.decode(errors="ignore"))
        return None

    base = filename.replace(".%(ext)s", ".mp3")

    if os.path.exists(base):
        return base

    return None


@app.on_message(filters.command("play"))
async def play(_, message):

    if len(message.command) < 2:
        await message.reply_text(
            "🎵 Usage:\n/play <YouTube URL>"
        )
        return

    chat_id = message.chat.id
    url = message.command[1]

    msg = await message.reply_text("🔎 Downloading audio...")

    file_path = await download_audio(url)

    if not file_path:
        await msg.edit_text("❌ Failed to download audio.")
        return

    try:
        await call.play(
            chat_id,
            MediaStream(
                file_path,
                audio_parameters=MediaStream.AudioQuality.HIGH,
            ),
        )

        active_streams[chat_id] = file_path

        await msg.edit_text(
            "🎵 **Now Playing**\n\n"
            f"🔗 `{url}`"
        )

    except Exception as e:
        print(e)
        await msg.edit_text(
            f"❌ Playback error:\n`{e}`"
        )


@app.on_message(filters.command("pause"))
async def pause(_, message):

    try:
        await call.pause(message.chat.id)

        await message.reply_text(
            "⏸️ Music paused."
        )

    except Exception as e:
        await message.reply_text(
            f"❌ {e}"
        )


@app.on_message(filters.command("resume"))
async def resume(_, message):

    try:
        await call.resume(message.chat.id)

        await message.reply_text(
            "▶️ Music resumed."
        )

    except Exception as e:
        await message.reply_text(
            f"❌ {e}"
        )


@app.on_message(filters.command("stop"))
async def stop(_, message):

    chat_id = message.chat.id

    try:
        await call.leave_call(chat_id)

        file_path = active_streams.pop(chat_id, None)

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        await message.reply_text(
            "⏹️ Music stopped and I left the voice chat."
        )

    except Exception as e:
        await message.reply_text(
            f"❌ {e}"
        )