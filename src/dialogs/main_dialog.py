import importlib

from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Start

from aiogram.dispatcher.filters.state import StatesGroup, State

from custom_windows.dynamic_window import DynamicWindow

from pony import orm

from database import GameModel


class GreetingSG(StatesGroup):
    start = State()


def get_state_path(game_name: str) -> str:
    return f'dialogs.{game_name}.{game_name.lower()}_dialog'


def render_game_buttons() -> list[Start]:
    with orm.db_session:
        buttons = [
            Start(
                Const(game.name),
                str(game.id),
                state=importlib.import_module(get_state_path(game.name)).MainSG.main,
                data={
                    'game': game.name,
                }
            ) 
            for game in GameModel.select()
        ]

    return buttons


async def get_main_dialog_data(dialog_manager: DialogManager, **kwargs):
    first_name = dialog_manager.event.from_user.first_name
    
    return {
        'first_name': first_name,
    }



main_dialog = Dialog(
    DynamicWindow(
        Format('Здравствуй, {first_name}! Выбери игру'),
        dynamic_keyboard=render_game_buttons,
        state=GreetingSG.start,
    ),
    getter=get_main_dialog_data,
    launch_mode=LaunchMode.ROOT,
)
