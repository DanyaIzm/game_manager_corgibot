from pony import orm

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from database import UserModel


class UserMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # Если сообщение, то берём инфу о пользователе из сообщения, иначе из каллбэка
        user_info = update.message.from_user if update.message else update.callback_query.from_user

        with orm.db_session:
            # Если пользователь уже есть в БД, то всё хорошо, выходим
            if UserModel.get(id=user_info.id):
                return

            # Если пользователя у нас ещё нет, то добавляем его
            UserModel(
                id=user_info.id,
                username=user_info.username,
                last_name=user_info.last_name,
                first_name=user_info.first_name
                )
