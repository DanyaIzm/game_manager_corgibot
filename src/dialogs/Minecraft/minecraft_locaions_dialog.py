from typing import Callable, Coroutine, List

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button, Start, SwitchTo, Back, Row

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftLocationModel, MinecraftLocationTypeModel

from dialogs.Minecraft.add_location_dialog import NewMinecraftLocationSG
from dialogs.Minecraft.add_location_type_dialog import NewMinecraftLocationTypeSG

from dialogs.Minecraft.minecraft_location_dialog import MinecraftLocationSG

from custom_windows.dynamic_window import DynamicWindow


class MinecraftLocationsSG(StatesGroup):
    main = State()

    all_location_types = State()
    all_locations = State()

    select_location_type = State()
    select_location = State()


async def get_minecraft_locations_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data

    return data


def render_locations_text(locations: List[str], is_location_types: bool):
    rendered_text = 'Список всех локаций: \n\n'

    if is_location_types:
        rendered_text = 'Список всех типов локаций:\n\n'

    for index, locaiton in enumerate(locations):
        rendered_text += f'({index + 1}) -> {locaiton}\n'

    return rendered_text


async def get_all_location_types(dialog_manager: DialogManager, **kwargs):
    with orm.db_session:
        location_types = [location_type.name for location_type in MinecraftLocationTypeModel.select()]

    return {
        'all_location_types_text': render_locations_text(location_types, True),
    }


async def setup_start_add_location_data(callback: types.CallbackQuery, start_button: Start, manager: DialogManager):
    context = manager.current_context()
    data = context.dialog_data
    data.update(context.start_data)

    # setup world data into the start button
    start_button.start_data = data


async def get_all_locations(dialog_manager: DialogManager, **kwargs):
    with orm.db_session:
        location_types = [location.name for location in MinecraftLocationModel.select()]

    return {
        'all_locations_text': render_locations_text(location_types, False),
    }


def set_location_type_decorator(location_type_id: int):
    # TODO: refactor
    """
    Декоратор, который возращает функцию, устанавливающую в data id типа локации
    """
    async def wrapped(callback: types.CallbackQuery, button: Button, manager: DialogManager):
        await manager.update({
            'location_type_id': location_type_id
        })

        await manager.dialog().switch_to(MinecraftLocationsSG.select_location)

    return wrapped


def render_location_types_keyboard():
    # TODO: refactor
    with orm.db_session:
        buttons = [
            Button(
                Const(f'{location_type.name}'),
                id=str(location_type.id),
                on_click=set_location_type_decorator(location_type.id)
            )
            for location_type in MinecraftLocationTypeModel.select()
        ]

    return buttons


def setup_start_select_location_data_HOF(location_name: str, location_id: int) -> Coroutine[types.CallbackQuery, Start, DialogManager]:
    """
    Gets location info and return a on_click handler, which setups start data into the button
    Data: location_id, location_name, world_id, world_name
    """

    async def setup_start_select_location_data(callback: types.CallbackQuery, start_button: Start, manager: DialogManager):
        data = {
            'location_name': location_name,
            'location_id': location_id,
        }

        start_data = manager.current_context().start_data

        data.update({
            'world_name': start_data['world_name'],
            'world_id': start_data['world_id'],
        })

        start_button.start_data = data
    
    return setup_start_select_location_data


# TODO: rename all
def render_locations_keyboard_decorator(manager: DialogManager) -> Callable:
    location_type_id = manager.current_context().dialog_data['location_type_id']

    def render_locations_keyboard():
        # TODO: refactor
        with orm.db_session:
            buttons = [
                Start(
                    Const(f'{location.name}'),
                    id=str(location.id),
                    on_click=setup_start_select_location_data_HOF(location.name, location.id),
                    state=MinecraftLocationSG.main
                )
                for location in MinecraftLocationModel.select(type=location_type_id)
            ]

        return buttons

    return render_locations_keyboard



minecraft_locations_dialog = Dialog(
    Window(
        Format('Локации мира: {world_name}'),
        SwitchTo(
            Const('Посмотреть все локации'),
            id='all_locations',
            state=MinecraftLocationsSG.all_locations
        ),
        SwitchTo(
            Const('Выбрать локацию'),
            id='select_location',
            state=MinecraftLocationsSG.select_location_type
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
        Format('{all_location_types_text}'),
        Back(Const('Назад')),
        getter=get_all_location_types,
        state=MinecraftLocationsSG.all_location_types
    ),
    # Все локации
    Window(
        Format('{all_locations_text}'),
        SwitchTo(Const('Назад'), id='switch_to_main_from_all_locations', state=MinecraftLocationsSG.main),
        getter=get_all_locations,
        state=MinecraftLocationsSG.all_locations
    ),
    # Выбрать тип локации
    DynamicWindow(
        Const('Выберите тип локации'),
        SwitchTo(
            Const('Назад к локациям'),
            id='switch_to_main_from_location_type_select',
            state=MinecraftLocationsSG.main
        ),
        dynamic_keyboard=render_location_types_keyboard,
        state=MinecraftLocationsSG.select_location_type
    ),
    # Выбрать локацию
    DynamicWindow(
        Const('Выберите локацию'),
        SwitchTo(
            Const('Назад к локациям'),
            id='switch_to_main_from_location_type_select',
            state=MinecraftLocationsSG.main
        ),
        dynamic_keyboard_decorator=render_locations_keyboard_decorator,
        state=MinecraftLocationsSG.select_location
    ),
    getter=get_minecraft_locations_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
