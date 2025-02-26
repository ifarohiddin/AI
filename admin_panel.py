from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

ADMINS = [123456789]  # Adminlarning Telegram ID-lari

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

        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO movies (name, link) VALUES (?, ?)", (name, file_url))
        conn.commit()
        movie_id = cursor.lastrowid
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
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET name = ? WHERE id = ?", (new_value, movie_id))
    if cursor.rowcount == 0:
        cursor.execute("UPDATE movies SET link = ? WHERE id = ?", (new_value, movie_id))
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
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
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