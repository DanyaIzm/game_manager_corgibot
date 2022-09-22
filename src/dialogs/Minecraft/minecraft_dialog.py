from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import LaunchMode
from aiogram_dialog.widgets.text import Format, Const, Multi
from aiogram_dialog.widgets.kbd import Cancel, Start, SwitchTo, Back, Button, Row

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types

from pony import orm

from database import MinecraftWorldModel

from custom_windows.dynamic_window import DynamicWindow

from dialogs.Minecraft.new_world_dialog import NewMinecraftWorldSG
from dialogs.Minecraft.minecraft_locaions_dialog import MinecraftLocationsSG


class MainSG(StatesGroup):
    main = State()

    select_world = State()
    delete_world = State()


# Main data getter
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


def render_locations_keyboard_HOF(world_name, world_id):
    """
    HOF для того, чтобы каждая кнопка добавляла в контекст данные о своём мире
    """
    async def wrapped(callback: types.CallbackQuery, button: Button, manager: DialogManager):
        await manager.update({
            'world_name': world_name,
            'world_id': world_id
        })

        await manager.dialog().back()

    return wrapped


def render_worlds_keyboard():
    with orm.db_session:
        buttons = [
            Button(
                Const(world.name),
                str(world.id),
                on_click=render_locations_keyboard_HOF(world.name, world.id)
            )
            for world in MinecraftWorldModel.select()
        ]

    return buttons
    

async def delete_world(callback: types.CallbackQuery, button: Button, manager: DialogManager):
    world_id = manager.current_context().dialog_data['world_id']

    with orm.db_session:
        MinecraftWorldModel[world_id].delete()
    
    await manager.dialog().switch_to(MainSG.main)


async def setup_start_locations_data(callback: types.CallbackQuery, start_button: Start, manager: DialogManager):
    data = manager.current_context().dialog_data

    # setup world data into the start button
    start_button.start_data = data



minecraft_dialog = Dialog(
    Window(
        Multi(
            Format('Игра {game}\n'),
            Format('Выбран мир: {world_name}', when=lambda data, w, m: data.get('world_name')),
        ),
        Start(
            Const('Локации'),
            id='locations',
            state=MinecraftLocationsSG.main,
            when=lambda data, w, m: data.get('world_name'),
            on_click=setup_start_locations_data,
        ),
        Row(
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
            SwitchTo(
                Const('Удалить мир'),
                id='delete_world',
                state=MainSG.delete_world,
                when=lambda data, w, m: data.get('world_name'),
            ),
            id='world_settings_row'
        ),
        Cancel(Const('В главное меню')),
        state=MainSG.main,
    ),
    # Окно выбора мира
    DynamicWindow(
        Const('Выберите мир из существующих: '),
        Back(Const('Назад')),
        dynamic_keyboard=render_worlds_keyboard,
        state=MainSG.select_world
    ),
    # Окно удаления мира
    Window(
        Const('Вы уверены?'),
        Row(
            Back(Const('Нет')),
            Button(
                Const('Да'),
                id='delete_world',
                on_click=delete_world
            ),
        ),
        state=MainSG.delete_world
    ),
    getter=get_minecraft_dialog_data,
    launch_mode=LaunchMode.SINGLE_TOP
)
