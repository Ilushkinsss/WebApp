import aiomysql
from config import db_config

async def create_db_pool():
    return await aiomysql.create_pool(
        host=db_config['host'],
        port=3306,
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['database']
    )

async def add_user(telegram_id, city, gender, age):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO Users (telegram_id, city, gender, age, balance, total_tickets) VALUES (%s, %s, %s, %s)",
                (telegram_id, city, gender, age)
            )
            await conn.commit()
