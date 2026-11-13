import telebot
from telebot import types

TOKEN = "9131804067:AAE9OQGTCfLAfOZrZyDg2wlIEPbRidF84tU"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "🎁 Create NFT Offer", callback_data="create"))
    kb.add(types.InlineKeyboardButton(
        "📋 My Offers", callback_data="offers"))

    bot.send_message(
        message.chat.id,
        "💎 TON NFT OFFER BOT\n\nWelcome!",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: True)
def callback(call):
    if call.data == "create":
        msg = bot.send_message(
            call.message.chat.id,
            "Введи назву NFT:"
        )
        bot.register_next_step_handler(msg, get_nft)

    elif call.data == "offers":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
                         "Твої тестові офери поки відсутні.")

def get_nft(message):
    nft = message.text
    msg = bot.send_message(
        message.chat.id,
        f"NFT: {nft}\n\nВведи ціну в TON:"
    )
    bot.register_next_step_handler(msg, get_price, nft)

def get_price(message, nft):
    try:
        price = float(message.text)
        if price <= 0:
            raise ValueError

        bot.send_message(
            message.chat.id,
            f"💎 DEMO NFT OFFER\n\n"
            f"NFT: {nft}\n"
            f"Price: {price} TON\n\n"
            f"⚠️ TEST OFFER — NOT REAL"
        )
    except ValueError:
        bot.send_message(message.chat.id,
                         "Введи правильну ціну.")

bot.infinity_polling()
