import os
import telebot
from dotenv import load_dotenv
from keto_analyzer import analyze_food_text

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("🥗 Keto_Atkins_Bot is online. Waiting for food...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a food name (like 'Egg') and I'll give you the Net Carbs!")

@bot.message_handler(func=lambda message: True)
def handle_food_query(message):
    query = message.text
    print(f"🔍 Searching: {query}")
    response = analyze_food_text(query)
    bot.reply_to(message, response, parse_mode='Markdown')

if __name__ == "__main__":
    bot.infinity_polling()