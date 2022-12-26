from aiogram import types
from aiogram.types import CallbackQuery
from bson import ObjectId

from keyboards.inline.tonality_markup import tonality_keyboard
from loader import dp
from utils.db_api.mongodb import posts


@dp.message_handler(text='Начать разметку')
async def start_marking(message: types.Message):
    posts_count = posts.count_documents({})
    if posts_count == 0:
        await message.answer('<b>База не заполнена постами</b>')
        return

    post = posts.find_one({'tone': None})
    if not post:
        await message.answer('<b>Все посты уже размечены</b>')
        return

    post_id = post['_id']
    await message.answer('<b>Текст поста:</b>\n'
                         f'{post["text"]}',
                         reply_markup=tonality_keyboard(post_id))


@dp.callback_query_handler(text_contains='tone')
async def choose_tonality(call: CallbackQuery):
    user_id = call.from_user.id
    data = call.data.split(':')
    post_id = ObjectId(data[1])
    tone = data[2]
    is_marked = posts.find_one({'_id': post_id,
                                'tone': {'$ne': None}})
    if not is_marked:
        posts.update_one({'_id': post_id}, {'$set': {'user_id': user_id,
                                                     'tone': tone}})
    else:
        await call.answer('Этот пост уже разметил другой пользователь')

    tone = posts.find_one({'_id': post_id})['tone']
    text = call.message.html_text
    await call.message.delete_reply_markup()
    await call.message.edit_text(f'{text}\n\n'
                                 f'<b>Выбранная тональность:</b> {tone}')

    # отправка нового поста
    post = posts.find_one({'tone': None})
    if not post:
        await call.message.answer('<b>Все посты уже размечены</b>')
        return

    post_id = post['_id']
    await call.message.answer('<b>Текст поста:</b>\n'
                              f'{post["text"]}',
                              reply_markup=tonality_keyboard(post_id))
