from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, add_referral, activate_referral_bonus, get_refer_stats, c, conn
from bot import bot
import re

REFERRAL_BONUS = 0.50
MIN_DEPOSIT_FOR_BONUS = 10 # 10 tk deposit korle bonus active hobe

def register_handlers():

    @bot.message_handler(commands=["start"])
    def start(message):
        user_id = message.from_user.id
        args = message.text.split()
        referred_by = None

        if len(args) > 1 and args[1].startswith("ref"):
            try:
                referred_by = int(args[1].replace("ref", ""))
            except: pass

        create_user(user_id, referred_by)

        # Refer add koro kintu bonus ekhoni diba na
        if referred_by and referred_by!= user_id:
            add_referral(referred_by, user_id)

        bot_username = bot.get_me().username
        refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"
        markup = main_menu()
        markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
        text = f"🤖 {BOT_NAME}\nProxyStore AI তে স্বাগতম ❤️\n📌 রেফার বোনাস: {REFERRAL_BONUS} BDT\n\nশর্ত: আপনার রেফার করা ইউজার ১০ টাকা ডিপোজিট করলে বোনাস পাবেন"
        bot.send_message(message.chat.id, text, reply_markup=markup)

    @bot.message_handler(commands=["admin"])
    def admin(message):
        if message.from_user.id!= ADMIN_ID:
            bot.reply_to(message, "❌ Access Denied")
            return
        bot.send_message(message.chat.id, "👑 Admin Panel", reply_markup=admin_buttons())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        msg_id = call.message_id
        chat_id = call.message.chat.id
        user_id = call.from_user.id
        bot_username = bot.get_me().username
        refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"

        if call.data == "shop":
            try: bot.edit_message_text("🛒 ক্যাটাগরি সিলেক্ট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=shop_menu())
            except: pass
        elif call.data == "vpn_list":
            bot.edit_message_text("🌐 VPN প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("vpn"))
        elif call.data == "proxy_list":
            bot.edit_message_text("🌍 Proxy প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("proxy"))
        elif call.data == "gmail_list":
            bot.edit_message_text("📧 Gmail প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("gmail"))
        elif call.data == "outlook_list":
            bot.edit_message_text("📮 Outlook প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("outlook"))
        elif call.data == "hotmail_list":
            bot.edit_message_text("📬 Hotmail প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("hotmail"))

        elif call.data == "refer":
            ref_count, ref_earn = get_refer_stats(user_id)
            text = f"""📌 *রেফার & আর্ন*

💰 প্রতি সফল রেফারে পাবেন *{REFERRAL_BONUS} BDT*

📊 *আপনার স্ট্যাটস:*
👥 মোট রেফার: *{ref_count}*
💵 মোট আয়: *{ref_earn} BDT*

🔗 *আপনার লিংক:*
`{refer_link}`

*শর্ত: রেফার করা ইউজারকে ১০ টাকা ডিপোজিট করতে হবে*"""
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
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
                markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
                bot.edit_message_text(f"✅ অর্ডার কনফার্ম!\n\nপ্রোডাক্ট: {name}\nদাম: {price} BDT\nনতুন ব্যালেন্স: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
                bot.send_message(ADMIN_ID, f"🛒 New Order\nUser: {user_id}\nProduct: {name}\nPrice: {price} BDT")
            else:
                bot.edit_message_text(f"❌ ব্যালেন্স নেই\nআপনার ব্যালেন্স: {balance} BDT\nপ্রয়োজন: {price} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

        elif call.data == "deposit":
            bot.edit_message_text("💰 ডিপোজিট করুন\nপেমেন্ট মেথড সিলেক্ট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())
        elif call.data == "bkash":
            bot.edit_message_text("💳 bKash Personal\n`01603940061`\n\n1. নাম্বারে টাকা পাঠান\n2. এরপর 'পেমেন্ট সাবমিট' করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "nagad":
            bot.edit_message_text("💳 Nagad Personal\n`01603940061`\n\n1. নাম্বারে টাকা পাঠান\n2. এরপর 'পেমেন্ট সাবমিট' করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "rocket":
            bot.edit_message_text("💳 Rocket Personal\n`01603940061`\n\n1. নাম্বারে টাকা পাঠান\n2. এরপর 'পেমেন্ট সাবমিট' করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "usdt":
            bot.edit_message_text("💲 USDT (TRC20)\n\n`TGE8oPaj7cYP14xuoHTZT19KxwSf12FYoz`\n\n1. Address এ পাঠান\n2. এরপর 'পেমেন্ট সাবমিট' করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")
        elif call.data == "submit_payment":
            user_state[user_id] = {"step": "amount"}
            bot.send_message(chat_id, "💰 ডিপোজিট এর পরিমাণ লিখুন")

        elif call.data == "wallet":
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
            bot.edit_message_text(f"👛 ওয়ালেট\n💰 ব্যালেন্স: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "orders":
            orders = get_orders(user_id)
            text = "📦 আমার অর্ডার\nকোন অর্ডার নেই" if not orders else "📦 আমার অর্ডার\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)

        elif call.data == "admin_add_balance":
            if user_id!= ADMIN_ID: return
            bot.send_message(chat_id, "👤 ইউজার এর Telegram ID দিন")
            user_state[user_id] = {"step": "admin_user_id"}
        elif call.data == "admin_orders":
            if user_id!= ADMIN_ID: return
            c.execute("SELECT id, user_id, product, price, status FROM orders ORDER BY id DESC LIMIT 20")
            orders = c.fetchall()
            text = "📦 কোন অর্ডার নেই" if not orders else "📦 শেষ ২০ টি অর্ডার\n"+"\n".join([f"ID: {x[0]} | User: {x[1]}\nProduct: {x[2]}\nPrice: {x[3]} BDT | {x[4]}\n" for x in orders])
            bot.send_message(chat_id, text)
        elif call.data == "admin_pending":
            if user_id!= ADMIN_ID: return
            c.execute("SELECT id, user_id, product, price FROM orders WHERE status='Pending' ORDER BY id DESC")
            orders = c.fetchall()
            if not orders:
                bot.send_message(chat_id, "✅ কোন পেন্ডিং অর্ডার নেই")
                return
            for o in orders:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("✅ Approve", callback_data=f"approve_{o[0]}"))
                bot.send_message(chat_id, f"🛒 Order ID: {o[0]}\nUser: {o[1]}\nProduct: {o[2]}\nPrice: {o[3]} BDT", reply_markup=markup)

        elif call.data.startswith("approve_"):
            if user_id!= ADMIN_ID: return
            order_id = int(call.data.split("_")[1])
            bot.send_message(chat_id, f"📦 Order {order_id} এর জন্য প্রোডাক্ট কোড দিন")
            user_state[user_id] = {"step": "admin_code", "order_id": order_id}

        elif call.data == "support":
            support_text = "🆘 সাপোর্ট সেন্টার\n💬 সাপোর্ট: @PolasChandra\nWhatsApp: 01873565112\n⏰ ২৪/৭ এভেইলেবল"
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
            bot.edit_message_text(support_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "about":
            about_text = "ℹ️ Proxy Store সম্পর্কে\n🚀 প্রিমিয়াম ডিজিটাল সার্ভিস এর বিশ্বস্ত প্রতিষ্ঠান"
            markup = main_menu()
            markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
            bot.edit_message_text(about_text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
        elif call.data == "home":
            try:
                markup = main_menu()
                markup.add(InlineKeyboardButton("🚀 রেফার & আর্ন", callback_data="refer"))
                bot.edit_message_text(f"🤖 {BOT_NAME}\nProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=markup)
            except: pass

        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in user_state)
    def process_all(message):
        user_id = message.from_user.id
        state = user_state[user_id]
        if state["step"] == "admin_user_id":
            state["target_id"] = int(message.text)
            state["step"] = "admin_amount"
            bot.send_message(message.chat.id, "💰 কত BDT অ্যাড করবেন?")
        elif state["step"] == "admin_amount":
            amount = float(message.text)
            target_id = state["target_id"]
            update_balance(target_id, amount)
            bot.send_message(message.chat.id, f"✅ {target_id} কে {amount} BDT অ্যাড করা হয়েছে\nনতুন ব্যালেন্স: {get_balance(target_id)} BDT")
            bot.send_message(target_id, f"🎉 এডমিন আপনার একাউন্টে {amount} BDT অ্যাড করেছে")
            del user_state[user_id]
        elif state["step"] == "admin_code":
            order_id = state["order_id"]
            code = message.text
            order = get_order_by_id(order_id)
            update_order_status(order_id, "Approved")
            bot.send_message(order[1], f"✅ আপনার অর্ডার এপ্রুভ হয়েছে!\n\nপ্রোডাক্ট: {order[2]}\nকোড: `{code}`\nধন্যবাদ!", parse_mode="Markdown")
            bot.send_message(message.chat.id, f"✅ Order {order_id} Approved and code sent to user")
            del user_state[user_id]
        elif state["step"] == "amount":
            state["amount"] = float(message.text) # float kore nilam
            state["step"] = "trx"
            bot.send_message(message.chat.id, "🧾 Transaction ID দিন")
        elif state["step"] == "trx":
            amount = state["amount"]
            bot.send_message(ADMIN_ID,f"💰 নতুন ডিপোজিট রিকোয়েস্ট\n👤 {message.from_user.first_name}\n🆔 {user_id}\nAmount: {amount} BDT\nTRX ID: {message.text}")

            # EKHANEI MAIN KAJ: 10 tk ba tar beshi hole bonus active
            if amount >= MIN_DEPOSIT_FOR_BONUS:
                referrer = activate_referral_bonus(user_id)
                if referrer:
                    bot.send_message(referrer, f"🎉 অভিনন্দন!\nআপনার রেফার করা ইউজার {amount} টাকা ডিপোজিট করেছে!\nআপনি {REFERRAL_BONUS} BDT বোনাস পেয়েছেন\nনতুন ব্যালেন্স: {get_balance(referrer)} BDT")

            bot.send_message(message.chat.id,"✅ ডিপোজিট রিকোয়েস্ট পাঠানো হয়েছে। ৫-১০ মিনিটের মধ্যে এপ্রুভ হবে।")
            del user_state[user_id]
