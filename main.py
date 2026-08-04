from bot import bot
from handlers import register_handlers

register_handlers()

print("✅ ProxyStore BOT Started")
bot.infinity_polling(timeout=30, skip_pending=True)