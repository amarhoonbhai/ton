from telethon.sync import TelegramClient
from config import api_id, api_hash, session_name

client = TelegramClient(session_name, api_id, api_hash)

print("📱 Logging in to Telegram...")
client.start()
print("✅ Login successful. Session saved.")