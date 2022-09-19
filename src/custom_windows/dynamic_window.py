from typing import Optional, Callable, Dict, List

from aiogram.dispatcher.filters.state import State
from aiogram.types import (
    InlineKeyboardMarkup, ParseMode
)

from aiogram_dialog.widgets.utils import (
    ensure_widgets, GetterVariant, WidgetSrc
)
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog import Window, DialogManager


class DynamicWindow(Window):
    """ 
    Данный класс нужен для того, чтобы обеспечивать постоянный рендер кнопок при каждом вызове окна.
    Проблема была в том, чтобы получать актуальные данные из базы данных, из которых потом рендерятся кнопки.
    Так как библитека устроена так, что все кнопки и окна создаются при инициализации приложения, то данные берутся именно в этот момент,
    из-за чего невозможно должную обеспечить интерактивность при работе с ботом.
    """

    def __init__(self, *widgets: WidgetSrc, dynamic_keyboard: Callable, state: State, getter: GetterVariant = None, parse_mode: Optional[ParseMode] = None, disable_web_page_preview: Optional[bool] = None, preview_add_transitions: Optional[List[Keyboard]] = None, preview_data: GetterVariant = None):
        super().__init__(
            *widgets,
            state=state,
            getter=getter,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            preview_add_transitions=preview_add_transitions,
            preview_data=preview_data
        )
        self.widgets = widgets
        self.dynamic_keyboard = dynamic_keyboard

    async def render_kbd(self, data: Dict,
                         manager: DialogManager) -> InlineKeyboardMarkup:
        _, self.keyboard, _, _ = ensure_widgets((*self.widgets, *self.dynamic_keyboard()))

        return await super().render_kbd(data, manager)