from pprint import pprint

import pymongo

# подключаемся к базе данных

db_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = db_client['bot_marking']

#  инициализируем коллекции
users = db['users']
posts = db['posts']
tonalities = db['tonalities']
posts_users = db['posts_users']

# import csv
# with open('mob_positive_12.csv', newline='', encoding='utf-8') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for index, row in enumerate(spamreader):
#         print(index)
#         text = ' '.join(row).strip()
#         if len(text) > 1:
#             print(text)
#             posts.insert_one({'text': text,
#                               'default_tone': 'Позитивная'})
