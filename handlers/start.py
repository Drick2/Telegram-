from telebot import types
from config import GROUP_LINK, CHANNEL_LINK, PUMP_FUN_LINK

def start_handler(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛒 Buy $MATO", url=PUMP_FUN_LINK),
        types.InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK),
        types.InlineKeyboardButton("👥 Group", url=GROUP_LINK),
        types.InlineKeyboardButton("💰 Airdrop", callback_data="airdrop")
    )
    text = """
<b>🍌 Welcome to $MATO — Matooke Coin!</b>

Peel to the moon with us! 🇺🇬  
Type /airdrop for free tokens.

Get started now 👇
    """
    message.reply_to(message, text, reply_markup=markup)
