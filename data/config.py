from environs import Env

# инициализируем файл .env
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # токен бота
ADMINS = env.list("ADMINS")  # список из ID админов
IP = env.str("ip")  # IP сервера, на котором запущен бот

PASS_PHRASE = env.str("PASS_PHRASE")  # парольная фрза
