import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

BOT_TOKEN = "8538647250:AAHIWOTbXr_ocVepdl2MnSzZD3BfMErEUs0"

# ===== ТВОЯ НОВАЯ КОРОТКАЯ ССЫЛКА =====
PUBLIC_URL = "https://tehnobot51.onrender.com/iptv.m3u"
# =======================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>Tehno51 IPTV Бот</b>\n\n"
        "Используй /list для получения плейлиста.\n"
        "📺 Короткая ссылка — легко вводить в пульте!"
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(
        f"📺 <b>Твой IPTV плейлист:</b>\n"
        f"<code>{PUBLIC_URL}</code>\n\n"
        f"⚡ Скопируй ссылку и открой в IPTV-плеере.",
        disable_web_page_preview=True
    )

# ===== ВЕБ-СЕРВЕР ДЛЯ RENDER =====
async def handle_port(request):
    return web.Response(text="✅ Tehno51 Bot is running")

async def handle_iptv(request):
    # Перенаправляем на реальный плейлист в GitHub
    return web.Response(
        text="https://raw.githubusercontent.com/Tehnovigoda51/tehnobot51/main/tehno51.m3u",
        content_type="text/plain"
    )

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_port)
    app.router.add_get('/health', handle_port)
    app.router.add_get('/iptv.m3u', handle_iptv)  # Короткая ссылка
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Web server started on port {port}")
    logger.info(f"🔗 Короткая ссылка: https://tehnobot51.onrender.com/iptv.m3u")

async def main():
    await start_web_server()
    logger.info("🚀 Бот Tehno51 запущен на Render!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
