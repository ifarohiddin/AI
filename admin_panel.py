from aiogram import Bot, types
from aiogram.types import Update, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()
ADMINS = [5358180855]  # Adminlarning Telegram ID-lari

async def admin_check(update: Update, bot: Bot, state: FSMContext) -> bool:
    user_id = update.message.from_user.id
    if user_id not in ADMINS:
        await update.message.reply("Sizda admin huquqlari yo'q!")
        return False
    return True

# Kino qo'shish
async def add_movie(update: Update, bot: Bot, state: FSMContext):
    if update.message.document:
        file = await update.message.document.get_file()
        file_url = file.file_path
        name = update.message.caption or "Nomsiz kino"

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            await update.message.reply("Ma'lumotlar bazasi ulanishi topilmadi!")
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
        cursor.execute("INSERT INTO movies (name, link) VALUES (%s, %s) RETURNING id", (name, file_url))
        movie_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        await update.message.reply(f"Kino qo'shildi! ID: {movie_id}")
    else:
        await update.message.reply("Iltimos, kino faylini yuboring!")

# Kino tahrirlash
async def edit_movie(update: Update, bot: Bot, state: FSMContext):
    args = update.message.text.split()[1:] if update.message.text else []
    if len(args) < 2:
        await update.message.reply("Iltimos, /edit_movie <ID> <yangi nom> yoki <yangi link> kiriting!")
        return

    movie_id, new_value = args[0], " ".join(args[1:])
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await update.message.reply("Ma'lumotlar bazasi ulanishi topilmadi!")
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

    await update.message.reply(f"Kino (ID: {movie_id}) tahrirlandi!")

# Kino o'chirish
async def delete_movie(update: Update, bot: Bot, state: FSMContext):
    args = update.message.text.split()[1:] if update.message.text else []
    if not args:
        await update.message.reply("Iltimos, /delete_movie <ID> kiriting!")
        return

    movie_id = args[0]
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await update.message.reply("Ma'lumotlar bazasi ulanishi topilmadi!")
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

    await update.message.reply(f"Kino (ID: {movie_id}) o'chirildi!")

# Kanal qo'shish/o'zgartirish
async def set_channel(update: Update, bot: Bot, state: FSMContext):
    args = update.message.text.split()[1:] if update.message.text else []
    if not args:
        await update.message.reply("Iltimos, /set_channel <kanal ID> kiriting!")
        return

    channel_id = args[0]
    bot.data["channel_id"] = channel_id
    await update.message.reply(f"Kanal o'zgartirildi: {channel_id}")

# Kanal o'chirish
async def delete_channel(update: Update, bot: Bot, state: FSMContext):
    args = update.message.text.split()[1:] if update.message.text else []
    if not args:
        await update.message.reply("Iltimos, o'chirish uchun kanal ID-sini kiriting!")
        return

    channel_id = args[0]
    if "channel_id" in bot.data and bot.data["channel_id"] == channel_id:
        del bot.data["channel_id"]
        await update.message.reply(f"Kanal {channel_id} o'chirildi!")
    else:
        await update.message.reply("Bunday kanal topilmadi!")

# Kanal tahrirlash
async def edit_channel(update: Update, bot: Bot, state: FSMContext):
    args = update.message.text.split()[1:] if update.message.text else []
    if len(args) < 2:
        await update.message.reply("Iltimos, /edit_channel <eski_ID> <yangi_ID> kiriting!")
        return

    old_channel_id, new_channel_id = args[0], args[1]
    if "channel_id" in bot.data and bot.data["channel_id"] == old_channel_id:
        bot.data["channel_id"] = new_channel_id
        await update.message.reply(f"Kanal {old_channel_id} yangi ID {new_channel_id} bilan tahrirlandi!")
    else:
        await update.message.reply("Bunday kanal topilmadi!")