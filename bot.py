from client import app, call


async def main():
    print("🎵 Music Bot is starting...")

    await app.start()
    await call.start()

    me = await app.get_me()

    print(f"✅ Bot started: @{me.username}")
    print("🎧 PyTgCalls started")
    print("🚀 Music bot is running...")

    await app.idle()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())