from aiogram import types
from aiogram.types import CallbackQuery
from bson import ObjectId

from keyboards.inline.tonality_markup import tonality_keyboard
from loader import dp
from utils.db_api.mongodb import posts, posts_users


@dp.message_handler(text='Начать разметку')
async def start_marking(message: types.Message):
    user_id = message.from_user.id
    posts_count = posts.count_documents({})
    if posts_count == 0:
        await message.answer('<b>База не заполнена постами</b>')
        return

    all_posts = posts.find()
    for post in all_posts:
        post_id = post['_id']
        is_marked = posts_users.find_one({'user_id': user_id,
                                          'post_id': post_id})
        if is_marked:
            continue
        else:
            await message.answer('<b>Текст поста:</b>\n'
                                 f'{post["text"]}',
                                 reply_markup=tonality_keyboard(post_id))
            break
    else:
        await message.answer('<b>Вы отметили все посты</b>')


@dp.callback_query_handler(text_contains='tone')
async def choose_tonality(call: CallbackQuery):
    user_id = call.from_user.id
    data = call.data.split(':')
    post_id = ObjectId(data[1])
    tone = data[2]
    posts_users.insert_one({'post_id': post_id,
                            'user_id': user_id,
                            'tone': tone})
    text = call.message.html_text
    await call.message.delete_reply_markup()
    await call.message.edit_text(f'{text}\n\n'
                                 f'<b>Выбранная тональность:</b> {tone}')

    all_posts = posts.find()
    for post in all_posts:
        post_id = post['_id']
        is_marked = posts_users.find_one({'user_id': user_id,
                                          'post_id': post_id})
        if is_marked:
            continue
        else:
            await call.message.answer('<b>Текст поста:</b>\n'
                                      f'{post["text"]}',
                                      reply_markup=tonality_keyboard(post_id))
            break
    else:
        await call.message.answer('<b>Вы отметили все посты</b>')
