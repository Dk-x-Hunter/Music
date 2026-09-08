from pyrogram import Client, filters
from pytgcalls.types import AudioQuality, MediaStream

from client import call


@Client.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply_text(
            "🎵 Usage:\n/play <YouTube URL>"
        )
        return

    url = message.command[1]

    msg = await message.reply_text("🎧 Starting playback...")

    try:
        await call.play(
            message.chat.id,
            MediaStream(
                url,
                AudioQuality.HIGH,
                ytdlp_parameters="--no-playlist",
            ),
        )

        await msg.edit_text(
            f"🎵 **Now Playing**\n\n🔗 `{url}`"
        )

    except Exception as e:
        print(f"Playback error: {e}")
        await msg.edit_text(
            f"❌ **Playback failed**\n\n`{e}`"
        )


@Client.on_message(filters.command("pause"))
async def pause(_, message):
    try:
        await call.pause(message.chat.id)
        await message.reply_text("⏸️ Music paused.")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


@Client.on_message(filters.command("resume"))
async def resume(_, message):
    try:
        await call.resume(message.chat.id)
        await message.reply_text("▶️ Music resumed.")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


@Client.on_message(filters.command("stop"))
async def stop(_, message):
    try:
        await call.leave_call(message.chat.id)
        await message.reply_text(
            "⏹️ Music stopped.\n👋 Left the voice chat."
        )
    except Exception as e:
        await message.reply_text(f"❌ {e}")