import logging
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

    def __init__(self, *widgets: WidgetSrc, dynamic_keyboard: Callable = None, dynamic_keyboard_decorator: Callable = None, state: State, getter: GetterVariant = None, parse_mode: Optional[ParseMode] = None, disable_web_page_preview: Optional[bool] = None, preview_add_transitions: Optional[List[Keyboard]] = None, preview_data: GetterVariant = None):
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
        self.dynamic_keyboard_decorator = dynamic_keyboard_decorator

        # if there's no any type of dynamic keyboard
        if not (dynamic_keyboard or dynamic_keyboard_decorator):
            raise ValueError('DynamicWindow must have dynamic_keyboard or dynamic_keyboard_decorator')
        
        if dynamic_keyboard and dynamic_keyboard_decorator:
            logging.log(
                logging.INFO,
                'DynamicWindow: dynamic_keyboard will be ignored because dynamic_keyboard_decorator has been provided'
                )


    async def render_kbd(self, data: Dict,
                         manager: DialogManager) -> InlineKeyboardMarkup:
        # TODO: refactor
        
        # if dynamic_keyboard_function needs extra data (e.g. for orm relations)
        if self.dynamic_keyboard_decorator:
            self.dynamic_keyboard = self.dynamic_keyboard_decorator(manager)

        _, self.keyboard, _, _ = ensure_widgets((*self.dynamic_keyboard(), *self.widgets))

        return await super().render_kbd(data, manager)
