import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *
from plugins import web_server
from aiohttp import web
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1002449417637

name = """
Link share bot started ✨ Credit:- @RexBots_Official
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.uptime = datetime.now()
        self.username = me.username

        # Restart notification
        try:
            await self.send_photo(
                chat_id=DATABASE_CHANNEL,
                photo="https://i.ibb.co/DH3N4Lyr/image.jpg",
                caption="**I ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ !**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/RexBots_Official")]]
                )
            )
        except Exception as e:
            self.LOGGER(__name__).warning(f"Restart message failed: {e}")

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info("Bot started successfully")
        self.LOGGER(__name__).info(name)

        # Start aiohttp web server
        try:
            runner = web.AppRunner(await web_server())
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", int(PORT))
            await site.start()
            self.LOGGER(__name__).info(f"Web server running on port {PORT}")
        except Exception as e:
            self.LOGGER(__name__).error(f"Web server error: {e}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped")
