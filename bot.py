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

# ============ ПОЛНАЯ БАЗА СЕРВИСНЫХ ЦЕНТРОВ ============
# ГОРОД: АСТРАХАНЬ
# ВСЕ БРЕНДЫ КОТОРЫЕ ТЫ ДОБАВИЛ
# ======================================================

SERVICE_CENTERS = {
    # === LG ===
    "lg": [
        {
            "brand": "📺 LG",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр LG"
        }
    ],
    
    # === Yandex ===
    "yandex": [
        {
            "brand": "🤖 Яндекс Бейсик",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Яндекс"
        }
    ],
    
    # === LENOVO ===
    "lenovo": [
        {
            "brand": "💻 Lenovo",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Lenovo"
        }
    ],
    
    # === Gefest ===
    "gefest": [
        {
            "brand": "🔥 Gefest",
            "name": "АСЦ Сармат Сервис",
            "address": "ул. Бабушкина, 88а",
            "phone": "+7 (927) 588-82-58",
            "hours": "ПН – ВС: 8:00 – 20:00",
            "services": "Сервисный центр Gefest"
        }
    ],
    
    # === ATLANT ===
    "atlant": [
        {
            "brand": "❄️ ATLANT",
            "name": "Атлант-2001",
            "address": "ул. Сен-Симона, 42",
            "phone": "+7 (8512) 38-28-67",
            "hours": "Пн — Пт 10:00–18:00, Сб — Вс выходной",
            "services": "Сервисный центр ATLANT"
        }
    ],
    
    # === САРАТОВ ===
    "саратов": [
        {
            "brand": "🏭 САРАТОВ",
            "name": "Эталон Сервис",
            "address": "ул. Жилая, д. 8к2",
            "phone": "+7 (909) 373-59-30",
            "hours": "будни 09:00–18:00, суббота 09:00–18:00",
            "services": "Сервисный центр Саратов"
        }
    ],
    
    # === PHILIPS ===
    "philips": [
        {
            "brand": "💡 Philips",
            "name": "Элком",
            "address": "ул. Савушкина, 51А",
            "phone": "+7 (800) 220-00-04",
            "hours": "ПН - СБ: 09:00 - 15:00, ВС: выходной",
            "services": "Сервисный центр Philips"
        }
    ],
    
    # === BEKO ===
    "beko": [
        {
            "brand": "🔵 Beko",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр BEKO"
        }
    ],
    
    # === INDESIT ===
    "indesit": [
        {
            "brand": "🔵 Indesit",
            "name": "Indesit",
            "address": "Горячая линия производителя",
            "phone": "+7 (800) 333-38-87",
            "hours": "Пн-Чт 7:00-18:00, Пт 7:00-17:00, Сб-Вс 9:00-17:00",
            "services": "Авторизованный сервисный центр Indesit"
        }
    ],
    
    # === Vestel ===
    "vestel": [
        {
            "brand": "📺 Vestel",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Vestel"
        }
    ],
    
    # === TCL ===
    "tcl": [
        {
            "brand": "📺 TCL",
            "name": "TCL.COM",
            "address": "Горячая линия производителя",
            "phone": "+7 (800) 100-80-80",
            "hours": "Ежедневно с 8:00 до 21:00",
            "services": "Сервисный центр TCL"
        }
    ],
    
    # === CANDY ===
    "candy": [
        {
            "brand": "🍬 Candy",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Candy"
        }
    ],
    
    # === HAIER ===
    "haier": [
        {
            "brand": "❄️ Haier",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Haier"
        }
    ],
    
    # === LERAN ===
    "leran": [
        {
            "brand": "🔧 Leran",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Leran"
        }
    ],
    
    # === MIDEA ===
    "midea": [
        {
            "brand": "❄️ Midea",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Midea"
        }
    ],
    
    # === OASIS ===
    "oasis": [
        {
            "brand": "🧊 Oasis",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Oasis"
        }
    ],
    
    # === Ballu ===
    "ballu": [
        {
            "brand": "🌬️ Ballu",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Ballu"
        }
    ],
    
    # === DON ===
    "don": [
        {
            "brand": "💤 DON",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр DON"
        }
    ],
    
    # === HIBERG ===
    "hiberg": [
        {
            "brand": "🔧 Hiberg",
            "name": "ИП Типаков Владимир Иванович",
            "address": "ул. Рождественского, д. 15В",
            "phone": "+7 (8512) 454-674",
            "hours": "Пн — Пт 09:00–18:00",
            "services": "Сервисный центр Hiberg"
        }
    ],
    
    # === WILLMARK ===
    "willmark": [
        {
            "brand": "🔧 WILLMARK",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр WILLMARK"
        }
    ],
    
    # === LEFF ===
    "leff": [
        {
            "brand": "🔧 LEFF",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр LEFF"
        }
    ],
    
    # === CENTEK ===
    "centek": [
        {
            "brand": "🔧 Centek",
            "name": "СЦ Энергия",
            "address": "ул. Ботвина, д. 6А/1",
            "phone": "+7 (8512) 200-545",
            "hours": "Пн — Пт 09:00–17:30",
            "services": "Сервисный центр Centek"
        }
    ],
    
    # === SAMSUNG (ДОБАВЛЯЕМ ЯВНО) ===
    "samsung": [
        {
            "brand": "📱 Samsung",
            "name": "ХАЙТЕК",
            "address": "ул. Ташкентская, 13А и ул. Звездная, 7/4",
            "phone": "+7 (8512) 23-83-10, +7 (8512) 23-83-11",
            "hours": "Пн - Пт с 09:00 до 19:00, Сб с 10:00 до 14:00",
            "services": "Авторизованный сервисный центр Samsung"
        }
    ],
    
    # === АЛИАСЫ (СИНОНИМЫ) ===
    "iphone": "lg",
    "macbook": "lenovo",
    "телевизор": "lg",
    "холодильник": "lg",
    "стиральная": "samsung",
    "ноутбук": "lenovo",
    "кондиционер": "lg",
    "айфон": "lg",
    "макбук": "lenovo",
    "самсунг": "samsung",
    "лг": "lg",
    "леново": "lenovo"
}

