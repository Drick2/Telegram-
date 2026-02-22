import telebot
from telebot import types
import os
import re
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Storage
rules_db = {}
warnings_db = {}

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def parse_mute_time(time_str):
    match = re.match(r'(\d+)([mhd])', time_str.lower().strip())
    if not match:
        return int((datetime.utcnow() + timedelta(hours=1)).timestamp())
    value, unit = int(match.group(1)), match.group(2)
    if unit == 'm': delta = timedelta(minutes=value)
    elif unit == 'h': delta = timedelta(hours=value)
    else: delta = timedelta(days=value)
    return int((datetime.utcnow() + delta).timestamp())

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id: continue
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ I've Read Rules", callback_data=f"accept_{member.id}"))
        text = f"""
<b>🎉 Welcome @{member.username or member.first_name}!</b>

Glad you're here 🇺🇬  
Click the button to confirm you read the rules.
Stay chill or get warned 😂
        """
        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    if call.data.startswith("accept_"):
        bot.answer_callback_query(call.id, "✅ Verified! Welcome to the squad 🔥")
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass

@bot.message_handler(commands=['help', 'start'])
def send_help(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📜 Rules", callback_data="show_rules"),
               types.InlineKeyboardButton("👤 My ID", callback_data="my_id"))
    text = """
<b>🤖 Kampala Group Manager Bot</b>

<b>👮 Admin Commands (reply to user):</b>
• /ban — Permanent ban  
• /kick — Kick out  
• /mute 30m or 2h or 1d — Timed mute  
• /unmute — Unmute  
• /warn — Give warning (3 = auto-ban)  
• /unwarn — Remove one warning  
• /pin — Pin message  
• /unpin — Unpin  
• /setrules — Reply to rules text to set custom rules

<b>Everyone:</b>
• /rules — Show rules  
• /id — Show your ID + chat info
    """
    bot.reply_to(message, text, reply_markup=markup)

@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules = rules_db.get(message.chat.id, "1. Be respectful\n2. No spam / links without permission\n3. No NSFW\n4. Follow admins\n5. Have fun 🇺🇬")
    bot.reply_to(message, f"<b>📜 Group Rules</b>\n\n{rules}", parse_mode='HTML')

@bot.message_handler(commands=['setrules'])
def set_rules(message):
    if not is_admin(message.chat.id, message.from_user.id): return bot.reply_to(message, "❌ Admins only!")
    if not message.reply_to_message: return bot.reply_to(message, "Reply to a message that contains the full rules!")
    rules_db[message.chat.id] = message.reply_to_message.text
    bot.reply_to(message, "✅ Rules updated successfully!")

@bot.message_handler(commands=['id'])
def show_id(message):
    user = message.from_user
    text = f"""
<b>👤 User Info</b>
Name: {user.first_name}
Username: @{user.username or 'None'}
ID: <code>{user.id}</code>

<b>💬 Chat Info</b>
Chat ID: <code>{message.chat.id}</code>
Type: {message.chat.type}
    """
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    try:
        bot.kick_chat_member(message.chat.id, user.id)
        bot.reply_to(message, f"🚫 <b>Banned</b> {user.first_name}", parse_mode='HTML')
    except:
        bot.reply_to(message, "Couldn't ban")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    bot.kick_chat_member(message.chat.id, user.id)
    bot.unban_chat_member(message.chat.id, user.id)
    bot.reply_to(message, f"👢 Kicked {user.first_name}")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    time_part = message.text.split()[-1] if len(message.text.split()) > 1 else "1h"
    until = parse_mute_time(time_part)
    bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=False, until_date=until)
    bot.reply_to(message, f"🔇 <b>Muted</b> {user.first_name} for {time_part}")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=True)
    bot.reply_to(message, f"🔊 Unmuted {user.first_name}")

@bot.message_handler(commands=['warn'])
def warn_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    chat = message.chat.id
    if chat not in warnings_db: warnings_db[chat] = {}
    warnings_db[chat][user.id] = warnings_db[chat].get(user.id, 0) + 1
    count = warnings_db[chat][user.id]
    text = f"⚠️ <b>Warning {count}/3</b> for {user.first_name}"
    if count >= 3:
        bot.kick_chat_member(chat, user.id)
        text += "\n\n🚫 3 warnings → Banned!"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=['unwarn'])
def unwarn_user(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    user = message.reply_to_message.from_user
    chat = message.chat.id
    if chat in warnings_db and user.id in warnings_db[chat]:
        warnings_db[chat][user.id] -= 1
        bot.reply_to(message, f"✅ Warning removed for {user.first_name}")

@bot.message_handler(commands=['pin'])
def pin_message(message):
    if not is_admin(message.chat.id, message.from_user.id) or not message.reply_to_message: return
    bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    bot.reply_to(message, "📌 Message pinned!")

@bot.message_handler(commands=['unpin'])
def unpin_message(message):
    if not is_admin(message.chat.id, message.from_user.id): return
    bot.unpin_chat_message(message.chat.id)
    bot.reply_to(message, "📌 Unpinned")

print("🚀 Fancy Kampala Group Bot is LIVE & looking clean!")
bot.polling(none_stop=True)
