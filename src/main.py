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
from dialogs.Minecraft.new_world_dialog import new_minecraft_world_dialog
from dialogs.Minecraft.minecraft_locaions_dialog import minecraft_locations_dialog

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
    registry.register(new_minecraft_world_dialog)

    registry.register(minecraft_locations_dialog)


    registry.register_start_handler(main_dialog.GreetingSG.start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=main)
