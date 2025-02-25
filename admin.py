from aiogram import Router, F
from aiogram.types import Message
from database import connect_db

router = Router()

ADMIN_IDS = [5358180855]  # Bu yerga adminlar ID'sini yozing

@router.message(F.text.startswith("/add_movie"))
async def add_movie(message: Message):
    """Admin yangi kino qo‘shishi"""
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("❌ Siz admin emassiz!")

    args = message.text.split(" ", 2)
    if len(args) < 3:
        return await message.answer("❌ Noto‘g‘ri format! Foydalanish: /add_movie ID Nomi")

    movie_id, title = args[1], args[2]
    
    conn = await connect_db()
    await conn.execute("INSERT INTO movies (id, title) VALUES ($1, $2)", movie_id, title)
    await conn.close()

    await message.answer(f"✅ {title} kinolari bazaga qo‘shildi!")

@router.message(F.text.startswith("/add_channel"))
async def add_channel(message: Message):
    """Admin yangi kanal qo‘shishi"""
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("❌ Siz admin emassiz!")

    args = message.text.split(" ", 2)
    if len(args) < 3:
        return await message.answer("❌ Noto‘g‘ri format! Foydalanish: /add_channel ID Nomi")

    channel_id, title = args[1], args[2]
    
    conn = await connect_db()
    await conn.execute("INSERT INTO channels (id, title) VALUES ($1, $2)", channel_id, title)
    await conn.close()

    await message.answer(f"✅ {title} kanali bazaga qo‘shildi!")