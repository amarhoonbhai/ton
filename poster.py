
from telebot import TeleBot
from bot_config import BOT_TOKEN, CHANNEL_USERNAME

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')

def send_gift_post(gift_name, gift_id, change_lines):
    if not change_lines:
        return

    message = f"🎁 {gift_name}\n" + "\n".join(change_lines) + "\n\n📢 Follow @FragmentGiftUpdate for more"
    image_url = f"https://cdn.changes.tg/original/{gift_id}.png"

    try:
        bot.send_photo(CHANNEL_USERNAME, image_url, caption=message)
        print(f"✅ Sent update for: {gift_name}")
    except Exception as e:
        print(f"❌ Failed to send update for {gift_name}: {e}")
