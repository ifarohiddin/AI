from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from movie_request import request_movie, MovieStates
from send_movie import send_movie
from admin_panel import add_movie, edit_movie, delete_movie, set_channel
from database import init_db
from aiogram.filters import Command
from check_user import check_membership
import os
from dotenv import load_dotenv

load_dotenv()

# Ma'lumotlar bazasini ishga tushirish
try:
    init_db()
except Exception as e:
    print(f"Database initialization failed: {e}")
    raise

bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# /start komandasiga javob
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Salom! Men kino botiman. Avval kanallarga a'zo bo'ling va /get_movie komandasi bilan kino so‘rov qiling!")
    
    # Kanal a’zoligini tekshirish
    if await check_membership(message, bot, None):  # FSMContext yo‘q, chunki bu dastlabki tekshiruv
        await message.answer("Siz barcha zarur kanallarga a'zo ekansiz! Kino so‘rov qilish uchun /get_movie ni ishlatishingiz mumkin.")
    else:
        await message.answer("Iltimos, avval barcha zarur kanallarga a'zo bo'ling!")

# Handler'lar
dp.message.register(request_movie, Command(commands=["get_movie"]))
dp.message.register(send_movie, MovieStates.waiting_for_movie_id)
dp.message.register(add_movie, Command(commands=["add_movie"]))
dp.message.register(edit_movie, Command(commands=["edit_movie"]))
dp.message.register(delete_movie, Command(commands=["delete_movie"]))
dp.message.register(set_channel, Command(commands=["set_channel"]))

if __name__ == "__main__":
    dp.run_polling(bot)