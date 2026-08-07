from bot import bot
from handler import register_handlers

register_handlers(bot)

print("✅ ProxyStore BOT Started")
bot.infinity_polling(timeout=30, skip_pending=True)
