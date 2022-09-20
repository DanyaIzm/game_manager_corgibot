from typing import List

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button, Start, SwitchTo, Back, Row
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel, MinecraftLocationModel, MinecraftLocationTypeModel

from dialogs.Minecraft.add_location_dialog import NewMinecraftLocationSG
from dialogs.Minecraft.add_location_type_dialog import NewMinecraftLocationTypeSG


class MinecraftLocationsSG(StatesGroup):
    main = State()

    all_location_types = State()


async def get_minecraft_locations_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data

    return data


def render_locations_text(locations: List[str]):
    rendered_text = 'Список всех локаций: \n\n'

    for index, locaiton in enumerate(locations):
        rendered_text += f'({index + 1}) -> {locaiton}\n'

    return rendered_text


async def get_all_location_types(dialog_manager: DialogManager, **kwargs):
    with orm.db_session:
        locations = [location.name for location in MinecraftLocationTypeModel.select()]

    return {
        'all_locations_text': render_locations_text(locations),
    }


async def setup_start_add_location_data(callback: types.CallbackQuery, start_button: Start, manager: DialogManager):
    context = manager.current_context()
    data = context.dialog_data
    data.update(context.start_data)

    # setup world data into the start button
    start_button.start_data = data



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
            on_click=setup_start_add_location_data
        ),
        Row(
            SwitchTo(
            Const('Все типы локаций'),
            id='all_location_types',
            state=MinecraftLocationsSG.all_location_types,
            ),
            Start(
                Const('Добавить тип локации'),
                id='add_location_type',
                state=NewMinecraftLocationTypeSG.get_name,
            ),
        ),
        Cancel(Const('Назад')),
        state=MinecraftLocationsSG.main,
    ),
    # Все типы локаций
    Window(
        Format('{all_locations_text}'),
        Back(Const('Назад')),
        getter=get_all_location_types,
        state=MinecraftLocationsSG.all_location_types
    ),
    getter=get_minecraft_locations_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
