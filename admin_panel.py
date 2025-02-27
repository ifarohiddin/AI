from aiogram import Bot, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()
ADMINS = [5358180855]  # Adminlarning Telegram ID-lari

async def admin_check(message: Message, bot: Bot, state: FSMContext) -> bool:
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("*❌ Sizda admin huquqlari yo'q!*\n\nFaqat adminlar ushbu opsiyalardan foydalanishi mumkin.", parse_mode="Markdown")
        return False
    return True

# Kino qo'shish (yangi: link va nom bilan)
async def add_movie(message: Message, bot: Bot, state: FSMContext, movie_name: str, movie_link: str):
    if not await admin_check(message, bot, state):
        return

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await message.reply("*❌ Ma'lumotlar bazasi ulanishi topilmadi!*\n\nRailway’dagi DATABASE_URL’ni tekshirib ko‘ring.", parse_mode="Markdown")
        return
    
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
    cursor.execute("INSERT INTO movies (name, link) VALUES (%s, %s) RETURNING id", (movie_name, movie_link))
    movie_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    await message.reply(f"*🎬 Kino muvaffaqiyatli qo'shildi! Nom: {movie_name} | Link: {movie_link}*\n\nRahmat, yangi kino uchun! 🎥", parse_mode="Markdown")

# Kino tahrirlash
async def edit_movie(message: Message, bot: Bot, state: FSMContext):
    if not await admin_check(message, bot, state):
        return
    args = message.text.split()[1:] if message.text else []
    if len(args) < 2:
        await message.reply("*❌ Iltimos, /edit_movie <ID> <yangi nom/link> kiriting!*\n\nMasalan: */edit_movie 1 Yangi Kino*", parse_mode="Markdown")
        return

    movie_id, new_value = args[0], " ".join(args[1:])
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await message.reply("*❌ Ma'lumotlar bazasi ulanishi topilmadi!*\n\nRailway’dagi DATABASE_URL’ni tekshirib ko‘ring.", parse_mode="Markdown")
        return
    
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
    cursor.execute("UPDATE movies SET name = %s WHERE id = %s", (new_value, movie_id))
    if cursor.rowcount == 0:
        cursor.execute("UPDATE movies SET link = %s WHERE id = %s", (new_value, movie_id))
    conn.commit()
    conn.close()

    await message.reply(f"*✏️ Kino (ID: {movie_id}) muvaffaqiyatli tahrirlandi!*\n\nYangi qiymat: *{new_value}*", parse_mode="Markdown")

# Kino o'chirish
async def delete_movie(message: Message, bot: Bot, state: FSMContext):
    if not await admin_check(message, bot, state):
        return
    args = message.text.split()[1:] if message.text else []
    if not args:
        await message.reply("*❌ Iltimos, /delete_movie <ID> kiriting!*\n\nMasalan: */delete_movie 1*", parse_mode="Markdown")
        return

    movie_id = args[0]
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await message.reply("*❌ Ma'lumotlar bazasi ulanishi topilmadi!*\n\nRailway’dagi DATABASE_URL’ni tekshirib ko‘ring.", parse_mode="Markdown")
        return
    
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
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    conn.close()

    await message.reply(f"*🗑️ Kino (ID: {movie_id}) muvaffaqiyatli o'chirildi!*\n\nRahmat, buni uchun!", parse_mode="Markdown")

# Kanal qo'shish/o'zgartirish (yangi: link va ID bilan)
async def set_channel(message: Message, bot: Bot, state: FSMContext):
    if not await admin_check(message, bot, state):
        return
    args = message.text.split()[1:] if message.text else []
    if not args:
        await message.reply("*❌ Iltimos, /set_channel <kanal ID> kiriting!*\n\nMasalan: */set_channel @example_channel* yoki */set_channel -1001234567890*", parse_mode="Markdown")
        return

    channel_id = args[0]
    global CHANNEL_ID
    CHANNEL_ID = channel_id
    await message.reply(f"*🌐 Kanal muvaffaqiyatli o'zgartirildi: {channel_id}*\n\nKanalni tekshirib ko‘ring!", parse_mode="Markdown")

# Kanal o'chirish
async def delete_channel(message: Message, bot: Bot, state: FSMContext):
    if not await admin_check(message, bot, state):
        return
    args = message.text.split()[1:] if message.text else []
    if not args:
        await message.reply("*❌ Iltimos, o'chirish uchun kanal ID-sini kiriting!*\n\nMasalan: *@example_channel* yoki *-1001234567890*", parse_mode="Markdown")
        return

    channel_id = args[0]
    global CHANNEL_ID
    if CHANNEL_ID == channel_id:
        CHANNEL_ID = "@DefaultChannel"
        await message.reply(f"*🗑️ Kanal {channel_id} muvaffaqiyatli o'chirildi!*\n\nStandart kanalga qaytdik: @DefaultChannel*", parse_mode="Markdown")
    else:
        await message.reply("*❌ Bunday kanal topilmadi!*\n\nKanal ID’sini qayta tekshirib ko‘ring.", parse_mode="Markdown")

# Kanal tahrirlash
async def edit_channel(message: Message, bot: Bot, state: FSMContext):
    if not await admin_check(message, bot, state):
        return
    args = message.text.split()[1:] if message.text else []
    if len(args) < 2:
        await message.reply("*❌ Iltimos, /edit_channel <eski_ID> <yangi_ID> kiriting!*\n\nMasalan: */edit_channel @old_channel @new_channel*", parse_mode="Markdown")
        return

    old_channel_id, new_channel_id = args[0], args[1]
    global CHANNEL_ID
    if CHANNEL_ID == old_channel_id:
        CHANNEL_ID = new_channel_id
        await message.reply(f"*✏️ Kanal {old_channel_id} yangi ID {new_channel_id} bilan muvaffaqiyatli tahrirlandi!*\n\nKanalni tekshirib ko‘ring!", parse_mode="Markdown")
    else:
        await message.reply("*❌ Bunday kanal topilmadi!*\n\nEski kanal ID’sini qayta tekshirib ko‘ring.", parse_mode="Markdown")