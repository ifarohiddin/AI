from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink
from config import CHANNELS

router = Router()

def check_subscription_keyboard():
    """Kanallarga obuna bo‘lish tugmalarini yaratish"""
    buttons = [[InlineKeyboardButton(text=f"📢 Kanal {i+1}", url=f"https://t.me/{channel}")] for i, channel in enumerate(CHANNELS)]
    buttons.append([InlineKeyboardButton(text="✅ A'zolikni tekshirish", callback_data="check_subs")])  # Pastdagi tekshirish tugmasi
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def check_subscription(bot, user_id):
    """Foydalanuvchining barcha kanallarga a'zo bo'lganligini tekshirish"""
    for channel in CHANNELS:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False  # Agar bitta kanalga a'zo bo‘lmasa, False qaytariladi
        except Exception:
            return False  # Kanalni topa olmasa ham False qaytariladi
    return True

@router.message(F.text == "/start")
async def start_command(message: Message):
    """Foydalanuvchi /start bosganda kanallarni tekshirish"""
    text = "📢 Botdan foydalanish uchun quyidagi kanallarga a'zo bo‘ling:\n\n"

    await message.answer(text, reply_markup=check_subscription_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "check_subs")
async def check_subscription_handler(callback: CallbackQuery):
    """Foydalanuvchi a'zolikni tekshirganida javob berish"""
    user_id = callback.from_user.id
    bot = callback.bot

    if await check_subscription(bot, user_id):
        await callback.message.edit_text("✅ Siz a'zo bo‘lgansiz. Endi kino ID jo‘nating.")
    else:
        await callback.message.edit_text("❌ Iltimos, barcha kanallarga a'zo bo‘ling va yana urining.", 
                                         reply_markup=check_subscription_keyboard())
