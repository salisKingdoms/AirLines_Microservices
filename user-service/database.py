import asyncpg
from config import DATABASE_URL

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

# Dependency for FastAPI
async def get_db():
    conn = await get_db_connection()
    try:
        yield conn
    finally:
        await conn.close()