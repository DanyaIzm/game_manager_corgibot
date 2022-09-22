from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftLocationModel, MinecraftLocationTypeModel

from custom_windows.dynamic_window import DynamicWindow

from dialogs.common.complete_dialog import complete


class NewMinecraftLocationSG(StatesGroup):
    get_name = State()
    get_type = State()
    get_coords = State()
    success = State()
    failure = State()


async def location_name_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    location_name = message.text

    try:
        location_name = location_name.strip()
    except:
        await message.answer('Некорректное название мира')
        return await dialog.switch_to(NewMinecraftLocationSG.get_name, manager)

    await manager.update({
        'location_name': location_name
    })

    return await dialog.next(manager)


def set_location_type_HOF(location_type_id: int):
    """
    HOF, которая возращает функцию, устанавливающую в data id типа локации
    """
    async def wrapped(callback: types.CallbackQuery, button: Button, manager: DialogManager):
        await manager.update({
            'location_type_id': location_type_id
        })

        await manager.dialog().next()

    return wrapped


def render_location_types_keyboard():
    # TODO: refactor
    with orm.db_session:
        buttons = [
            Button(
                Const(f'{location_type.name}'),
                id=str(location_type.id),
                on_click=set_location_type_HOF(location_type.id)
            )
            for location_type in MinecraftLocationTypeModel.select()
        ]

    return buttons


async def set_location_coords(message: types.Message, dialog: Dialog, manager: DialogManager):
    # get locaiton coord
    location_coords = message.text

    try:
        location_coords = location_coords.strip().split(' ')
        if len(location_coords) != 3:
            raise ValueError()
    except:
        await message.answer('Некорректные координаты')
        return await dialog.switch_to(NewMinecraftLocationSG.get_coords, manager)

    # get other location data
    context = manager.current_context()
    dialog_data = context.dialog_data
    # World id is inside start data
    start_data = context.start_data

    location_type_id = dialog_data['location_type_id']
    location_name = dialog_data['location_name']
    world_id = start_data['world_id']

    try:
        with orm.db_session:
            # Add new locaiton into the database
            MinecraftLocationModel(
                name=location_name,
                type=location_type_id,
                world=world_id,
                x=location_coords[0],
                y=location_coords[1],
                z=location_coords[2]
                )
    except:
        return await dialog.switch_to(NewMinecraftLocationSG.failure)
    else:
        return await dialog.switch_to(NewMinecraftLocationSG.success)



new_minecraft_location_dialog = Dialog(
    Window(
        Const('Введите название локации'),
        MessageInput(location_name_input),
        Cancel(Const('Отменить')),
        state=NewMinecraftLocationSG.get_name,
    ),
    DynamicWindow(
        Const('Выберите тип локации'),
        Cancel(Const('Отменить')),
        dynamic_keyboard=render_location_types_keyboard,
        state=NewMinecraftLocationSG.get_type,
    ),
    Window(
        Const('Введите координаты локации через пробел'),
        MessageInput(set_location_coords),
        Cancel(Const('Отменить')),
        state=NewMinecraftLocationSG.get_coords,
    ),
    Window(
        Format('Отлично, локация добавлена'),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftLocationSG.success,
    ),
    Window(
        Multi(
            Const('Не удалось добавить локацию =('),
        ),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftLocationSG.failure,
    ),
    launch_mode=LaunchMode.SINGLE_TOP
)
