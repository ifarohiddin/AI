from telegram import Update
from telegram.ext import ContextTypes

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.message.from_user.id
    channel_id = context.bot_data.get("channel_id", "@DefaultChannel")
    try:
        member = await context.bot.get_chat_member(channel_id, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            await update.message.reply_text(
                f"Iltimos, avval {channel_id} kanaliga a'zo bo'ling!"
            )
            return False
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi. Kanalni tekshirib ko'ring.")
        return False