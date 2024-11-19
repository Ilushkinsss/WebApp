import logging
import asyncio
import aiomysql
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

API_TOKEN = '7336746673:AAF3_vUh_Sm01UpRBSH-1T8aOC5A_czJZ5c'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

app = FastAPI()  # API

# Настройка подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '861211955233iK',
    'database': 'mysql'
}



class User(BaseModel):
    telegram_id: str
    city: str
    gender: str
    age: int

# Глобальная переменная для пула базы данных
db_pool = None

async def create_db_pool():
    return await aiomysql.create_pool(
        host=db_config['host'],
        port=3306,
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['database']
    )

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/register")
async def register(user: User):
    if db_pool is None:
        return {"success": "false", "error": "Database pool is not initialized."}

    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO Users (telegram_id, city, gender, age) VALUES (%s, %s, %s, %s)",
                    (user.telegram_id, user.city, user.gender, user.age)
                )
                await conn.commit()
        return {"success": "true"}
    except Exception as e:
        return {"success": "false", "error": str(e)}

    except aiomysql.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

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

