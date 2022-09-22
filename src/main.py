import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_dialog import DialogRegistry, DialogManager

from aiogram import types

from database import database

from middleware.user_middleware import UserMiddleware
from middleware.auth_middleware import AuthMiddleware

from dialogs import main_dialog
from dialogs.Minecraft.minecraft_dialog import minecraft_dialog
from dialogs.Minecraft.new_world_dialog import new_minecraft_world_dialog
from dialogs.Minecraft.minecraft_locaions_dialog import minecraft_locations_dialog
from dialogs.Minecraft.add_location_dialog import new_minecraft_location_dialog
from dialogs.Minecraft.add_location_type_dialog import new_minecraft_location_type_dialog
from dialogs.Minecraft.minecraft_location_dialog import minecraft_location_dialog

import config


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

registry = DialogRegistry(dp)

# Генирируем мапинг орм
database.generate_mapping(create_tables=True)


@dp.message_handler(commands=['reset'])
async def reset(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    await bot.send_message(message.from_user.id, 'Состояния бота были успешно сброшены.\n\nДля начала работы напишите команду /start')


async def main(*args):
    # Настройка логгера
    logging.basicConfig(level=logging.INFO)

    # Миддлвари
    dp.setup_middleware(UserMiddleware())
    dp.setup_middleware(AuthMiddleware())

    # Регистрируем диалоги
    registry.register(main_dialog.main_dialog)

    registry.register(minecraft_dialog)
    registry.register(new_minecraft_world_dialog)

    registry.register(minecraft_locations_dialog)
    registry.register(new_minecraft_location_dialog)
    registry.register(new_minecraft_location_type_dialog)

    registry.register(minecraft_location_dialog)


    registry.register_start_handler(main_dialog.GreetingSG.start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=main)
