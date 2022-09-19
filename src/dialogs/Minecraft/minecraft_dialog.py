from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog.widgets.kbd import Cancel, Start, SwitchTo, Back, Button

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel

from custom_windows.dynamic_window import DynamicWindow

from dialogs.Minecraft.new_world_dialog import NewMinecraftWorldSG


class MainSG(StatesGroup):
    main = State()

    select_world = State()

    in_world = State()


async def get_minecraft_dialog_data(dialog_manager: DialogManager, **kwargs):
    context = dialog_manager.current_context()
    data = context.start_data
    data.update(context.dialog_data)

    if data.get('world_id'):
        with orm.db_session:
            if not MinecraftWorldModel.get(id=data['world_id']):
                del data['world_id']
                del data['world_name']

    return data


def switch_world_decorator(world_name, world_id):
    async def wrapped(callback: types.CallbackQuery, button: Button, manager: DialogManager):
        await manager.update({
            'world_name': world_name,
            'world_id': world_id
        })

        await manager.dialog().back()

    return wrapped


def render_world_buttons():
    with orm.db_session:
        buttons = [
            Button(
                Const(world.name),
                str(world.id),
                on_click=switch_world_decorator(world.name, world.id)
            )
            for world in MinecraftWorldModel.select()
        ]

    return buttons


minecraft_dialog = Dialog(
    Window(
        Multi(
            Format('Игра {game}\n'),
            Format('Выбран мир {world_name}', when=lambda data, w, m: data.get('world_name')),
        ),
        Start(
            Const('Добавить мир'),
            id='new_world',
            state=NewMinecraftWorldSG.get_name,
        ),
        SwitchTo(
            Const('Выбрать мир'),
            id='select_world',
            state=MainSG.select_world,
        ),
        Cancel(Const('В главное меню')),
        state=MainSG.main,
    ),
    DynamicWindow(
        Const('Выберите мир из существующих: '),
        Back(Const('Назад')),
        dynamic_keyboard=render_world_buttons,
        state=MainSG.select_world
    ),
    getter=get_minecraft_dialog_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
