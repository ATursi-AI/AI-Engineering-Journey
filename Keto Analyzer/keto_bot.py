import os
import telebot
from dotenv import load_dotenv
from keto_analyzer import analyze_food_text, analyze_barcode_image
from user_data import log_food, get_daily_stats

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("🥗 Keto Prime AI is online...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
                 "🚀 **Keto Prime Future AI**\n\n"
                 "1. **Scan/Search:** Send a food name or photo.\n"
                 "2. **Track:** I automatically log what you scan.\n"
                 "3. **Check:** Type /stats to see your daily fuel gauge.")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    stats = get_daily_stats(message.from_user.id)
    if not stats:
        bot.reply_to(message, "📉 Your daily log is empty. Scan some food first!")
        return

    # Create the Future Dashboard
    response = (
        "🏎️ **DAILY FUEL GAUGE**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🍞 **Net Carbs:** `{stats['carbs']:.1f}g`\n"
        f"🥓 **Fat:** `{stats['fat']:.1f}g`\n"
        f"🥩 **Protein:** `{stats['protein']:.1f}g`\n"
        f"🔥 **Calories:** `{stats['calories']:.0f}`\n\n"
        "_(Resets automatically at midnight)_"
    )
    bot.reply_to(message, response, parse_mode='Markdown')

def process_and_reply(message, response_package):
    text = response_package.get("text")
    image_url = response_package.get("image")
    stats = response_package.get("stats")
    name = response_package.get("name")
    
    # 1. Send the Result
    if image_url:
        try:
            bot.send_photo(message.chat.id, image_url, caption=text, parse_mode='Markdown')
        except:
            bot.reply_to(message, text, parse_mode='Markdown')
    else:
        bot.reply_to(message, text, parse_mode='Markdown')

    # 2. Log to Database (The Future Feature)
    if stats and name:
        log_food(message.from_user.id, name, stats)
        # Optional: Confirm logging
        # bot.send_message(message.chat.id, "✅ Added to daily log.")

@bot.message_handler(content_types=['text'])
def handle_food_query(message):
    print(f"🔍 Searching: {message.text}")
    response_package = analyze_food_text(message.text)
    process_and_reply(message, response_package)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print("📸 Photo received...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, "👀 Scanning barcode...")
        
        response_package = analyze_barcode_image(downloaded_file)
        process_and_reply(message, response_package)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

if __name__ == "__main__":
    bot.infinity_polling()