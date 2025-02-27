from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from movie_request import request_movie, MovieStates
from send_movie import send_movie
from admin_panel import add_movie, edit_movie, delete_movie, set_channel, delete_channel, edit_channel
from database import init_db
from aiogram.filters import Command
from check_user import check_membership
from aiogram.fsm.context import FSMContext
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

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

# Global o‘zgaruvchi sifatida kanal ID’sini saqlash
CHANNEL_ID = "@DefaultChannel"  # Dastlabki kanal ID

# Yangi davlatlar (states) aniqlash
class AdminStates(StatesGroup):
    waiting_for_movie_file = State()
    waiting_for_edit_movie = State()
    waiting_for_delete_movie = State()
    waiting_for_set_channel = State()
    waiting_for_delete_channel = State()
    waiting_for_edit_channel = State()

# Kinolar ro‘yxatini olish funksiyasi
async def get_movies_list(bot: Bot, user_id: int):
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return "Ma'lumotlar bazasi ulanishi topilmadi!"

    url = urlparse(db_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
        sslmode='require'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, link FROM movies")
    movies = cursor.fetchall()
    conn.close()

    if not movies:
        return "Hozircha hech qanday kino mavjud emas!"

    response = "Kinolar ro‘yxati:\n"
    for movie in movies:
        response += f"ID: {movie[0]} | Nom: {movie[1]} | Link: {movie[2]}\n"
    return response

# Kanallar ro‘yxatini olish funksiyasi
async def get_channels_list():
    return f"Hozirgi kanal: {CHANNEL_ID}"

# /start komandasiga javob (oddiy foydalanuvchi va admin uchun)
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    ADMINS = [5358180855]  # Admin ID

    if user_id in ADMINS:
        # Admin uchun inline button'lar
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Kino Qo'shish", callback_data="add_movie")],
            [types.InlineKeyboardButton(text="Kino Tahrirlash", callback_data="edit_movie")],
            [types.InlineKeyboardButton(text="Kino O'chirish", callback_data="delete_movie")],
            [types.InlineKeyboardButton(text="Kinolar Ro‘yxatini Ko‘rish", callback_data="view_movies")],
            [types.InlineKeyboardButton(text="Kanal Qo'shish", callback_data="set_channel")],
            [types.InlineKeyboardButton(text="Kanal O'chirish", callback_data="delete_channel")],
            [types.InlineKeyboardButton(text="Kanal Tahrirlash", callback_data="edit_channel")],
            [types.InlineKeyboardButton(text="Kanallar Ro‘yxatini Ko‘rish", callback_data="view_channels")]
        ])
        await message.answer("Salom, Admin! Quyidagi opsiyalardan birini tanlang:", reply_markup=keyboard)
    else:
        # Oddiy foydalanuvchi uchun
        await message.answer("Salom! Men kino botiman. Avval kanallarga a'zo bo'ling!")
        if await check_membership(message, bot, None, CHANNEL_ID):
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Kanallar Ro‘yxatini Ko‘rish", callback_data="view_channels")]
            ])
            await message.answer("Siz barcha zarur kanallarga a'zo ekansiz! Kino so‘rov qilish uchun kino ID-sini kiriting:", reply_markup=keyboard)
            await state.set_state(MovieStates.waiting_for_movie_id)
        else:
            await message.answer("Iltimos, avval barcha zarur kanallarga a'zo bo'ling!")

