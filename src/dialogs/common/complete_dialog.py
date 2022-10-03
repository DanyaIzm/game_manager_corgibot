from aiogram import types
from aiogram.dispatcher.filters.state import State

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def complete(callback: types.CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()


async def complete_and_reset_dialog(callback: types.CallbackQuery, button: Button, manager: DialogManager):
    # complete current dialog
    await complete(callback, button, manager)

    context = manager.current_context()

    data = {}
    data.update(context.dialog_data)
    data.update(context.start_data)

    state = manager.dialog().dialog.states_group().main

    # start last dialog again
    await manager.start(state=state, data=data)
