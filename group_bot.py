import telebot
import os
import time

TOKEN = os.getenv("TOKEN")  # ← we'll add this safely later
bot = telebot.TeleBot(TOKEN)

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id: continue
        bot.send_message(message.chat.id, f"👋 Welcome @{member.username or member.first_name} to the squad! 🇺🇬\nRead rules → /rules")

@bot.message_handler(commands=['rules'])
def show_rules(message):
    rules = "📜 Group Rules:\n1. No spam/links\n2. Be respectful\n3. No NSFW\n4. Listen to admins\nBreak rules = warn → mute → ban"
    bot.reply_to(message, rules)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Only admins!")
    if not message.reply_to_message:
        return bot.reply_to(message, "Reply to the bad message then type /ban")
    user = message.reply_to_message.from_user
    try:
        bot.kick_chat_member(message.chat.id, user.id)
        bot.reply_to(message, f"🚫 Banned {user.first_name} (@{user.username or 'no username'})")
    except:
        bot.reply_to(message, "Couldn't ban (they might be admin)")

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
    bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=False)
    bot.reply_to(message, f"🔇 Muted {user.first_name} (1 hour)")

print("🚀 Group bot starting...")
bot.polling(none_stop=True)