# Callback handler'lar admin uchun
@dp.callback_query(lambda c: c.data == "add_movie")
async def process_add_movie(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Kino faylini yuboring (caption orqali nom kiriting):")
    await state.set_state(AdminStates.waiting_for_movie_file)

@dp.callback_query(lambda c: c.data == "edit_movie")
async def process_edit_movie(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Kino ID va yangi nom/linkni kiriting (format: /edit_movie <ID> <yangi qiymat>):")
    await state.set_state(AdminStates.waiting_for_edit_movie)

@dp.callback_query(lambda c: c.data == "delete_movie")
async def process_delete_movie(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "O'chirish uchun kino ID-sini kiriting (format: /delete_movie <ID>):")
    await state.set_state(AdminStates.waiting_for_delete_movie)

@dp.callback_query(lambda c: c.data == "set_channel")
async def process_set_channel(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Yangi kanal ID-sini kiriting (format: /set_channel <kanal_ID>):")
    await state.set_state(AdminStates.waiting_for_set_channel)

@dp.callback_query(lambda c: c.data == "delete_channel")
async def process_delete_channel(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "O'chirish uchun kanal ID-sini kiriting:")
    await state.set_state(AdminStates.waiting_for_delete_channel)

@dp.callback_query(lambda c: c.data == "edit_channel")
async def process_edit_channel(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Kanal ID va yangi kanal ID-sini kiriting (format: /edit_channel <eski_ID> <yangi_ID>):")
    await state.set_state(AdminStates.waiting_for_edit_channel)

@dp.callback_query(lambda c: c.data == "view_movies")
async def process_view_movies(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    movies_list = await get_movies_list(bot, callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, movies_list)

@dp.callback_query(lambda c: c.data == "view_channels")
async def process_view_channels(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    channels_list = await get_channels_list()
    await bot.send_message(callback_query.from_user.id, channels_list)

# Admin uchun yangi handler'lar
@dp.message(AdminStates.waiting_for_movie_file, lambda message: message.from_user.id in [5358180855])
async def handle_add_movie_file(message: Message, state: FSMContext):
    if message.document:
        file = await message.document.get_file()
        file_url = file.file_path
        name = message.caption or "Nomsiz kino"
        await add_movie(message, bot, state)
        await state.clear()
    else:
        await message.answer("Iltimos, kino faylini yuboring!")

@dp.message(AdminStates.waiting_for_edit_movie, lambda message: message.from_user.id in [5358180855])
async def handle_edit_movie(message: Message, state: FSMContext):
    args = message.text.split()
    if len(args) < 3 or not args[0].startswith("/edit_movie"):
        await message.answer("Iltimos, /edit_movie <ID> <yangi nom/link> kiriting!")
        await state.clear()
        return
    movie_id, new_value = args[1], " ".join(args[2:])
    await edit_movie(message, bot, state)
    await state.clear()

@dp.message(AdminStates.waiting_for_delete_movie, lambda message: message.from_user.id in [5358180855])
async def handle_delete_movie(message: Message, state: FSMContext):
    args = message.text.split()
    if not args or not args[0].startswith("/delete_movie"):
        await message.answer("Iltimos, /delete_movie <ID> kiriting!")
        await state.clear()
        return
    movie_id = args[1]
    await delete_movie(message, bot, state)
    await state.clear()

@dp.message(AdminStates.waiting_for_set_channel, lambda message: message.from_user.id in [5358180855])
async def handle_set_channel(message: Message, state: FSMContext):
    args = message.text.split()
    if not args or not args[0].startswith("/set_channel"):
        await message.answer("Iltimos, /set_channel <kanal ID> kiriting!")
        await state.clear()
        return
    channel_id = args[1]
    global CHANNEL_ID
    CHANNEL_ID = channel_id
    await set_channel(message, bot, state)
    await state.clear()

@dp.message(AdminStates.waiting_for_delete_channel, lambda message: message.from_user.id in [5358180855])
async def handle_delete_channel(message: Message, state: FSMContext):
    args = message.text.split()
    if not args:
        await message.answer("Iltimos, o'chirish uchun kanal ID-sini kiriting!")
        await state.clear()
        return
    channel_id = args[0]
    global CHANNEL_ID
    if CHANNEL_ID == channel_id:
        CHANNEL_ID = "@DefaultChannel"
        await delete_channel(message, bot, state)
    else:
        await message.answer("Bunday kanal topilmadi!")
    await state.clear()

@dp.message(AdminStates.waiting_for_edit_channel, lambda message: message.from_user.id in [5358180855])
async def handle_edit_channel(message: Message, state: FSMContext):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Iltimos, /edit_channel <eski_ID> <yangi_ID> kiriting!")
        await state.clear()
        return
    old_channel_id, new_channel_id = args[0], args[1]
    global CHANNEL_ID
    if CHANNEL_ID == old_channel_id:
        CHANNEL_ID = new_channel_id
        await edit_channel(message, bot, state)
    else:
        await message.answer("Bunday kanal topilmadi!")
    await state.clear()

# Handler'lar
dp.message.register(request_movie, Command(commands=["get_movie"]))
dp.message.register(send_movie, MovieStates.waiting_for_movie_id)
dp.message.register(add_movie, Command(commands=["add_movie"]))
dp.message.register(edit_movie, Command(commands=["edit_movie"]))
dp.message.register(delete_movie, Command(commands=["delete_movie"]))
dp.message.register(set_channel, Command(commands=["set_channel"]))

if __name__ == "__main__":
    dp.run_polling(bot)