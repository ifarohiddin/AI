from aiogram import Bot, types
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse  # Yangilangan import

load_dotenv()

async def send_movie(update: Update, bot: Bot, state: FSMContext):
    movie_id = update.message.text
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

    cursor.execute("SELECT name, link FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()

    if movie:
        name, link = movie
        await update.message.reply_text(f"Kino: {name}\nLink: {link}")
    else:
        await update.message.reply_text("Bunday ID bilan kino topilmadi!")

    conn.close()
    await state.clear()