from bot import bot
from telebot import types

# sob button er handler ekhanei thakbe

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot_username = bot.get_me().username
    refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"

    # Button banano
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

# Baki button gulo
@bot.message_handler(func=lambda message: message.text == "🛒 Shop")
def shop(message):
    bot.send_message(message.chat.id, "🛒 Shop coming soon!")

@bot.message_handler(func=lambda message: message.text == "💰 Deposit")
def deposit(message):
    bot.send_message(message.chat.id, "💰 Deposit coming soon!")

@bot.message_handler(func=lambda message: message.text == "👛 Wallet")
def wallet(message):
    bot.send_message(message.chat.id, "👛 Wallet: 0.00 BDT")

@bot.message_handler(func=lambda message: message.text == "📦 Orders")
def orders(message):
    bot.send_message(message.chat.id, "📦 No orders yet!")

@bot.message_handler(func=lambda message: message.text == "🆘 Support")
def support(message):
    bot.send_message(message.chat.id, "🆘 Contact @admin for support")

@bot.message_handler(func=lambda message: message.text == "ℹ️ About")
def about(message):
    bot.send_message(message.chat.id, "ℹ️ ProxyStore AI - Best IP Provider Bot")
