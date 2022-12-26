from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_menu import main_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=f"Нажмите на кнопку <b>«Начать разметку»</b> для начала работы",
                         reply_markup=main_keyboard)
