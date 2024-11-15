from aiogram import types
from aiogram.filters import Command
from fastapi import HTTPException
from models import User
from database.db import add_user  # Импортируем функцию добавления пользователя

async def setup(dp):
    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.answer("Привет!")

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(message.text)
