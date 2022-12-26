from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.mongodb import tonalities


def tonality_keyboard(post_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for tonality in tonalities.find():
        name = tonality['name']
        keyboard.insert(InlineKeyboardButton(text=name, callback_data=f'tone:{post_id}:{name}'))
    return keyboard
