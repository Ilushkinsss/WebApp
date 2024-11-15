import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from database.db import create_db_pool
from handlers import user_handlers

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    global db_pool
    db_pool = await create_db_pool()
    await user_handlers.setup(dp)  # Подключаем обработчики
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
