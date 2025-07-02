import asyncio
import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telethon import TelegramClient
from config import api_id, api_hash, session_name, target_chat

client = TelegramClient(session_name, api_id, api_hash)

async def send_top_usernames_image():
    # Setup headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1200,2000')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://fragment.com/username")
        await asyncio.sleep(5)  # Let page load
        screenshot_path = "username_full.png"
        cropped_path = "top_usernames_crop.png"
        driver.save_screenshot(screenshot_path)

        # Crop coordinates based on visual test (adjust as needed)
        image = Image.open(screenshot_path)
        crop_box = (270, 250, 930, 600)  # Left, Top, Right, Bottom (customizable)
        cropped = image.crop(crop_box)
        cropped.save(cropped_path)

        # Format message
        today = datetime.datetime.utcnow().strftime("%B %d")
        caption = (
            f"🔝 Top 5 Username Sales Today — {today}\n\n"
            f"Mention: @FragmentGiftUpdate"
        )

        async with client:
            await client.send_file(
                target_chat,
                file=cropped_path,
                caption=caption,
                parse_mode="html"
            )

    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(send_top_usernames_image())