from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def check_subscription_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ A'zo bo‘ldim", callback_data="check_subs")]
        ]
    )
