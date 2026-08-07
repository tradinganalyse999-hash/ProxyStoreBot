from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu, quantity_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, add_referral, activate_referral_bonus, get_refer_stats, add_deposit_request, approve_deposit, c, conn
from bot import bot

REFERRAL_BONUS = 0.50
MIN_DEPOSIT_FOR_BONUS = 10

def register_handlers():

    @bot.message_handler(commands=["start"])
    def start(message):
        user_id = message.from_user.id
        args = message.text.split()
        referred_by = None
        if len(args) > 1 and args[1].startswith("ref"):
            try: referred_by = int(args[1].replace("ref", ""))
            except: pass
        create_user(user_id, referred_by)
        if referred_by and referred_by!= user_id: add_referral(referred_by, user_id)
        markup = main_menu()
        text = f"🤖 {BOT_NAME}\nProxyStore AI তে স্বাগতম ❤️\n📌 রেফার বোনাস: {REFERRAL_BONUS} BDT\nশর্ত: আপনার রেফার করা ইউজার ১০ টাকা ডিপোজিট করলে বোনাস পাবেন"
        bot.send_message(message.chat.id, text, reply_markup=markup)

    @bot.message_handler(commands=["admin"])
    def admin(message):
        if message.from_user.id!= ADMIN_ID:
            bot.reply_to(message, "❌ Access Denied")
            return
        bot.send_message(message.chat.id, "👑 Admin Panel", reply_markup=admin_buttons())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        msg_id = call.message_id # EI LINE TA 100% THIK
        chat_id = call.message.chat.id
        user_id = call.from_user.id

        if call.data == "shop":
            bot.edit_message_text("🛒 ক্যাটাগরি সিলেক্ট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=shop_menu())

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

        # QUANTITY SYSTEM
        elif call.data.startswith("qty_"):
            _, category, name, price = call.data.split("_", 3)
            qty = 1; price = float(price)
            total = price * qty
            text = f"🛒 *{name}*\n\n💎 প্রাইস: {price} BDT\nস্টক: 99+\n\nপরিমাণ: {qty}\nমোট: 💎 {total} BDT"
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, qty), parse_mode="Markdown")

        elif call.data.startswith("inc_"):
            _, category, name, price, qty = call.data.split("_")
            qty = int(qty) + 1; price = float(price)
            total = price * qty
            text = f"🛒 *{name}*\n\n💎 প্রাইস: {price} BDT\nস্টক: 99+\n\nপরিমাণ: {qty}\nমোট: 💎 {total} BDT"
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, qty), parse_mode="Markdown")

        elif call.data.startswith("dec_"):
            _, category, name, price, qty = call.data.split("_")
            qty = int(qty); price = float(price)
            if qty > 1: qty = qty - 1
            total = price * qty
            text = f"🛒 *{name}*\n\n💎 প্রাইস: {price} BDT\nস্টক: 99+\n\nপরিমাণ: {qty}\nমোট: 💎 {total} BDT"
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, qty), parse_mode="Markdown")

        elif call.data.startswith("confirm_"):
            _, category, name, price, qty = call.data.split("_")
            price = float(price); qty = int(qty); total_price = price * qty
            balance = get_balance(user_id)
            if balance >= total_price:
                order_id = add_order(user_id, f"{category.upper()}: {name} x{qty}", total_price)
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton("✅ Confirm", callback_data=f"admin_confirm_{order_id}"),
                    InlineKeyboardButton("❌ Cancel", callback_data=f"admin_cancel_{order_id}")
                )
                bot.send_message(ADMIN_ID, f"🛒 নতুন অর্ডার\n👤 User: {user_id}\n📦 Product: {name} x{qty}\n💰 Total: {total_price} BDT\nApprove করবেন?", reply_markup=markup)
                bot.edit_message_text(f"⏳ আপনার অর্ডারটি এডমিন এর কাছে পাঠানো হয়েছে। এপ্রুভ হলেই প্রোডাক্ট পাবেন।", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
            else:
                bot.edit_message_text(f"❌ ব্যালেন্স নেই\nআপনার ব্যালেন্স: {balance} BDT\nপ্রয়োজন: {total_price} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

        # ADMIN ORDER CONFIRM/CANCEL
        elif call.data.startswith("admin_confirm_"):
            if user_id!= ADMIN_ID: return
            order_id = int(call.data.split("_")[2])
            order = get_order_by_id(order_id)
            if order:
                update_balance(order[1], -order[3])
                update_order_status(order_id, "Approved")
                bot.send_message(order[1], f"✅ আপনার অর্ডার এপ্রুভ হয়েছে!\n\nপ্রোডাক্ট: {order[2]}\nমোট: {order[3]} BDT\nধন্যবাদ!")
                bot.edit_message_text(f"✅ Order Approved\nID: {order_id}\nUser: {order[1]}", chat_id=chat_id, message_id=msg_id)

        elif call.data.startswith("admin_cancel_"):
            if user_id!= ADMIN_ID: return
            order_id = int(call.data.split("_")[2])
            order = get_order_by_id(order_id)
            if order:
                update_order_status(order_id, "Cancelled")
                bot.send_message(order[1], f"❌ আপনার অর্ডারটি বাতিল করা হয়েছে।\nপ্রোডাক্ট: {order[2]}")
                bot.edit_message_text(f"❌ Order Cancelled\nID: {order_id}\nUser: {order[1]}", chat_id=chat_id, message_id=msg_id)

        elif call.data.startswith("custom_"):
            _, category, name, price = call.data.split("_")
            user_state[user_id] = {"step": "custom_qty", "category": category, "name": name, "price": float(price)}
            bot.send_message(chat_id, "পরিমাণ কত পিস নিবেন? শুধু নাম্বার লিখুন")

        elif call.data == "refer":
            ref_count, ref_earn = get_refer_stats(user_id)
            bot_username = bot.get_me().username
            refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"
            text = f"📌 *রেফার & আর্ন*\n💰 প্রতি সফল রেফারে পাবেন *{REFERRAL_BONUS} BDT*\n\n📊 *আপনার স্ট্যাটস:*\n👥 মোট রেফার: *{ref_count}*\n💵 মোট আয়: *{ref_earn} BDT*\n\n🔗 *আপনার লিংক:*\n`{refer_link}`"
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu(), parse_mode="Markdown")

        elif call.data == "deposit":
            bot.edit_message_text("💰 ডিপোজিট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

        elif call.data in ["bkash", "nagad", "rocket", "usdt"]:
            methods = {"bkash": "bKash: `01603940061`", "nagad": "Nagad: `01603940061`", "rocket": "Rocket: `01603940061`", "usdt": "USDT TRC20:\n`TGE8oPaj7cYP14xuoHTZT19KxwSf12FYoz`"}
            bot.edit_message_text(f"💳 {methods[call.data]}\n\n1. টাকা পাঠান\n2. এরপর 'পেমেন্ট সাবমিট' করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu(), parse_mode="Markdown")

        elif call.data == "submit_payment":
            user_state[user_id] = {"step": "amount"}
            bot.send_message(chat_id, "💰 ডিপোজিট এর পরিমাণ লিখুন")

        elif call.data == "wallet":
            bot.edit_message_text(f"👛 ওয়ালেট\n💰 ব্যালেন্স: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

        elif call.data == "orders":
            orders = get_orders(user_id)
            text = "📦 আমার অর্ডার\nকোন অর্ডার নেই" if not orders else "📦 আমার অর্ডার\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

        # DEPOSIT APPROVE/REJECT
        elif call.data.startswith("approve_dep_"):
            if user_id!= ADMIN_ID: return
            deposit_id = int(call.data.split("_")[2])
            u_id, amount = approve_deposit(deposit_id)
            if u_id:
                bot.send_message(u_id, f"🎉 আপনার {amount} BDT ডিপোজিট সফল হয়েছে!\nনতুন ব্যালেন্স: {get_balance(u_id)} BDT")
                bot.edit_message_text(f"✅ Deposit Approved\nUser: {u_id}\nAmount: {amount} BDT", chat_id=chat_id, message_id=msg_id)

        elif call.data.startswith("reject_dep_"):
            if user_id!= ADMIN_ID: return
            deposit_id = int(call.data.split("_")[2])
            c.execute("SELECT user_id, amount FROM deposits WHERE id=? AND status='pending'", (deposit_id,))
            res = c.fetchone()
            if res:
                u_id, amount = res
                c.execute("UPDATE deposits SET status='rejected' WHERE id=?", (deposit_id,))
                conn.commit()
                warning_msg = f"⚠️ *সতর্কবার্তা* ⚠️\n\n🤖 বটের সাথে কখনো প্রতারণা করো না।\n⛔ পরের বার করলে ব্ল্যাক খাবে। 🚫\n\nআপনার {amount} BDT ডিপোজিট রিকোয়েস্ট বাতিল করা হয়েছে।"
                bot.send_message(u_id, warning_msg, parse_mode="Markdown")
                bot.edit_message_text(f"❌ Deposit Rejected\nUser: {u_id}\nAmount: {amount} BDT", chat_id=chat_id, message_id=msg_id)

        elif call.data == "support":
            bot.edit_message_text("🆘 সাপোর্ট: @PolasChandra\nWhatsApp: 01873565112", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "about":
            bot.edit_message_text("ℹ️ Proxy Store সম্পর্কে\n🚀 প্রিমিয়াম ডিজিটাল সার্ভিস", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "home":
            bot.edit_message_text(f"🤖 {BOT_NAME}\nProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in user_state)
    def process_all(message):
        user_id = message.from_user.id
        state = user_state[user_id]
        if state["step"] == "custom_qty":
            try: qty = int(message.text)
            except: bot.send_message(message.chat.id, "❌ সঠিক সংখ্যা দিন"); return
            category = state["category"]; name = state["name"]; price = state["price"]
            total = price * qty
            text = f"🛒 *{name}*\n\n💎 প্রাইস: {price} BDT\nস্টক: 99+\n\nপরিমাণ: {qty}\nমোট: 💎 {total} BDT"
            bot.send_message(message.chat.id, text, reply_markup=quantity_menu(category, name, price, qty), parse_mode="Markdown")
            del user_state[user_id]
        elif state["step"] == "amount":
            try: state["amount"] = float(message.text)
            except: bot.send_message(message.chat.id, "❌ ভুল Amount"); return
            state["step"] = "trx"; bot.send_message(message.chat.id, "🧾 Transaction ID দিন")
        elif state["step"] == "trx":
            amount = state["amount"]; trx_id = message.text
            deposit_id = add_deposit_request(user_id, amount, trx_id)
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(InlineKeyboardButton(f"✅ {amount} BDT Approve", callback_data=f"approve_dep_{deposit_id}"), InlineKeyboardButton(f"❌ Reject", callback_data=f"reject_dep_{deposit_id}"))
            bot.send_message(ADMIN_ID,f"💰 নতুন ডিপোজিট রিকোয়েস্ট\n🆔 {user_id}\nAmount: {amount} BDT\nTRX ID: `{trx_id}`", reply_markup=markup, parse_mode="Markdown")
            if amount >= MIN_DEPOSIT_FOR_BONUS:
                referrer = activate_referral_bonus(user_id)
                if referrer: bot.send_message(referrer, f"🎉 রেফার বোনাস {REFERRAL_BONUS} BDT পেয়েছেন")
            bot.send_message(message.chat.id,"✅ ডিপোজিট রিকোয়েস্ট পাঠানো হয়েছে।"); del user_state[user_id]
