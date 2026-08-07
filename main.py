from bot import bot
from handler import register_handler

register_handlers()

print("✅ ProxyStore BOT Started")
bot.infinity_polling(timeout=30, skip_pending=True)
