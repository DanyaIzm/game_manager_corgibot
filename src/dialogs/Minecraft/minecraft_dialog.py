from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel

from aiogram.dispatcher.filters.state import StatesGroup, State


class MainSG(StatesGroup):
    main = State()


async def get_minecraft_dialog_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data
    return data



minecraft_dialog = Dialog(
    Window(
        Format('Выбрана игра {game}'),
        Cancel(Const('В главное меню')),
        state=MainSG.main,
    ),
    getter=get_minecraft_dialog_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
