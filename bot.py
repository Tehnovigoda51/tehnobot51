import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "8538647250:AAHIWOTbXr_ocVepdl2MnSzZD3BfMErEUs0"

# ТВОЯ РАБОЧАЯ ССЫЛКА — GitHub Raw
PUBLIC_URL = "https://raw.githubusercontent.com/Tehnovigoda51/tehnobot51/main/tehno51.m3u"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>Tehno51 IPTV Бот</b>\n\n"
        "Используй /list для получения плейлиста."
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(
        f"📺 <b>Твой плейлист:</b>\n"
        f"<code>{PUBLIC_URL}</code>\n\n"
        f"⚡ Скопируй ссылку и открой в IPTV-плеере.",
        disable_web_page_preview=True
    )

async def main():
    logger.info("🚀 Бот Tehno51 запущен на PythonAnywhere!")
    logger.info(f"🔗 Ссылка: {PUBLIC_URL}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())