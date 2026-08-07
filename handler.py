from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu, quantity_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, c, get_all_users
from bot import bot

def register_handlers(bot):

    @bot.message_handler(commands=["start"])
    def start(message):
        create_user(message.from_user.id)
        bot.send_message(message.chat.id, f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI", reply_markup=main_menu())

    @bot.message_handler(commands=["admin"])
    def admin(message):
        if message.from_user.id!= ADMIN_ID:
            bot.reply_to(message, "❌ Access Denied")
            return
        bot.send_message(message.chat.id, "👑 Admin Panel", reply_markup=admin_buttons())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        msg_id = call.message.message_id
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        if call.data == "shop":
            try:
                bot.edit_message_text("🛒 Select Category", chat_id=chat_id, message_id=msg_id, reply_markup=shop_menu())
            except: pass

        elif call.data == "admin_broadcast":
            if user_id!= ADMIN_ID: return
            bot.send_message(chat_id, "📢 Broadcast message likhe pathao. Sob user pabe.")
            user_state[user_id] = {"step": "broadcast_msg"}

        elif call.data == "wallet":
            bot.edit_message_text(f"👛 Wallet\n💰 Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "home":
            try:
                bot.edit_message_text(f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
            except: pass

        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in user_state)
    def process_all(message):
        user_id = message.from_user.id
        state = user_state[user_id]
        if state["step"] == "broadcast_msg":
            message_text = message.text
            all_users = get_all_users()
            sent = 0
            for uid in all_users:
                try:
                    bot.send_message(uid, f"📢 **Notice from {BOT_NAME}**\n\n{message_text}", parse_mode="Markdown")
                    sent += 1
                except:
                    pass
            bot.send_message(message.chat.id, f"✅ Broadcast Done!\n{sent} jon user ke pathano hoise")
            del user_state[user_id]
