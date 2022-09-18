from pony import orm

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from database import UserModel


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()


    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Срабатывает при обработке сообщения или каллбэка
        
        with orm.db_session:
            # Достём пользователя из базы данных
            user = UserModel[message.from_user.id]

            # Если пользователь на админ, то не даём ему пользоваться ботом
            if not user.is_admin:
                
                raise CancelHandler

    # Используем тот же метод для проверки прав пользователя для каллбэков
    on_pre_process_callback_query = on_pre_process_message
