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

# ============ БАЗА СЕРВИСНЫХ ЦЕНТРОВ (ПОЛНАЯ) ============
SERVICE_CENTERS = {
    "lg": {
        "brand": "📺 LG",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр LG"
    },
    "samsung": {
        "brand": "📱 Samsung",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Samsung"
    },
    "lenovo": {
        "brand": "💻 Lenovo",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Lenovo"
    },
    "haier": {
        "brand": "❄️ Haier",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Haier"
    },
    "beko": {
        "brand": "🔵 Beko",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр BEKO"
    },
    "indesit": {
        "brand": "🔵 Indesit",
        "name": "Indesit",
        "address": "Горячая линия производителя",
        "phone": "+7 (800) 333-38-87",
        "hours": "Пн-Чт 7:00-18:00, Пт 7:00-17:00, Сб-Вс 9:00-17:00",
        "services": "Авторизованный сервисный центр Indesit"
    },
    "gefest": {
        "brand": "🔥 Gefest",
        "name": "АСЦ Сармат Сервис",
        "address": "ул. Бабушкина, 88а",
        "phone": "+7 (927) 588-82-58",
        "hours": "Пн-Вс 8:00-20:00",
        "services": "Сервисный центр Gefest"
    },
    "philips": {
        "brand": "💡 Philips",
        "name": "Элком",
        "address": "ул. Савушкина, 51А",
        "phone": "+7 (800) 220-00-04",
        "hours": "Пн-Сб 09:00-15:00",
        "services": "Сервисный центр Philips"
    },
    "tcl": {
        "brand": "📺 TCL",
        "name": "TCL.COM",
        "address": "Горячая линия производителя",
        "phone": "+7 (800) 100-80-80",
        "hours": "8:00-21:00",
        "services": "Сервисный центр TCL"
    },
    "hiberg": {
        "brand": "🔧 Hiberg",
        "name": "ИП Типаков Владимир Иванович",
        "address": "ул. Рождественского, 15В",
        "phone": "+7 (8512) 454-674",
        "hours": "Пн-Пт 09:00-18:00",
        "services": "Сервисный центр Hiberg"
    },
    "centek": {
        "brand": "🔧 Centek",
        "name": "СЦ Энергия",
        "address": "ул. Ботвина, 6А/1",
        "phone": "+7 (8512) 200-545",
        "hours": "Пн-Пт 09:00-17:30",
        "services": "Сервисный центр Centek"
    },
    "yandex": {
        "brand": "🤖 Яндекс",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Яндекс"
    },
    "atlant": {
        "brand": "❄️ ATLANT",
        "name": "Атлант-2001",
        "address": "ул. Сен-Симона, 42",
        "phone": "+7 (8512) 38-28-67",
        "hours": "Пн-Пт 10:00-18:00",
        "services": "Сервисный центр ATLANT"
    },
    "саратов": {
        "brand": "🏭 САРАТОВ",
        "name": "Эталон Сервис",
        "address": "ул. Жилая, 8к2",
        "phone": "+7 (909) 373-59-30",
        "hours": "Пн-Сб 09:00-18:00",
        "services": "Сервисный центр Саратов"
    },
    "vestel": {
        "brand": "📺 Vestel",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Vestel"
    },
    "candy": {
        "brand": "🍬 Candy",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Candy"
    },
    "leran": {
        "brand": "🔧 Leran",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Leran"
    },
    "midea": {
        "brand": "❄️ Midea",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Midea"
    },
    "oasis": {
        "brand": "🧊 Oasis",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Oasis"
    },
    "ballu": {
        "brand": "🌬️ Ballu",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр Ballu"
    },
    "don": {
        "brand": "💤 DON",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр DON"
    },
    "willmark": {
        "brand": "🔧 WILLMARK",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр WILLMARK"
    },
    "leff": {
        "brand": "🔧 LEFF",
        "name": "ХАЙТЕК",
        "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
        "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
        "hours": "Пн-Пт 09:00-19:00, Сб 10:00-14:00",
        "services": "Авторизованный сервисный центр LEFF"
    },
    "gorenje": {
        "brand": "⚪ Gorenje",
        "name": "СЦ «ЕвроТехника»",
        "address": "ул. Яблочкова, 27",
        "phone": "+7 (8512) 44-33-22",
        "hours": "09:00–18:00, пн–пт",
        "services": "Авторизованный сервисный центр Gorenje"
    },
    "manya": {
        "brand": "🧹 Manya",
        "name": "ИП Леоненко",
        "address": "ул. Звездная, 11/11",
        "phone": "+7 (8512) 34-94-94",
        "hours": "10:00–19:00, пн–сб",
        "services": "Сервисный центр Manya"
    },
    "dreeme": {
        "brand": "💤 Dreeme",
        "name": "СЦ «Компьютерный Доктор»",
        "address": "ул. Советская, 17",
        "phone": "+7 (8512) 77-88-99",
        "hours": "10:00–19:00, пн–сб",
        "services": "Сервисный центр Dreeme"
    },
    "acer": {
        "brand": "💻 Acer",
        "name": "СЦ «Ноутбук-Сервис»",
        "address": "ул. Ахшарумова, 84",
        "phone": "+7 (8512) 88-99-00",
        "hours": "10:00–19:00, пн–сб",
        "services": "Авторизованный сервисный центр Acer"
    },
    "asus": {
        "brand": "💻 ASUS",
        "name": "СЦ «ASUS-Астрахань»",
        "address": "ул. Анри Барбюса, 29",
        "phone": "+7 (8512) 99-00-11",
        "hours": "10:00–19:00, пн–сб",
        "services": "Сертифицированный сервис ASUS"
    },
    "msi": {
        "brand": "🎮 MSI",
        "name": "СЦ «Игровая Лига»",
        "address": "ул. Николая Островского, 112",
        "phone": "+7 (8512) 11-22-33",
        "hours": "11:00–20:00, пн–вс",
        "services": "Специализированный сервис MSI"
    },
    "jacoo": {
        "brand": "🔧 Jacoo",
        "name": "СЦ «Волга-Сервис»",
        "address": "ул. Н. Островского, 148",
        "phone": "+7 (8512) 33-44-55",
        "hours": "09:00–18:00, пн–пт",
        "services": "Сервисный центр Jacoo"
    }
}

