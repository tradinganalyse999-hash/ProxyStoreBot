from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, c, conn
from bot import bot
import re

REFERRAL_BONUS = 0.50 # 1 refer e koto diba

def register_handlers():

    @bot.message_handler(commands=["start"])
    def start(message):
        user_id = message.from_user.id
        args = message.text.split()
        referred_by = None

        # Refer check: /start ref12345
        if len(args) > 1 and args[1].startswith("ref"):
            try:
                referred_by = int(args[1].replace("ref", ""))
            except: pass

        create_user(user_id, referred_by) # referred_by pathay dilam

        # Jodi notun user hoy ebong refer hoy
        if referred_by and referred_by!= user_id:
            # refer kora user ke bonus dao
            update_balance(referred_by, REFERRAL_BONUS)
            c.execute("UPDATE users SET referral_count = referral_count + 1, total_referral_earning = total_referral_earning +? WHERE user_id =?", (REFERRAL_BONUS, referred_by))
            conn.commit()
            try:
                bot.send_message(referred_by, f"🎉 Congratulations!\n\n1 New Referral Joined!\nYou got {REFERRAL_BONUS} BDT bonus.\nNew Balance: {get_balance(referred_by)} BDT")
            except: pass

        bot_username = bot.get_me().username
        refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"
        markup = main_menu()
        markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
        text = f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI\n📌 Refer & Earn: {REFERRAL_BONUS} BDT per referral"
        bot.send_message(message.chat.id, text, reply_markup=markup)

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
        bot_username = bot.get_me().username
        refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"

        if call.data == "shop":
            try:
                bot.edit_message_text("🛒 Select Category", chat_id=chat_id, message_id=msg_id, reply_markup=shop_menu())
            except: pass
        elif call.data == "vpn_list":
            bot.edit_message_text("🌐 VPN Products", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("vpn"))
        elif call.data == "proxy_list":
            bot.edit_message_text("🌍 Proxy Products", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("proxy"))
        elif call.data == "gmail_list":
            bot.edit_message_text("📧 Gmail Products", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("gmail"))
        elif call.data == "outlook_list":
            bot.edit_message_text("📮 Outlook Products", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("outlook"))
        elif call.data == "hotmail_list":
            bot.edit_message_text("📬 Hotmail Products", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("hotmail"))

        # NOTUN: Refer & Earn with Count
        elif call.data == "refer":
            c.execute("SELECT referral_count, total_referral_earning FROM users WHERE user_id =?", (user_id,))
            data = c.fetchone()
            ref_count = data[0] if data else 0
            ref_earn = data[1] if data else 0.0

            text = f"""📌 *Refer & Earn*

💰 Get *{REFERRAL_BONUS} BDT* for each successful referral.

📊 *Your Stats:*
👥 Total Referrals: *{ref_count}*
💵 Total Earned: *{ref_earn} BDT*

🔗 *Your Link:*
`{refer_link}`

👥 *Invite friends.*
💵 *Earn instantly.*"""
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup, parse_mode="Markdown")

        elif call.data.startswith("buy_"):
            parts = call.data.rsplit("_", 2)
            name = parts[1].replace("_", " ")
            price = float(parts[2])
            balance = get_balance(user_id)
            if balance >= price:
                update_balance(user_id, -price)
                add_order(user_id, name, price)
                markup = main_menu()
                markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
                bot.edit_message_text(f"✅ Order Confirmed!\n\nProduct: {name}\nPrice: {price} BDT\nNew Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
                bot.send_message(ADMIN_ID, f"🛒 New Order\nUser: {user_id}\nProduct: {name}\nPrice: {price} BDT")
            else:
                bot.edit_message_text(f"❌ Not Enough Balance\nYour Balance: {balance} BDT\nRequired: {price} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

        elif call.data == "deposit":
            bot.edit_message_text("💰 Deposit Balance\nSelect Payment Method", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())
        elif call.data == "bkash":
            bot.edit_message_text("💳 bKash Personal\n`01603940061`\n\n1. Number copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "nagad":
            bot.edit_message_text("💳 Nagad Personal\n`01603940061`\n\n1. Number copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "rocket":
            bot.edit_message_text("💳 Rocket Personal\n`01603940061`\n\n1. Number copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "usdt":
            bot.edit_message_text("💲 USDT (TRC20)\n\n`TGE8oPaj7cYP14xuoHTZT19KxwSf12FYoz`\n\n1. Address copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "submit_payment":
            user_state[user_id] = {"step": "amount"}
            bot.send_message(chat_id, "💰 Enter Deposit Amount")

        elif call.data == "wallet":
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
            bot.edit_message_text(f"👛 Wallet\n💰 Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "orders":
            orders = get_orders(user_id)
            text = "📦 My Orders\nNo orders yet" if not orders else "📦 My Orders\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)

        elif call.data == "admin_add_balance":
            if user_id!= ADMIN_ID: return
            bot.send_message(chat_id, "👤 User er Telegram ID dao")
            user_state[user_id] = {"step": "admin_user_id"}
        elif call.data == "admin_orders":
            if user_id!= ADMIN_ID: return
            c.execute("SELECT id, user_id, product, price, status FROM orders ORDER BY id DESC LIMIT 20")
            orders = c.fetchall()
            text = "📦 No orders yet" if not orders else "📦 Last 20 Orders\n"+"\n".join([f"ID: {x[0]} | User: {x[1]}\nProduct: {x[2]}\nPrice: {x[3]} BDT | {x[4]}\n" for x in orders])
            bot.send_message(chat_id, text)
        elif call.data == "admin_pending":
            if user_id!= ADMIN_ID: return
            c.execute("SELECT id, user_id, product, price FROM orders WHERE status='Pending' ORDER BY id DESC")
            orders = c.fetchall()
            if not orders:
                bot.send_message(chat_id, "✅ No Pending Orders")
                return
            for o in orders:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("✅ Approve", callback_data=f"approve_{o[0]}"))
                bot.send_message(chat_id, f"🛒 Order ID: {o[0]}\nUser: {o[1]}\nProduct: {o[2]}\nPrice: {o[3]} BDT", reply_markup=markup)

        elif call.data.startswith("approve_"):
            if user_id!= ADMIN_ID: return
            order_id = int(call.data.split("_")[1])
            bot.send_message(chat_id, f"📦 Enter Product Code for Order {order_id}")
            user_state[user_id] = {"step": "admin_code", "order_id": order_id}

        elif call.data == "support":
            support_text = "🆘 Support Center\n💬 Support: @PolasChandra\nWhatsApp: 01873565112\n⏰ Available: 24/7"
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
            bot.edit_message_text(support_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "about":
            about_text = "ℹ️ About Proxy Store\n🚀 Welcome to Proxy Store\nPremium Digital Services Provider"
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
            bot.edit_message_text(about_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "home":
            try:
                markup = main_menu()
                markup.add(InlineKeyboardButton("🚀 Refer & Earn", callback_data="refer"))
                bot.edit_message_text(f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
            except: pass

        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in user_state)
    def process_all(message):
        user_id = message.from_user.id
        state = user_state[user_id]
        if state["step"] == "admin_user_id":
            state["target_id"] = int(message.text)
            state["step"] = "admin_amount"
            bot.send_message(message.chat.id, "💰 Koto BDT add korba?")
        elif state["step"] == "admin_amount":
            amount = float(message.text)
            target_id = state["target_id"]
            update_balance(target_id, amount)
            bot.send_message(message.chat.id, f"✅ {target_id} ke {amount} BDT add kora hoise\nNew Balance: {get_balance(target_id)} BDT")
            bot.send_message(target_id, f"🎉 Admin apnar account e {amount} BDT add korse")
            del user_state[user_id]
        elif state["step"] == "admin_code":
            order_id = state["order_id"]
            code = message.text
            order = get_order_by_id(order_id)
            update_order_status(order_id, "Approved")
            bot.send_message(order[1], f"✅ Your Order Approved!\n\nProduct: {order[2]}\nCode: `{code}`\nEnjoy!", parse_mode="Markdown")
            bot.send_message(message.chat.id, f"✅ Order {order_id} Approved and code sent to user")
            del user_state[user_id]
        elif state["step"] == "amount":
            state["amount"] = message.text
            state["step"] = "trx"
            bot.send_message(message.chat.id, "🧾 Send Transaction ID / TrxID")
        elif state["step"] == "trx":
            bot.send_message(ADMIN_ID,f"💰 New Deposit Request\n👤 {message.from_user.first_name}\n🆔 {user_id}\nAmount: {state['amount']} BDT\nTRX ID: {message.text}")
            bot.send_message(message.chat.id,"✅ Deposit Request Sent. Admin will approve in 5-10 min.")
            del user_state[user_id]
