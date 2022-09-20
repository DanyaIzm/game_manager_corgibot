from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel

from dialogs.common.complete_dialog import complete


class NewMinecraftWorldSG(StatesGroup):
    get_name = State()
    get_version = State()
    get_description = State()
    success = State()
    failure = State()


async def world_name_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    world_name = message.text

    try:
        world_name = world_name.strip()
    except:
        await message.answer('Некорректное название мира')
        return await dialog.switch_to(NewMinecraftWorldSG.get_name, manager)

    await manager.update({
        'name': world_name
    })

    return await dialog.next(manager)


async def world_version_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    version = message.text

    try:
        version = version.strip()
    except:
        await message.answer('Некорректная версия')
        return await dialog.switch_to(NewMinecraftWorldSG.get_version, manager)

    await manager.update({
        'version': version
    })

    return await dialog.next(manager)


async def world_description_input(message: types.Message, dialog: Dialog, manager: DialogManager):
    description = message.text

    try:
        description = description.strip()
    except:
        message.answer('Ошибка в описании мира')
        return await dialog.switch_to(NewMinecraftWorldSG.get_description, manager)

    await manager.update({
        'description': description
    })

    try:
        dialog_data = manager.current_context().dialog_data
        with orm.db_session:
            new_world = MinecraftWorldModel(
                name=dialog_data['name'],
                version=dialog_data['version'],
                description=dialog_data['description'],
                )
    except:
        return await dialog.switch_to(NewMinecraftWorldSG.failure)
    else:
        return await dialog.switch_to(NewMinecraftWorldSG.success)




new_minecraft_world_dialog = Dialog(
    Window(
        Const('Введите название мира'),
        MessageInput(world_name_input),
        Cancel(Const('Отменить')),
        state=NewMinecraftWorldSG.get_name,
    ),
    Window(
        Const('Введите версию игры'),
        MessageInput(world_version_input),
        Cancel(Const('Отменить')),
        state=NewMinecraftWorldSG.get_version,
    ),
    Window(
        Const('Введите краткое описание мира'),
        MessageInput(world_description_input),
        Cancel(Const('Отменить')),
        state=NewMinecraftWorldSG.get_description,
    ),
    Window(
        Format('Отлично, мир успешно добавлен'),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftWorldSG.success,
    ),
    Window(
        Const('Не удалось добавить мир =('),
        Button(
            Const('Ок'),
            id='ok',
            on_click=complete
        ),
        state=NewMinecraftWorldSG.failure,
    ),
    launch_mode=LaunchMode.SINGLE_TOP
)
