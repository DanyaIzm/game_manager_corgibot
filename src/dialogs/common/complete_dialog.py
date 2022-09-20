from aiogram import types

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def complete(callback: types.CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()
