from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from data.config import PASS_PHRASE
from keyboards.default.main_menu import main_keyboard
from utils.db_api.mongodb import users


class ThrottlingMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        await call.answer()

    async def on_pre_process_message(self, message: Message, data: dict):
        user_id = message.from_user.id
        name = message.from_user.full_name
        username = message.from_user.username
        is_user = users.find_one({'_id': user_id})

        # если является пользователем (то есть вводил пароль ранее), то разрешаем использование бота
        if is_user:
            return True

        # иначе, выполняем проверку на отправку пароля
        text = message.text
        if text == PASS_PHRASE:
            await message.answer(text='<b>Вы успешно авторизовались в боте!</b>',
                                 reply_markup=main_keyboard)
            users.insert_one(
                {'_id': message.from_user.id,
                 'name': name,
                 'username': username,
                 'date': message.date})
        else:
            await message.answer('<b>Введите парольную для взаимодействия с ботом</b>')
            raise CancelHandler()
