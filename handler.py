from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, c
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

        elif call.data.startswith("buy_"):
            # IMPORTANT FIX: dan dik theke 2 bar split korbo
            parts = call.data.rsplit("_", 2)
            category = parts[0].replace("buy_", "")
            name = parts[1].replace("_", " ")
            price = float(parts[2])

            balance = get_balance(user_id)
            if balance >= price:
                update_balance(user_id, -price)
                add_order(user_id, name, price)
                bot.edit_message_text(f"✅ Order Confirmed!\n\nProduct: {name}\nPrice: {price} BDT\nNew Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
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
            bot.edit_message_text("💳 Rocket Personal\n`off ase akon`\n\n1. Number copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "usdt":
            bot.edit_message_text("💲 USDT (TRC20)\n\n`TGE8oPaj7cYP14xuoHTZT19KxwSf12FYoz`\n\n1. Address copy kore payment korun\n2. Payment er por 'Submit Payment' e click korun", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "submit_payment":
            user_state[user_id] = {"step": "amount"}
            bot.send_message(chat_id, "💰 Enter Deposit Amount")

        elif call.data == "wallet":
            bot.edit_message_text(f"👛 Wallet\n💰 Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "orders":
            orders = get_orders(user_id)
            text = "📦 My Orders\nNo orders yet" if not orders else "📦 My Orders\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

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
            support_text = (
                "🆘 Support Center\n\n"
                "কোনো সমস্যা বা প্রশ্ন থাকলে আমাদের সাথে যোগাযোগ করুন।\n\n"
                "💬 Support: @PolasChandra\n"
                "WhatsApp: 01873565112\n"
                "⏰ Available: 24/7\n"
                "⚡ Fast Response • Trusted Support"
            )
            bot.edit_message_text(support_text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "about":
            about_text = (
                "ℹ️ About Proxy Store\n"
                "🚀 Welcome to Proxy Store\n"
                "আপনার বিশ্বস্ত ডিজিটাল সার্ভিস পার্টনার।\n\n"
                "Proxy Store প্রদান করে দ্রুত, নিরাপদ এবং নির্ভরযোগ্য Premium Digital Services। "
                "আমাদের লক্ষ্য হলো গ্রাহকদের জন্য সেরা মানের সার্ভিস ও সহজ অভিজ্ঞতা নিশ্চিত করা।\n\n"
                "📦 Our Services:\n"
                "🔹 Premium VPN Account\n"
                "🔹 High-Speed Proxy\n"
                "🔹 Digital Premium Services\n"
                "✨ Why Choose Us?\n"
                "✅ Instant Delivery System\n"
                "✅ Affordable & Competitive Price\n"
                "✅ Secure & Reliable Service\n"
                "✅ 24/7 Customer Support\n"
                "🔐 আপনার নিরাপত্তা ও সন্তুষ্টিই আমাদের সর্বোচ্চ অগ্রাধিকার।\n\n"
                "❤️ ধন্যবাদ Proxy Store-এর সাথে থাকার জন্য।\n"
                "🤖 Powered by Proxy Store"
            )
            bot.edit_message_text(about_text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "home":
            try:
                bot.edit_message_text(f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
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
