import telebot
import re

TOKEN = "8648862851:AAHzyHo8cFCH3QTWdNgDPSs9rsef6tAlNGk"
CHANNEL = "@kansal_advanced_strategy"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.upper()

    strike = re.search(r'(\d+\s?(PE|CE))', text)
    above = re.search(r'ABOVE\s+(\d+)', text)
    target = re.search(r'TARGET\s+([\d/]+)', text)
    sl = re.search(r'SL\s+(\d+)', text)

    strike_text = strike.group(1) if strike else ""
    above_text = above.group(1) if above else ""
    target_text = target.group(1) if target else ""
    sl_text = sl.group(1) if sl else ""

    final = f"📌 {strike_text} | above {above_text} | {target_text} possible | below {sl_text} weak"

    bot.send_message(CHANNEL, final)

bot.infinity_polling()
