from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import user_state
from config import ADMIN_ID, SUPPORT_USERNAME, BOT_NAME
from buttons import main_menu, shop_menu, deposit_menu, product_menu, quantity_menu
from admin import admin_buttons
from database import create_user, get_balance, update_balance, add_order, get_orders, get_order_by_id, update_order_status, c, get_all_users, get_stock_count, take_codes, add_stock
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
        elif call.data == "morelogin_list":
            bot.edit_message_text("🖥️ Morelogin 100 Minutes", chat_id=chat_id, message_id=msg_id, reply_markup=product_menu("morelogin"))

        elif call.data == "noop":
            bot.answer_callback_query(call.id, "Quantity change korte + - use koro")

        elif call.data.startswith("select_qty|"):
            parts = call.data.split("|")
            category, name, price = parts[1], parts[2], float(parts[3])
            bot.edit_message_text(f"🛒 {name}\n💎 Price: {price} BDT\nStock: unlimited\nQuantity: 1", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, 1))
        elif call.data.startswith("qty_plus|"):
            parts = call.data.split("|")
            category, name, price, qty = parts[1], parts[2], float(parts[3]), int(parts[4])
            qty += 1
            bot.edit_message_text(f"🛒 {name}\n💎 Price: {price} BDT\nStock: unlimited\nQuantity: {qty}", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, qty))
        elif call.data.startswith("qty_minus|"):
            parts = call.data.split("|")
            category, name, price, qty = parts[1], parts[2], float(parts[3]), int(parts[4])
            if qty > 1: qty -= 1
            bot.edit_message_text(f"🛒 {name}\n💎 Price: {price} BDT\nStock: unlimited\nQuantity: {qty}", chat_id=chat_id, message_id=msg_id, reply_markup=quantity_menu(category, name, price, qty))
        elif call.data.startswith("custom_qty|"):
            parts = call.data.split("|")
            category, name, price = parts[1], parts[2], float(parts[3])
            user_state[user_id] = {"step": "custom_qty", "category": category, "name": name, "price": price}
            bot.send_message(chat_id, "📝 Koyta niba? Number likhe pathao")
        elif call.data.startswith("buy|"):
            parts = call.data.split("|")
            category, name, price, qty = parts[1], parts[2], float(parts[3]), int(parts[4])
            total_price = price * qty
            balance = get_balance(user_id)
            if balance >= total_price:
                if category in ["proxy", "morelogin"]:
                    available = get_stock_count(category, name)
                    if available < qty:
                        bot.send_message(ADMIN_ID, f"⚠️ Stock sesh! {name} - {qty} pcs order asche but stock {available} pcs")
                        bot.edit_message_text(f"❌ Stock e nai. Admin ke janao. Stock: {available} pcs", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
                        return
                update_balance(user_id, -total_price)
                if category in ["proxy", "morelogin"]:
                    codes = take_codes(category, name, qty)
                    code_list = "\n".join([f"`{co}`" for co in codes])
                    add_order(user_id, f"{name} x{qty}", total_price)
                    delivery_msg = f"✅ Order Delivered!\n\nProduct: {name}\nQuantity: {qty} pcs\nTotal: {total_price} BDT\n\n🔑 Your Codes:\n{code_list}\n\nProblem hole {SUPPORT_USERNAME}"
                    bot.send_message(user_id, delivery_msg, parse_mode="Markdown")
                    bot.edit_message_text(f"✅ Order Complete! Code upore diye disi", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
                else:
                    add_order(user_id, f"{name} x{qty}", total_price)
                    bot.edit_message_text(f"✅ Order Confirmed!\n\nProduct: {name}\nQuantity: {qty} pcs\nTotal: {total_price} BDT\n\nAdmin 5-10 min er moddhe code diye dibe", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
                    bot.send_message(ADMIN_ID, f"🛒 New Manual Order\nUser: {user_id}\nProduct: {name} x{qty}\nTotal: {total_price} BDT")
            else:
                bot.edit_message_text(f"❌ Not Enough Balance\nYour Balance: {balance} BDT\nRequired: {total_price} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=deposit_menu())

        elif call.data == "admin_add_stock":
            if user_id!= ADMIN_ID: return
            bot.send_message(chat_id, "📦.txt file pathao\nFormat: prottek line e 1 ta code")
            user_state[user_id] = {"step": "wait_txt_file"}
        elif call.data == "admin_broadcast":
            if user_id!= ADMIN_ID: return
            bot.send_message(chat_id, "📢 Broadcast message likhe pathao. Sob user pabe.")
            user_state[user_id] = {"step": "broadcast_msg"}
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
        elif call.data.startswith("confirm_"):
            if user_id!= ADMIN_ID: return
            parts = call.data.split("_")
            target_user = int(parts[1])
            amount = float(parts[2])
            update_balance(target_user, amount)
            new_balance = get_balance(target_user)
            success_msg = f"✅ ডিপোজিট সফল!\n\n💰 যোগ হয়েছে: +{amount:.2f} টাকা\n💳 ব্যালেন্স: {new_balance:.2f} টাকা"
            bot.send_message(target_user, success_msg)
            bot.edit_message_text(f"✅ Confirmed. {amount} BDT added to {target_user}", chat_id=chat_id, message_id=msg_id)
        elif call.data.startswith("cancel_"):
            if user_id!= ADMIN_ID: return
            target_user = int(call.data.split("_")[1])
            bot.send_message(target_user, "⚠ Payment Verification Failed")
            bot.edit_message_text("❌ Cancelled by Admin", chat_id=chat_id, message_id=msg_id)
        elif call.data == "wallet":
            bot.edit_message_text(f"👛 Wallet\n💰 Balance: {get_balance(user_id)} BDT", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "orders":
            orders = get_orders(user_id)
            text = "📦 My Orders\nNo orders yet" if not orders else "📦 My Orders\n"+"\n".join([f"• {x[0]} - {x[1]} BDT - {x[2]}" for x in orders])
            bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "support":
            support_text = f"🆘 Support Center\nSupport: {SUPPORT_USERNAME}"
            bot.edit_message_text(support_text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "about":
            about_text = f"ℹ About {BOT_NAME}"
            bot.edit_message_text(about_text, chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
        elif call.data == "home":
            try:
                bot.edit_message_text(f"🤖 {BOT_NAME}\nWelcome to ProxyStore AI", chat_id=chat_id, message_id=msg_id, reply_markup=main_menu())
            except: pass
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda m: m.from_user.id in user_state, content_types=['text', 'document'])
    def process_all(message):
        user_id = message.from_user.id
        state = user_state.get(user_id)
        if not state: return

        if state["step"] == "wait_txt_file":
            if message.content_type == 'document' and message.document:
                try:
                    file_name = message.document.file_name
                    if not file_name.lower().endswith(".txt"):
                        bot.send_message(message.chat.id, "❌ Sudhu.txt file pathao")
                        return
                    file_info = bot.get_file(message.document.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    codes = downloaded_file.decode("utf-8", errors="ignore").splitlines()
                    codes = [c.strip() for c in codes if c.strip()!= ""]
                    if not codes:
                        bot.send_message(message.chat.id, "❌ File ta faka!")
                        return
                    state["codes"] = codes
                    state["step"] = "stock_category"
                    bot.send_message(message.chat.id, f"✅ {len(codes)} ta code peyechi\n\nEkhon Category bolo:\n`proxy` / `morelogin`", parse_mode="Markdown")
                except Exception as e:
                    bot.send_message(message.chat.id, f"❌ Error: {e}")
            else:
                bot.send_message(message.chat.id, "❌ Age.txt file ta upload koro, text na. Pin icon e click kore Document hisebe pathao.")

        elif state["step"] == "stock_category":
            cat = message.text.lower().strip()
            if cat not in ["proxy", "morelogin"]:
                bot.send_message(message.chat.id, "❌ Vul category. `proxy` ba `morelogin` likho", parse_mode="Markdown")
                return
            state["category"] = cat
            state["step"] = "stock_product"
            if cat == "proxy":
                bot.send_message(message.chat.id, "Product er name ki? Likhba:\n`Owl Proxy 200MB`", parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "Product er name ki? Likhba:\n`Morelogin 100 Minutes`", parse_mode="Markdown")

        elif state["step"] == "stock_product":
            add_stock(state["category"], message.text.strip(), state["codes"])
            bot.send_message(message.chat.id, f"✅ Stock Add Complete!\n\nCategory: {state['category']}\nProduct: {message.text.strip()}\nTotal: {len(state['codes'])} pcs")
            del user_state[user_id]

        elif state["step"] == "admin_user_id":
            state["target_id"] = int(message.text)
            state["step"] = "admin_amount"
            bot.send_message(message.chat.id, "💰 Koto BDT add korba?")
        elif state["step"] == "admin_amount":
            amount = float(message.text)
            target_id = state["target_id"]
            update_balance(target_id, amount)
            bot.send_message(message.chat.id, f"✅ {target_id} ke {amount} BDT add kora hoise")
            bot.send_message(target_id, f"🎉 Admin apnar account e {amount} BDT add korse")
            del user_state[user_id]
        elif state["step"] == "broadcast_msg":
            message_text = message.text
            all_users = get_all_users()
            sent = 0
            for uid in all_users:
                try:
                    bot.send_message(uid, f"📢 **Notice from {BOT_NAME}**\n\n{message_text}", parse_mode="Markdown")
                    sent += 1
                except: pass
            bot.send_message(message.chat.id, f"✅ Broadcast Done! {sent} jon ke pathano hoise")
            del user_state[user_id]
        elif state["step"] == "admin_code":
            order_id = state["order_id"]
            code = message.text
            order = get_order_by_id(order_id)
            update_order_status(order_id, "Approved")
            bot.send_message(order[1], f"✅ Your Order Approved!\n\nProduct: {order[2]}\nCode: `{code}`", parse_mode="Markdown")
            bot.send_message(message.chat.id, f"✅ Order {order_id} Approved")
            del user_state[user_id]
        elif state["step"] == "amount":
            state["amount"] = message.text
            state["step"] = "trx"
            bot.send_message(message.chat.id, "🧾 Send Transaction ID / TrxID")
        elif state["step"] == "trx":
            amount = state['amount']
            trx = message.text
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{user_id}_{amount}"),
                InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{user_id}")
            )
            bot.send_message(ADMIN_ID,f"💰 New Deposit Request\n👤 {message.from_user.first_name}\n🆔 {user_id}\nAmount: {amount} BDT\nTRX ID: {trx}", reply_markup=markup)
            bot.send_message(message.chat.id,"✅ Deposit Request Sent. Admin will approve in 5-10 min.")
            del user_state[user_id]
        elif state["step"] == "custom_qty":
            try:
                qty = int(message.text)
                if qty < 1: qty = 1
                category = state["category"]
                name = state["name"]
                price = state["price"]
                bot.send_message(message.chat.id, f"🛒 {name}\n💎 Price: {price} BDT\nQuantity: {qty}", reply_markup=quantity_menu(category, name, price, qty))
                del user_state[user_id]
            except:
                bot.send_message(message.chat.id, "❌ Sothik number dao")