# ============ ФУНКЦИИ ПОИСКА ============
def find_service_centers(query: str):
    """Поиск сервисных центров по запросу"""
    query = query.lower().strip()
    
    # Прямое совпадение с ключом
    if query in SERVICE_CENTERS:
        data = SERVICE_CENTERS[query]
        if isinstance(data, str):
            # Если это алиас
            return SERVICE_CENTERS.get(data, [])
        return data
    
    # Поиск по вхождению
    results = []
    for key, centers in SERVICE_CENTERS.items():
        if query in key and not isinstance(centers, str):
            results.extend(centers)
    
    return results

def format_service_message(centers):
    """Форматирование списка сервисов в красивое сообщение"""
    if not centers:
        return "❌ Сервисные центры не найдены."
    
    lines = ["🔧 <b>НАЙДЕННЫЕ СЕРВИСНЫЕ ЦЕНТРЫ:</b>\n"]
    
    for i, center in enumerate(centers, 1):
        lines.append(f"\n<b>{i}. {center['brand']}</b> — {center['name']}")
        lines.append(f"📍 <b>Адрес:</b> {center['address']}")
        lines.append(f"📞 <b>Телефон:</b> {center['phone']}")
        lines.append(f"🕒 <b>Часы:</b> {center['hours']}")
        lines.append(f"🛠 <b>Услуги:</b> {center['services']}")
        lines.append("─" * 30)
    
    return "\n".join(lines)

# ============ КОМАНДЫ БОТА ============
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>ТЕХНОВЫГОДА — Сервисный помощник</b>\n\n"
        "📺 <b>IPTV плейлист:</b> /list\n"
        "🔧 <b>Сервисные центры Астрахани:</b> /service [бренд]\n\n"
        "🔍 <b>Примеры:</b>\n"
        "/service lg\n"
        "/service samsung\n"
        "/service haier\n"
        "/service centek\n\n"
        "📌 <i>База содержит более 20 брендов!</i>"
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(
        f"📺 <b>Твой IPTV плейлист:</b>\n<code>{PUBLIC_URL}</code>",
        disable_web_page_preview=True
    )

@dp.message(Command("service"))
async def cmd_service(message: types.Message):
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        # Показываем список всех брендов
        brands_list = "• " + "\n• ".join([k for k in SERVICE_CENTERS.keys() if not isinstance(SERVICE_CENTERS[k], str)])
        await message.answer(
            f"🔧 <b>Сервисные центры Астрахани</b>\n\n"
            f"📋 <b>Доступные бренды ({len([k for k in SERVICE_CENTERS.keys() if not isinstance(SERVICE_CENTERS[k], str)]))}:</b>\n"
            f"{brands_list}\n\n"
            f"💡 <b>Пример:</b> /service lg\n"
            f"📍 <i>Информация актуальна на 2026 год</i>"
        )
        return
    
    query = args[1].strip().lower()
    centers = find_service_centers(query)
    
    if centers:
        response = format_service_message(centers)
    else:
        response = f"❌ Сервисные центры для «{query}» не найдены.\n\nПроверь список брендов через /service"
    
    await message.answer(response, parse_mode=ParseMode.HTML)

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
    logger.info(f"🔧 Загружено брендов: {len([k for k in SERVICE_CENTERS.keys() if not isinstance(SERVICE_CENTERS[k], str)])}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
