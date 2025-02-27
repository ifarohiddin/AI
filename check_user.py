from aiogram import Bot, types
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
from typing import Union

async def check_membership(update: Union[Update, types.Message], bot: Bot, state: Union[FSMContext, None] = None) -> bool:
    user_id = update.from_user.id if isinstance(update, (Update, types.Message)) else update.from_user.id
    channel_id = bot.data.get("channel_id", "@DefaultChannel")
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            if isinstance(update, types.Message):
                await update.reply(
                    f"Iltimos, avval {channel_id} kanaliga a'zo bo'ling!"
                )
            return False
    except Exception as e:
        if isinstance(update, types.Message):
            await update.reply("Xatolik yuz berdi. Kanalni tekshirib ko'ring.")
        return False