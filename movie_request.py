from aiogram import Bot, types
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from check_user import check_membership  # Relative emas, absolute import

class MovieStates(StatesGroup):
    waiting_for_movie_id = State()

async def request_movie(update: Update, bot: Bot, state: FSMContext):
    if not await check_membership(update, bot, state):
        return

    await update.message.reply_text("Iltimos, kino ID-sini kiriting:")
    await state.set_state(MovieStates.waiting_for_movie_id)