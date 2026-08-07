import telebot
from config import BOT_TOKEN
from handler import register_handlers

bot = telebot.TeleBot(BOT_TOKEN)
register_handlers(bot)
