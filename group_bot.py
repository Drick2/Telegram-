import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Replace these with your real links
GROUP_LINK = "t.me/yourgroup"  # ← your group invite link
CHANNEL_LINK = "t.me/MATOAirdrop"  # ← your channel invite link
PUMP_FUN_LINK = "https://pump.fun/YOUR_TOKEN_CA_HERE"  # ← after you create token

# Fake storage (real one would use DB, this is simple for now)
referrals =  # user_id: count
points =     # user_id: total $MATO

def is_member(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍌 Join Airdrop", callback_data="check_join"),
        types.InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)
    )
    markup.add(
        types.InlineKeyboardButton("🛒 Buy $MATO", url=PUMP_FUN_LINK),
        types.InlineKeyboardButton("💰 My Balance", callback_data="balance")
    )
    markup.add(
        types.InlineKeyboardButton("🔗 Referral Link", callback_data="referral")
    )
    
    text = """
<b>🍌 $MATO — Matooke Coin of Kampala</b>

The tastiest meme coin on Solana! 🇺🇬  
Peel to the moon with us.  

Click "Join Airdrop" to start earning free $MATO!
    """
    bot.reply_to(message, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id
    group_id = "-100YOURGROUPID"  # ← replace with real group ID (get from /id command later)
    
    if not is_member(group_id, user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Join Group", url=GROUP_LINK))
        bot.answer_callback_query(call.id, "Join the group first!", show_alert=True)
        bot.send_message(call.message.chat.id, "You gotta join the squad first bro! 👇", reply_markup=markup)
        return
    
    if not is_member(CHANNEL_LINK.replace("t.me/", ""), user_id):
        bot.answer_callback_query(call.id, "Join the channel first!", show_alert=True)
        bot.send_message(call.message.chat.id, "One more step — join the channel! 👇", reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)
        ))
        return
    
    # They’re in both — give referral link
    if user_id not in referrals:
        referrals = 0
        points = 0
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Your Referral Link", url=f"https://t.me/{bot.get_me().username}?start={user_id}"))
    
    bot.answer_callback_query(call.id, "You’re in! 🎉")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"<b>✅ You’re verified!</b>\n\nYour referral link: https://t.me/{bot.get_me().username}?start={user_id}\n\nEach friend = +2 $MATO! Invite now 🍌",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "balance")
def balance(call):
    user_id = call.from_user.id
    my_points = points.get(user_id, 0)
    my_refs = referrals.get(user_id, 0)
    text = f"""
<b>💰 Your $MATO Balance</b>

You have: <b>{my_points} $MATO</b>  
Referrals: <b>{my_refs}</b> (2 per friend)  
Total earned: <b>{my_refs * 2} $MATO</b>

Keep inviting & posting memes for more!
    """
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == "referral")
def referral(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"🔗 Share this: https://t.me/{bot.get_me().username}?start={user_id}\n\nEach join = 2 free $MATO!")

@bot.message_handler(commands=['help', 'menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍌 Join Airdrop", callback_data="check_join"),
        types.InlineKeyboardButton("💰 My Balance", callback_data="balance"),
        types.InlineKeyboardButton("🔗 Referral Link", callback_data="referral"),
        types.InlineKeyboardButton("🛒 Buy $MATO", url=PUMP_FUN_LINK)
    )
    bot.reply_to(message, "Main Menu 🍌", reply_markup=markup)

# Handle referral links (when someone clicks their link)
@bot.message_handler(commands=['start'])
def handle_referral(message):
    if len(message.text.split()) > 1:
        ref_id = int(message.text.split()[1])
        user_id = message.from_user.id
        if ref_id != user_id and ref_id in referrals:
            referrals += 1
            points += 2
            bot.send_message(ref_id, f"🎉 New friend joined! +2 $MATO added! Total: {points }")
            bot.reply_to(message, "Thanks for joining! You’re now in the $MATO squad 🍌")
        else:
            start(message)

print("🚀 $MATO Airdrop Bot is LIVE!")
bot.polling(none_stop=True)
