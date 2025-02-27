from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from movie_request import request_movie, MovieStates
from send_movie import send_movie
from admin_panel import add_movie, edit_movie, delete_movie, set_channel
from database import init_db
from aiogram.filters import Command
import os
from dotenv import load_dotenv

load_dotenv()

# Ma'lumotlar bazasini ishga tushirish
init_db()

bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Handler'lar
dp.message.register(request_movie, Command(commands=["get_movie"]))
dp.message.register(send_movie, MovieStates.waiting_for_movie_id)
dp.message.register(add_movie, Command(commands=["add_movie"]))
dp.message.register(edit_movie, Command(commands=["edit_movie"]))
dp.message.register(delete_movie, Command(commands=["delete_movie"]))
dp.message.register(set_channel, Command(commands=["set_channel"]))

if __name__ == "__main__":
    dp.run_polling(bot)