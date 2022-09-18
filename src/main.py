import logging

from aiogram import types
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import database

from middleware.user_middleware import UserMiddleware
from middleware.auth_middleware import AuthMiddleware

import config


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Приветик!')


async def main(*args):
    # Настройка логгера
    logging.basicConfig(level=logging.INFO)

    # Миддлвари
    dp.setup_middleware(UserMiddleware())
    dp.setup_middleware(AuthMiddleware())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=main)
