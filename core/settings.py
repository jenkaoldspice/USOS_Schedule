from starlette.config import Config
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
config = Config(".env")

TOKEN = config("TOKEN", cast=str, default="")
LOGIN = config("LOGIN", cast=str, default="")
PASSWORD = config("PASSWORD", cast=str, default="")
headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117'
    }

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
