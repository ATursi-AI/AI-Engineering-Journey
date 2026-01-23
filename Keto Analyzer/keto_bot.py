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

def send_smart_reply(message, response_package):
    """
    Helper function to send image + text if image exists, or just text.
    """
    text = response_package.get("text")
    image_url = response_package.get("image")
    
    if image_url:
        try:
            bot.send_photo(message.chat.id, image_url, caption=text, parse_mode='Markdown')
        except Exception as e:
            # If image fails (bad url), fallback to text
            print(f"Image failed: {e}")
            bot.reply_to(message, text, parse_mode='Markdown')
    else:
        bot.reply_to(message, text, parse_mode='Markdown')

# 1. HANDLE TEXT
@bot.message_handler(content_types=['text'])
def handle_food_query(message):
    query = message.text
    print(f"🔍 Searching: {query}")
    
    # Get the Package (Dict)
    response_package = analyze_food_text(query)
    
    # Send it smartly
    send_smart_reply(message, response_package)

# 2. HANDLE PHOTOS (Barcodes)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print("📸 Photo received...")
    try:
        # Get the file ID of the largest photo
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        bot.reply_to(message, "👀 Scanning barcode...")
        
        # Get the Package (Dict)
        response_package = analyze_barcode_image(downloaded_file)
        
        # Send it smartly
        send_smart_reply(message, response_package)
        
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error handling photo: {e}")

if __name__ == "__main__":
    bot.infinity_polling()