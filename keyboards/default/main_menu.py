from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Начать разметку'),
        ],
    ],
    resize_keyboard=True)
