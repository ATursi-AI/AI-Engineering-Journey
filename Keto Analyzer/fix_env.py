# fix_env.py
env_content = """TELEGRAM_TOKEN=8509805374:AAFDKX1eHnVSvfcOjMYqwE8Mf3fzi0E8-Wo
GEMINI_API_KEY=PASTE_YOUR_GEMINI_KEY_HERE
FATSECRET_CLIENT_ID=PASTE_YOUR_ID_HERE
FATSECRET_CLIENT_SECRET=PASTE_YOUR_SECRET_HERE"""

with open(".env", "w", encoding="utf-8") as f:
    f.write(env_content.strip())

print("✅ Your .env file has been recreated with perfect formatting.")