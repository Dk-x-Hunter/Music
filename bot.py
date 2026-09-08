import asyncio

from pyrogram import idle

from client import app, user, call


async def main():
    print("🎵 Starting Music Bot...")

    # Start bot account
    await app.start()
    print("🤖 Bot started")

    # Start user account
    await user.start()
    print("👤 User account started")

    # Start PyTgCalls
    await call.start()
    print("🎧 Voice Chat client started")

    me = await app.get_me()
    print(f"✅ Running as @{me.username or me.first_name}")

    # Keep everything running
    await idle()

    # Stop everything when the process exits
    await call.stop()
    await user.stop()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())