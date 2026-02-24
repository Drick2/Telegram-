from telebot import types
from config import GROUP_ID, CHANNEL_LINK

def is_member(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in except:
        return False

def airdrop_handler(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Join Airdrop", callback_data="check_join"))
    text = """
<b>💰 $MATO AIRDROP</b>

5% supply (50M $MATO) for community!  
Join group & channel → post memes → invite friends.

Click below to check eligibility 🍌
    """
    message.reply_to(message, text, reply_markup=markup)

def callback_handler(call):
    user_id = call.from_user.id
    if call.data == "check_join":
        if not is_member(GROUP_ID, user_id):
            markup = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Join Group", url=GROUP_LINK)
            )
            bot.answer_callback_query(call.id, "Join group first!", show_alert=True)
            bot.send_message(call.message.chat.id, "Join the squad first 🍌", reply_markup=markup)
            return
        if not is_member(CHANNEL_LINK.replace("t.me/", ""), user_id):
            bot.answer_callback_query(call.id, "Join channel too!", show_alert=True)
            bot.send_message(call.message.chat.id, "One more — join channel!", reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)
            ))
            return
        bot.answer_callback_query(call.id, "You’re in! 🎉")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ You’re verified! Now post matooke memes & invite friends for points! 🍌"
        )
    elif call.data == "airdrop":
        airdrop_handler(call.message)
