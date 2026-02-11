import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

BOT_TOKEN = "8538647250:AAHIWOTbXr_ocVepdl2MnSzZD3BfMErEUs0"
PUBLIC_URL = "https://tehnobot51.onrender.com/iptv.m3u"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ============ БАЗА СЕРВИСНЫХ ЦЕНТРОВ ============
SERVICE_CENTERS = {
    "lg": [{
        "brand": "📺 LG",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр LG"
    }],
    "haier": [{
        "brand": "❄️ Haier",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Haier"
    }],
    "samsung": [{
        "brand": "📱 Samsung",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Samsung"
    }],
    "lenovo": [{
        "brand": "💻 Lenovo",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Lenovo"
    }],
    "beko": [{
        "brand": "🔵 Beko",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Beko"
    }],
    "indesit": [{
        "brand": "🔵 Indesit",
        "name": "Indesit",
        "address": "Горячая линия производителя",
        "phone": "+7 (800) 333-38-87",
        "hours": "Пн-Чт 7:00-18:00, Пт 7:00-17:00, Сб-Вс 9:00-17:00",
        "services": "Авторизованный сервисный центр Indesit"
    }],
    "gefest": [{
        "brand": "🔥 Gefest",
        "name": "АСЦ Сармат Сервис",
        "address": "ул. Бабушкина, 88а",
        "phone": "+7 (927) 588-82-58",
        "hours": "Пн-Вс 8:00-20:00",
        "services": "Сервисный центр Gefest"
    }],
    "philips": [{
        "brand": "💡 Philips",
        "name": "Элком",
        "address": "ул. Савушкина, 51А",
        "phone": "+7 (800) 220-00-04",
        "hours": "Пн-Сб 09:00-15:00",
        "services": "Сервисный центр Philips"
    }],
    "tcl": [{
        "brand": "📺 TCL",
        "name": "TCL.COM",
        "address": "Горячая линия производителя",
        "phone": "+7 (800) 100-80-80",
        "hours": "8:00-21:00",
        "services": "Сервисный центр TCL"
    }],
    "hiberg": [{
        "brand": "🔧 Hiberg",
        "name": "ИП Типаков Владимир Иванович",
        "address": "ул. Рождественского, 15В",
        "phone": "+7 (8512) 454-674",
        "hours": "Пн-Пт 09:00-18:00",
        "services": "Сервисный центр Hiberg"
    }],
    "centek": [{
        "brand": "🔧 Centek",
        "name": "СЦ Энергия",
        "address": "ул. Ботвина, 6А/1",
        "phone": "+7 (8512) 200-545",
        "hours": "Пн-Пт 09:00-17:30",
        "services": "Сервисный центр Centek"
    }]
}
# ==============================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>ТЕХНОВЫГОДА — Сервисный помощник</b>\n\n"
        "📺 IPTV: /list\n"
        "🔧 Сервисы: /service [бренд]\n\n"
        "✅ /service lg\n"
        "✅ /service haier\n"
        "✅ /service samsung"
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(f"📺 <b>IPTV плейлист:</b>\n<code>{PUBLIC_URL}</code>")

@dp.message(Command("service"))
async def cmd_service(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        brands = "• " + "\n• ".join(SERVICE_CENTERS.keys())
        await message.answer(f"🔧 <b>Бренды:</b>\n{brands}\n\nПример: /service lg")
        return
    
    query = args[1].strip().lower()
    centers = SERVICE_CENTERS.get(query, [])
    
    if centers:
        text = f"🔧 <b>{centers[0]['brand']}</b>\n📍 {centers[0]['address']}\n📞 {centers[0]['phone']}\n🕒 {centers[0]['hours']}\n🛠 {centers[0]['services']}"
        await message.answer(text)
    else:
        await message.answer(f"❌ Бренд «{query}» не найден")

async def handle_iptv(request):
    url = "https://raw.githubusercontent.com/Tehnovigoda51/tehnobot51/main/tehno51.m3u"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return web.Response(text=await resp.text(), content_type='audio/x-mpegurl')

async def start_web_server():
    app = web.Application()
    app.router.add_get('/iptv.m3u', handle_iptv)
    app.router.add_get('/', lambda r: web.Response(text="OK"))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 10000))).start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
