import asyncpg
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

async def connect_db():
    return await asyncpg.create_pool(
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, host=DB_HOST, port=DB_PORT
    )

async def get_movie_by_id(pool, movie_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM movies WHERE id=$1", movie_id)