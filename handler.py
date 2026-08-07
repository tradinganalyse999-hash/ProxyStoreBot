    # v3 cache-bust 07-08-2026
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu, quantity_menu
from database import create_user, get_balance, update_balance, add_order, get_orders, add_referral, activate_referral_bonus, get_refer_stats, add_deposit_request, approve_deposit
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
            try:
                referred_by = int(args[1].replace("ref", ""))
            except:
                pass
        create_user(user_id, referred_by)
        if referred_by and referred_by!= user_id:
            add_referral(referred_by, user_id)
        text = f"🤖 {BOT_NAME}\nProxyStore AI তে স্বাগতম ❤️\n📌 রেফার বোনাস: {REFERRAL_BONUS} BDT"
        bot.send_message(message.chat.id, text, reply_markup=main_menu())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        try:
            if not call.message:
                return
            msg_id = call.message.id
            chat_id = call.message.chat.id
            user_id = call.from_user.id

            if call.data == "shop":
                bot.edit_message_text("🛒 ক্যাটাগরি সিলেক্ট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=shop_menu())

            elif call.data.endswith("_list"):
                category = call.data.replace("_list","")
                bot.edit_message_text(f"🛒 {category.upper()} প্রোডাক্ট", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu(category))

            elif call.data.startswith("qty_"):
                _, category, safe_name, price = call.data.split("_", 3)
                name = safe_name.replace("_"," ")
                bot.edit_message_text(f"🛒 *{name}*\n💎 প্রাইস: {price} BDT\nপরিমাণ: 1", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, safe_name, float(price), 1), parse_mode="Markdown")

            elif call.data.startswith("inc_"):
                _, category, safe_name, price, qty = call.data.split("_")
                name = safe_name.replace("_"," ")
                qty = int(qty) + 1
                bot.edit_message_text(f"🛒 *{name}*\n💎 প্রাইস: {price} BDT\nপরিমাণ: {qty}", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, safe_name, float(price), qty), parse_mode="Markdown")

            elif call.data.startswith("dec_"):
                _, category, safe_name, price, qty = call.data.split("_")
                name = safe_name.replace("_"," ")
                qty = int(qty)
                if qty > 1:
                    qty -= 1
                bot.edit_message_text(f"🛒 *{name}*\n💎 প্রাইস: {price} BDT\nপরিমাণ: {qty}", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, safe_name, float(price), qty), parse_mode="Markdown")

            elif call.data.startswith("confirm_"):
                _, category, safe_name, price, qty = call.data.split("_")
                name = safe_name.replace("_", " ")
                total = float(price) * int(qty)
                balance = get_balance(user_id)
                if balance >= total:
                    order_id = add_order(user_id, f"{name} x{qty}", total)
                    bot.send_message(ADMIN_ID, f"🛒 নতুন অর্ডার #{order_id}\nUser: {user_id}\nProduct: {name} x{qty}\nTotal: {total} BDT")
                    bot.edit_message_text("⏳ অর্ডার এডমিন এর কাছে গেছে", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
                else:
                    bot.edit_message_text(f"❌ ব্যালেন্স নেই\nব্যালেন্স: {balance} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

            elif call.data == "wallet":
                bot.edit_message_text(f"👛 ওয়ালেট\n💰 ব্যালেন্স: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

            elif call.data == "orders":
                orders = get_orders(user_id)
                text = "📦 আমার অর্ডার\nকোন অর্ডার নেই" if not orders else "📦 আমার অর্ডার\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
                bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

            elif call.data == "refer":
                ref_count, ref_earn = get_refer_stats(user_id)
                bot_username = bot.get_me().username
                refer_link = f"https://t.me/{bot_username}?start=ref{user_id}"
                text = f"📌 *রেফার & আর্ন*\n💰 প্রতি সফল রেফারে পাবেন *{REFERRAL_BONUS} BDT*\n\n📊 *আপনার স্ট্যাটস:*\n👥 মোট রেফার: *{ref_count}*\n💵 মোট আয়: *{ref_earn} BDT*\n\n🔗 *আপনার লিংক:*\n`{refer_link}`"
                bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu(), parse_mode="Markdown")

            elif call.data == "deposit":
                bot.edit_message_text("💰 ডিপোজিট করুন", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

            elif call.data == "home":
                bot.edit_message_text(f"🤖 {BOT_NAME}", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())

            bot.answer_callback_query(call.id)

        except Exception as e:
            print("CALLBACK ERROR:", e)
            bot.answer_callback_query(call.id, "⚠️ সমস্যা হয়েছে")# v2
            
