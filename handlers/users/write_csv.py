import csv

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from utils.db_api.mongodb import posts, users


@dp.message_handler(Command('csv'))
async def write_csv(message: Message):
    with open('data/posts.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Пользователь', 'Тональность', 'Текст'])
        for post in posts.find({'tone': {'$ne': None}}):
            user = users.find_one({'_id': post['user_id']})
            name = user['name']
            writer.writerow([f"{name} ({post['user_id']})", post['tone'], post['text']])

    doc = open('data/posts.csv', 'rb')
    await message.answer_document(doc)
