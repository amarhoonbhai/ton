import asyncio
import datetime
import aiohttp
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telethon import TelegramClient
from config import api_id, api_hash, session_name, target_chat

client = TelegramClient(session_name, api_id, api_hash)

# --- TON Price Update ---

async def fetch_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["the-open-network"]["usd"]

async def post_ton_price():
    ton_price = await fetch_ton_price()
    today = datetime.datetime.utcnow().strftime("%B %d")
    caption = (
        f"🟦 TON Price Update — {today}\n\n"
        f"💰 1 TON = ${ton_price:.2f} USD\n\n"
        f"🔔 Follow @FragmentGiftUpdate for rare gift and market updates."
    )
    ton_logo_url = "https://cryptologos.cc/logos/ton-crystal-ton-logo.png?v=025"

    async with client:
        await client.send_file(
            target_chat,
            file=ton_logo_url,
            caption=caption,
            parse_mode="html"
        )
    print("✅ Posted TON price update.")

# --- Top Usernames Screenshot ---

async def post_top_usernames():
    # Setup headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1200,2000')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://fragment.com/username")
        await asyncio.sleep(5)
        driver.save_screenshot("username_full.png")

        image = Image.open("username_full.png")
        crop_box = (270, 250, 930, 600)
        cropped = image.crop(crop_box)
        cropped_path = "top_usernames_crop.png"
        cropped.save(cropped_path)

        today = datetime.datetime.utcnow().strftime("%B %d")
        caption = f"🔝 Top 5 Username Sales Today — {today}\n\nMention: @FragmentGiftUpdate"

        async with client:
            await client.send_file(
                target_chat,
                file=cropped_path,
                caption=caption,
                parse_mode="html"
            )
        print("✅ Posted top usernames update.")
    finally:
        driver.quit()

# --- Schedule Loop ---

async def scheduler():
    print("⏳ Scheduler started. Waiting for 6:00 and 9:00 UTC...")
    while True:
        now = datetime.datetime.utcnow().strftime("%H:%M")
        if now == "06:00":
            await post_ton_price()
        elif now == "09:00":
            await post_top_usernames()
        await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    asyncio.run(scheduler())