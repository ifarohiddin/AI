from telegram import Update
from telegram.ext import ContextTypes
import psycopg2
from dotenv import load_dotenv
import os
import urlparse

load_dotenv()
ADMINS = [5358180855]  # Adminlarning Telegram ID-lari

async def admin_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.message.from_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("Sizda admin huquqlari yo'q!")
        return False
    return True

# Kino qo'shish
async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return

    if update.message.document:
        file = await update.message.document.get_file()
        file_url = file.file_path
        name = update.message.caption or "Nomsiz kino"

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            await update.message.reply_text("Ma'lumotlar bazasi ulanishi topilmadi!")
            return
        
        url = urlparse(db_url)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (name, link) VALUES (%s, %s) RETURNING id", (name, file_url))
        movie_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        await update.message.reply_text(f"Kino qo'shildi! ID: {movie_id}")
    else:
        await update.message.reply_text("Iltimos, kino faylini yuboring!")

# Kino tahrirlash
async def edit_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Iltimos, /edit_movie <ID> <yangi nom> yoki <yangi link> kiriting!")
        return

    movie_id, new_value = args[0], " ".join(args[1:])
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await update.message.reply_text("Ma'lumotlar bazasi ulanishi topilmadi!")
        return
    
    url = urlparse(db_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET name = %s WHERE id = %s", (new_value, movie_id))
    if cursor.rowcount == 0:
        cursor.execute("UPDATE movies SET link = %s WHERE id = %s", (new_value, movie_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Kino (ID: {movie_id}) tahrirlandi!")

# Kino o'chirish
async def delete_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return

    if not context.args:
        await update.message.reply_text("Iltimos, /delete_movie <ID> kiriting!")
        return

    movie_id = context.args[0]
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        await update.message.reply_text("Ma'lumotlar bazasi ulanishi topilmadi!")
        return
    
    url = urlparse(db_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Kino (ID: {movie_id}) o'chirildi!")

# Kanal qo'shish/o'zgartirish
async def set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await admin_check(update, context):
        return

    if not context.args:
        await update.message.reply_text("Iltimos, /set_channel <kanal ID> kiriting!")
        return

    channel_id = context.args[0]
    context.bot_data["channel_id"] = channel_id
    await update.message.reply_text(f"Kanal o'zgartirildi: {channel_id}")