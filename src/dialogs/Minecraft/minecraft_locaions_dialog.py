from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button, Start
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel, MinecraftLocationModel, MinecraftLocationTypeModel

from dialogs.Minecraft.add_location_dialog import NewMinecraftLocationSG


class MinecraftLocationsSG(StatesGroup):
    main = State()


async def get_minecraft_locations_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data

    return data



minecraft_locations_dialog = Dialog(
    Window(
        Format('Локации мира: {world_name}'),
        Button(
            Const('Посмотреть все локации'),
            id='all_locations'
        ),
        Button(
            Const('Выбрать локацию'),
            id='select_location'
        ),
        Start(
            Const('Добавить локацию'),
            id='add_location',
            state=NewMinecraftLocationSG.get_name,
        ),
        Button(
            Const('Добавить тип локации'),
            id='add_location_type'
        ),
        Cancel(Const('Назад')),
        state=MinecraftLocationsSG.main,
    ),
    getter=get_minecraft_locations_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
