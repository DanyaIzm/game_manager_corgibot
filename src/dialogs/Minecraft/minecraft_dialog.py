from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel

from dialogs.Minecraft.new_world_dialog import NewMinecraftWorldSG


class MainSG(StatesGroup):
    main = State()
    in_world = State()


async def get_minecraft_dialog_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data
    return data



minecraft_dialog = Dialog(
    Window(
        Format('Выбрана игра {game}'),
        Start(
            Const('Добавить мир'),
            id='new_world',
            state=NewMinecraftWorldSG.get_name
        ),
        Cancel(Const('В главное меню')),
        state=MainSG.main,
    ),
    getter=get_minecraft_dialog_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
