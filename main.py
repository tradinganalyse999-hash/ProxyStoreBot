from bot import bot
from handlers import register_handlers
from telebot import types

register_handlers()

# /start command handle korar jonno
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot_username = bot.get_me().username
    refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"

    # Button banano - ReplyKeyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("🛒 Shop"), types.KeyboardButton("💰 Deposit"))
    keyboard.row(types.KeyboardButton("👛 Wallet"), types.KeyboardButton("📦 Orders"))
    keyboard.row(types.KeyboardButton("🆘 Support"), types.KeyboardButton("ℹ️ About"))
    keyboard.row(types.KeyboardButton("🚀 Refer & Earn")) # <-- Notun button

    text = f"""👋 *Welcome to ProxyStore AI*

🚀 *Refer & Earn*

💰 Get *0.50 BDT* for each successful referral.

🔗 Share your referral link.
👥 Invite friends.
💵 Earn instantly.

*Your Referral Link:*
`{refer_link}`"""

    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="Markdown")

# Jokhon "Refer & Earn" button e click korbe
@bot.message_handler(func=lambda message: message.text == "🚀 Refer & Earn")
def refer_button(message):
    user_id = message.from_user.id
    bot_username = bot.get_me().username
    refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"

    text = f"""🚀 *Refer & Earn*

💰 Get *0.50 BDT* for each successful referral.

🔗 Your Link:
`{refer_link}`

👥 Invite friends.
💵 Earn instantly."""
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("✅ ProxyStore BOT Started")
bot.infinity_polling(timeout=30, skip_pending=True)
