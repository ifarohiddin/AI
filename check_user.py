from aiogram import Bot, types
from aiogram.types import Update, Message
from aiogram.fsm.context import FSMContext

async def check_membership(update: Update | Message, bot: Bot, state: FSMContext | None = None) -> bool:
    user_id = update.from_user.id if isinstance(update, Update) else update.from_user.id
    channel_id = bot.data.get("channel_id", "@DefaultChannel")  # Bir nechta kanal uchun ro‘yxat qo‘shish mumkin
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            if isinstance(update, Message):
                await update.reply(
                    f"Iltimos, avval {channel_id} kanaliga a'zo bo'ling!"
                )
            return False
    except Exception as e:
        if isinstance(update, Message):
            await update.reply("Xatolik yuz berdi. Kanalni tekshirib ko'ring.")
        return False