import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties  # ✅ Yangi usul
from config import TOKEN
from handlers import router

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))  # ✅ Xatolik tuzatildi
    dp = Dispatcher()
    dp.include_router(router)

    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
