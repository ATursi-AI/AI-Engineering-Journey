import os
import telebot
from dotenv import load_dotenv
from keto_analyzer import analyze_food_text, analyze_barcode_image

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("🥗 Keto_Atkins_Bot is online. Waiting for food or barcodes...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a food name (like 'Egg'), a restaurant ('McDonalds'), or a PHOTO of a barcode!")

# 1. HANDLE TEXT
@bot.message_handler(content_types=['text'])
def handle_food_query(message):
    query = message.text
    print(f"🔍 Searching: {query}")
    response = analyze_food_text(query)
    bot.reply_to(message, response, parse_mode='Markdown')

# 2. HANDLE PHOTOS (Barcodes)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print("📸 Photo received...")
    try:
        # Get the file ID of the largest photo (Telegram sends multiple sizes)
        file_info = bot.get_file(message.photo[-1].file_id)
        
        # Download the image bytes
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Send to Analyzer
        bot.reply_to(message, "👀 Scanning barcode...")
        response = analyze_barcode_image(downloaded_file)
        
        bot.reply_to(message, response, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error handling photo: {e}")

if __name__ == "__main__":
    bot.infinity_polling()