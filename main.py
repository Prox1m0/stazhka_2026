import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, ADMIN_ID
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
from services.settings_service import load_settings

load_settings()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if ADMIN_ID is None:
        raise ValueError("❌ Не задан ADMIN_ID в .env")
    
    print(f"✅ Бот запущен. Админ-ID: {ADMIN_ID}")
    asyncio.run(main())
