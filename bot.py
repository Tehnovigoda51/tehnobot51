import os
import logging
import aiohttp
import re
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

# ============ ТВОЯ РАБОЧАЯ ССЫЛКА ============
GOOGLE_SHEET_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThbaWJ9-P9-f46WZAaTIBUKjjOGXKS9G9GmFzkYtmCsik_cmqIzJXLnV2315dHI5UPgyEEM7wqaAjo/pub?gid=510149580&single=true&output=csv"
# =============================================

async def load_products():
    """Загружает и парсит твой файл в список товаров"""
    products = []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GOOGLE_SHEET_CSV) as resp:
                if resp.status != 200:
                    logger.error(f"Не удалось загрузить файл: {resp.status}")
                    return products
                
                text = await resp.text()
                lines = text.splitlines()
                
                current_warehouse = "Неизвестно"
                
                for line in lines:
                    if not line.strip():
                        continue
                    
                    # Определяем склад
                    if "СКЛАД" in line.upper() or "РОЗНИЦА" in line.upper():
                        parts = line.split(',')
                        if parts and parts[0].strip():
                            current_warehouse = parts[0].strip()
                        continue
                    
                    # Пропускаем служебные строки
                    if any(word in line.upper() for word in ["ИТОГО", "ПАРАМЕТРЫ", "АРТИКУЛ", "НОМЕНКЛАТУРА", "===>"]):
                        continue
                    
                    columns = line.split(',')
                    
                    if len(columns) > 8:
                        name = columns[1].strip() if len(columns) > 1 else ""
                        stock_text = columns[7].strip() if len(columns) > 7 else ""
                        
                        if not name or len(name) < 3:
                            continue
                        
                        try:
                            match = re.search(r'(\d+)', stock_text)
                            stock = int(match.group(1)) if match else 0
                        except:
                            stock = 0
                        
                        if stock <= 0:
                            continue
                        
                        products.append({
                            "name": name,
                            "stock": stock,
                            "warehouse": current_warehouse
                        })
                
                logger.info(f"✅ Загружено {len(products)} товаров")
                return products
                
    except Exception as e:
        logger.error(f"Ошибка загрузки: {e}")
        return products

PRODUCTS = []

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🎬 <b>ТЕХНОВЫГОДА — Поиск товаров</b>\n\n"
        "🔍 <b>Поиск по моделям:</b> /search <i>название</i>\n"
        "📺 <b>IPTV плейлист:</b> /list\n\n"
        "✅ <b>Примеры:</b>\n"
        "/search beko 7612\n"
        "/search lg ga-b509\n"
        "/search haier c2f636\n"
        "/search телевизор 55 tcl\n\n"
        "📦 <i>Поиск работает по ключевым словам</i>"
    )

@dp.message(Command("list"))
async def send_list(message: types.Message):
    await message.answer(
        f"📺 <b>Твой IPTV плейлист:</b>\n<code>{PUBLIC_URL}</code>",
        disable_web_page_preview=True
    )

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    global PRODUCTS
    
    if not PRODUCTS:
        status_msg = await message.answer("⏳ Загружаю остатки...")
        PRODUCTS = await load_products()
        await status_msg.delete()
        
        if not PRODUCTS:
            await message.answer("❌ Не удалось загрузить данные о товарах.")
            return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("🔍 Пример: /search beko 7612")
        return
    
    query = args[1].strip().lower()
    keywords = query.split()
    
    results = []
    for product in PRODUCTS:
        name_lower = product["name"].lower()
        
        if all(keyword in name_lower for keyword in keywords):
            results.append(product)
    
    results.sort(key=lambda x: x["stock"], reverse=True)
    results = results[:15]
    
    if not results:
        await message.answer(f"❌ Ничего не найдено по запросу «{query}»")
        return
    
    response = [f"🔍 <b>Найдено по запросу «{query}»:</b>"]
    response.append(f"📦 Всего позиций: {len(results)}\n")
    
    for i, p in enumerate(results[:10], 1):
        response.append(
            f"{i}. <b>{p['name'][:60]}</b>{'…' if len(p['name']) > 60 else ''}\n"
            f"   📍 {p['warehouse']}  |  🟢 {p['stock']} шт"
        )
    
    if len(results) > 10:
        response.append(f"\n... и ещё {len(results) - 10} позиций")
    
    await message.answer("\n".join(response), parse_mode=ParseMode.HTML)

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
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
