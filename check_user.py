from aiogram import Bot, types
from aiogram.types import Update
from aiogram.fsm.context import FSMContext

async def check_membership(update: Update, bot: Bot, state: FSMContext) -> bool:
    user_id = update.message.from_user.id
    channel_id = bot.data.get("channel_id", "@DefaultChannel")
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
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