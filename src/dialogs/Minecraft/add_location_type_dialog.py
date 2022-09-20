from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftLocationTypeModel

from dialogs.common.complete_dialog import complete


class NewMinecraftLocationTypeSG(StatesGroup):
    get_name = State()
    success = State()
    failure = State()


async def location_type_name_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    location_type_name = message.text

    try:
        location_type_name = location_type_name.strip()
    except:
        await message.answer('Некорректное название мира')
        return await dialog.switch_to(NewMinecraftLocationTypeSG.get_name, manager)

    try:
        with orm.db_session:
            # Add new locaiton type into the database
            MinecraftLocationTypeModel(name=location_type_name)
    except:
        return await dialog.switch_to(NewMinecraftLocationTypeSG.failure)
    else:
        return await dialog.switch_to(NewMinecraftLocationTypeSG.success)



new_minecraft_location_type_dialog = Dialog(
    Window(
        Const('Введите название типа локации'),
        MessageInput(location_type_name_input),
        Cancel(Const('Отменить')),
        state=NewMinecraftLocationTypeSG.get_name,
    ),
    Window(
        Format('Отлично, тип локации добавлен'),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftLocationTypeSG.success,
    ),
    Window(
        Const('Не удалось добавить тип локации =('),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftLocationTypeSG.failure,
    ),
    launch_mode=LaunchMode.SINGLE_TOP
)
