from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel


class MainSG(StatesGroup):
    main = State()
    in_world = State()
    new_words = State()


async def get_minecraft_dialog_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data
    return data


async def world_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    word_name = message.text

    with orm.db_session:
        MinecraftWorldModel()


minecraft_dialog = Dialog(
    Window(
        Format('Выбрана игра {game}'),
        Cancel(Const('В главное меню')),
        state=MainSG.main,
    ),
    Window(
        Const('Введите <название мира/версия/описание>'),
        state=MainSG.new_words,
    ),
    getter=get_minecraft_dialog_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
