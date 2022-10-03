from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back

from aiogram.dispatcher.filters.state import StatesGroup, State

from pony import orm

from database import MinecraftLocationModel

from dialogs.common.complete_dialog import complete


class MinecraftLocationSG(StatesGroup):
    main = State()
    coords = State()


async def get_minecraft_location_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().start_data

    return data


async def get_coords_data(dialog_manager: DialogManager, **kwargs):
    location_id = dialog_manager.current_context().start_data.get('location_id')

    with orm.db_session:
        location = MinecraftLocationModel[location_id]

    location_coords = f'{location.x} {location.y} {location.z}'

    return {
        'location_coords': location_coords,
    }



minecraft_location_dialog = Dialog(
    Window(
        Format('Мир -> "{world_name}"\n\nЛокация -> "{location_name}"\n\nКраткое описание:\n{location_description}'),
        SwitchTo(
            Const('Координаты'),
            id='coords',
            state=MinecraftLocationSG.coords
        ),
        Button(
            Const('Назад'),
            id='return_to_all_locations',
            on_click=complete
        ),
        state=MinecraftLocationSG.main
    ),
    Window(
        Format('Координаты локации:\n<code>{location_coords}</code>'),
        Back(
            Const('Назад')
        ),
        parse_mode='HTML',
        getter=get_coords_data,
        state=MinecraftLocationSG.coords
    ),
    getter=get_minecraft_location_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
