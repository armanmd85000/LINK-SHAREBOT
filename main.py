import asyncio
from bot import Bot

bot = Bot()

async def main():
    await bot.start()
    await asyncio.Event().wait()  # keep bot alive forever

if __name__ == "__main__":
    asyncio.run(main())
