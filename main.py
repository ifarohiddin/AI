from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup  # StatesGroup va State import qo'shildi
from movie_request import request_movie, MovieStates
from send_movie import send_movie
from admin_panel import add_movie, edit_movie, delete_movie, set_channel, delete_channel, edit_channel
from database import init_db
from aiogram.filters import Command
from check_user import check_membership
from aiogram.fsm.context import FSMContext
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

# Yangi davlatlar (states) aniqlash
class AdminStates(StatesGroup):
    waiting_for_movie_file = State()
    waiting_for_edit_movie = State()
    waiting_for_delete_movie = State()
    waiting_for_set_channel = State()
    waiting_for_delete_channel = State()
    waiting_for_edit_channel = State()

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
            [types.InlineKeyboardButton(text="Kanal Qo'shish", callback_data="set_channel")],
            [types.InlineKeyboardButton(text="Kanal O'chirish", callback_data="delete_channel")],
            [types.InlineKeyboardButton(text="Kanal Tahrirlash", callback_data="edit_channel")]
        ])
        await message.answer("Salom, Admin! Quyidagi opsiyalardan birini tanlang:", reply_markup=keyboard)
    else:
        # Oddiy foydalanuvchi uchun
        await message.answer("Salom! Men kino botiman. Avval kanallarga a'zo bo'ling!")
        if await check_membership(message, bot, None):
            await message.answer("Siz barcha zarur kanallarga a'zo ekansiz! Kino so‘rov qilish uchun kino ID-sini kiriting:")
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
    await delete_channel(message, bot, state)
    await state.clear()

@dp.message(AdminStates.waiting_for_edit_channel, lambda message: message.from_user.id in [5358180855])
async def handle_edit_channel(message: Message, state: FSMContext):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Iltimos, /edit_channel <eski_ID> <yangi_ID> kiriting!")
        await state.clear()
        return
    old_channel_id, new_channel_id = args[0], args[1]
    await edit_channel(message, bot, state)
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