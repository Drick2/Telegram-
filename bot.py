import telebot
from handlers.start import start_handler
from handlers.airdrop import airdrop_handler, callback_handler

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# Register handlers
bot.message_handler(commands= )(start_handler)
bot.message_handler(commands=['airdrop', 'tasks'])(airdrop_handler)
bot.callback_query_handler(func=lambda call: True)(callback_handler)

print("🚀 $MATO Airdrop Bot is LIVE!")
bot.polling(none_stop=True)
