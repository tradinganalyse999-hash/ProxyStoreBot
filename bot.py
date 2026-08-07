import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
    from handler import register_handlers
    register_handlers()
