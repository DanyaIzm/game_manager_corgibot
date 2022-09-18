import logging

from aiogram import types
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_dialog import DialogRegistry

from database import database

from middleware.user_middleware import UserMiddleware
from middleware.auth_middleware import AuthMiddleware

from dialogs import main_dialog
from dialogs.Minecraft import minecraft_dialog

import config


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

registry = DialogRegistry(dp)


async def main(*args):
    # Настройка логгера
    logging.basicConfig(level=logging.INFO)

    # Миддлвари
    dp.setup_middleware(UserMiddleware())
    dp.setup_middleware(AuthMiddleware())

    # Регистрируем диалоги
    registry.register(main_dialog.main_dialog)
    registry.register(minecraft_dialog.minecraft_dialog)

    registry.register_start_handler(main_dialog.GreetingSG.start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=main)
