import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse  # Yangilangan import

load_dotenv()

def init_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set!")
    
    url = urlparse(db_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            link TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()