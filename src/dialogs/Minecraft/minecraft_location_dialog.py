from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button, Start, SwitchTo, Back, Row
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from dialogs.Minecraft.states import MinecraftLocationSG

from dialogs.common.complete_dialog import complete


async def get_minecraft_location_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data

    return data



minecraft_location_dialog = Dialog(
    Window(
        Format('Здесь будет управление локациями. Текущая локация "{location_name}" мира "{world_name}"'),
        Button(
            Const('Назад'),
            id='return_to_all_locations',
            on_click=complete
        ),
        state=MinecraftLocationSG.main
    ),
    getter=get_minecraft_location_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