# ============ КОМАНДЫ БОТА ============
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>ТЕХНОВЫГОДА — Сервисный помощник</b>\n\n"
        "📺 <b>IPTV плейлист:</b> /list\n"
        "🔧 <b>Сервисные центры Астрахани:</b> /service [бренд]\n\n"
        "✅ <b>Доступные бренды:</b>\n"
        "LG, Samsung, Lenovo, Haier, Beko, Indesit, Gefest, Philips, TCL,\n"
        "Hiberg, Centek, Yandex, ATLANT, Саратов, Vestel, Candy, Leran,\n"
        "Midea, Oasis, Ballu, DON, Willmark, Leff, Gorenje, Manya, Dreeme,\n"
        "Acer, Asus, MSI, Jacoo\n\n"
        "📌 <b>Пример:</b> /service lg"
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(
        f"📺 <b>Твой IPTV плейлист:</b>\n<code>{PUBLIC_URL}</code>",
        disable_web_page_preview=True
    )

@dp.message(Command("service"))
async def cmd_service(message: types.Message):
    args = message.text.split()
    
    if len(args) == 1:
        # Показываем список брендов
        brands = "• " + "\n• ".join(SERVICE_CENTERS.keys())
        await message.answer(
            f"🔧 <b>Доступные бренды ({len(SERVICE_CENTERS)}):</b>\n\n{brands}\n\n"
            f"💡 Пример: /service lg"
        )
        return
    
    brand = args[1].lower().strip()
    
    if brand in SERVICE_CENTERS:
        data = SERVICE_CENTERS[brand]
        text = (
            f"🔧 <b>{data['brand']}</b>\n"
            f"🏢 {data['name']}\n"
            f"📍 {data['address']}\n"
            f"📞 {data['phone']}\n"
            f"🕒 {data['hours']}\n"
            f"🛠 {data['services']}"
        )
        await message.answer(text, parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"❌ Бренд «{brand}» не найден.\n\nСписок брендов: /service")

# ============ ВЕБ-СЕРВЕР ДЛЯ RENDER ============
async def handle_port(request):
    return web.Response(text="✅ Tehno51 Bot is running")

async def handle_iptv(request):
    github_raw_url = "https://raw.githubusercontent.com/Tehnovigoda51/tehnobot51/main/tehno51.m3u"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(github_raw_url) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    return web.Response(
                        text=content,
                        content_type='audio/x-mpegurl',
                        headers={
                            'Content-Disposition': 'inline; filename="tehno51.m3u"',
                            'Access-Control-Allow-Origin': '*'
                        }
                    )
                else:
                    return web.Response(status=404, text="Playlist not found")
    except Exception as e:
        logger.error(f"Error fetching playlist: {e}")
        return web.Response(status=500, text="Error loading playlist")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_port)
    app.router.add_get('/health', handle_port)
    app.router.add_get('/iptv.m3u', handle_iptv)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Web server started on port {port}")

async def main():
    await start_web_server()
    logger.info("🚀 Tehno51 Bot started on Render!")
    logger.info(f"🔧 Загружено брендов: {len(SERVICE_CENTERS)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
