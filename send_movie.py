from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_id = update.message.text
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, link FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()

    if movie:
        name, link = movie
        await update.message.reply_text(f"Kino: {name}\nLink: {link}")
    else:
        await update.message.reply_text("Bunday ID bilan kino topilmadi!")
    
    conn.close()
    return None