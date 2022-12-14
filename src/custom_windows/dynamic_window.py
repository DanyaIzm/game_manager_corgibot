import logging
from typing import Optional, Callable, Dict, List

from aiogram.dispatcher.filters.state import State
from aiogram.types import (
    InlineKeyboardMarkup, ParseMode
)

from aiogram_dialog.widgets.utils import (
    ensure_keyboard, GetterVariant, WidgetSrc
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

    def __init__(self, *widgets: WidgetSrc, dynamic_keyboard: Callable = None, dynamic_keyboard_HOF: Callable = None, state: State, getter: GetterVariant = None, parse_mode: Optional[ParseMode] = None, disable_web_page_preview: Optional[bool] = None, preview_add_transitions: Optional[List[Keyboard]] = None, preview_data: GetterVariant = None):
        """
        dynamic_heyboard_HOF должна создавать функцию, генирирующую клавитуру.
        Функция высшего порядка нужна для тех случаев, когда для генерирования клавиатуры
        необходимо получить определённые данные (e.g. для поддержания отношений ORM).
        """
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
        # saves static keyboard to rerender all keyabord when update
        self.static_keyboard = self.keyboard
        self.dynamic_keyboard = dynamic_keyboard
        self.dynamic_keyboard_HOF = dynamic_keyboard_HOF

        # if there's no any type of dynamic keyboard
        if not (dynamic_keyboard or dynamic_keyboard_HOF):
            raise ValueError('DynamicWindow must have dynamic_keyboard or dynamic_keyboard_HOF')
        
        if dynamic_keyboard and dynamic_keyboard_HOF:
            logging.log(
                logging.INFO,
                'DynamicWindow: dynamic_keyboard will be ignored because dynamic_keyboard_HOF has been provided'
                )


    async def render_kbd(self, data: Dict,
                         manager: DialogManager) -> InlineKeyboardMarkup:
        # if dynamic_keyboard_function needs extra data (e.g. for orm relations)
        if self.dynamic_keyboard_HOF:
            self.dynamic_keyboard = self.dynamic_keyboard_HOF(manager)

        self.keyboard = ensure_keyboard((*self.dynamic_keyboard(), self.static_keyboard))

        return await super().render_kbd(data, manager)
