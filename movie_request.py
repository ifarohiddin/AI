from telegram import Update
from telegram.ext import ContextTypes
from check_user import check_membership

async def request_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_membership(update, context):
        return

    await update.message.reply_text("Iltimos, kino ID-sini kiriting:")
    return "GET_MOVIE_ID"