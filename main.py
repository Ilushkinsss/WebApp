import logging
import asyncio
import aiomysql
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

API_TOKEN = '7336746673:AAF3_vUh_Sm01UpRBSH-1T8aOC5A_czJZ5c'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

app = FastAPI() #API

# Настройка подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'telegram_bot'
}

class User(BaseModel):
    telegram_id: str
    city: str
    gender: str
    age: int


@app.post("/register")
def register(user: User):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Вставка данных в базу данных
        cursor.execute(
            "INSERT INTO Users (telegram_id, city, gender, age) VALUES (%s, %s, %s, %s)",
            (user.telegram_id, user.city, user.gender, user.age)
        )
        conn.commit()

        return {"success": "true"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

logging.basicConfig(level=logging.INFO)

async def create_db_pool():
    return await aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='861211955233iK',
        db='mysql'
    )

async def create_user_table():
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS USER (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    telegram_id BIGINT NOT NULL,
                    city VARCHAR(100),
                    gender ENUM('male', 'female', 'other'),
                    balance DECIMAL(10, 2) DEFAULT 0.00,
                    total_tickets INT DEFAULT 0
                )
            """)
            await conn.commit()

async def add_user(user_id, username):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT IGNORE INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
            await conn.commit()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    global db_pool
    db_pool = await create_db_pool()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
