import os
from dotenv import load_dotenv

# .env faylidan ma'lumotlarni yuklash
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Bot tokeni
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL URL

ADMINS = [5358180855]  # Admin user ID'lari

CHANNELS = ["channel_username1", "channel_username2"]  # Kerakli kanallar



# PostgreSQL ulanish sozlamalari
DB_HOST = "localhost"
DB_NAME = "testdemo"
DB_USER = "newpostgres"
DB_PASSWORD = "Minatokun13."
DB_PORT = 5432