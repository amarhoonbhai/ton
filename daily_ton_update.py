import asyncio
import datetime
import aiohttp
from telethon import TelegramClient
from telethon.tl.types import InputMediaPhoto

from config import api_id, api_hash, session_name, target_chat

client = TelegramClient(session_name, api_id, api_hash)

async def fetch_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data["the-open-network"]["usd"]

async def send_daily_ton_update():
    ton_price = await fetch_ton_price()
    today = datetime.datetime.utcnow().strftime("%B %d")
    caption = (
        f"🟦 TON Price Update — {today}\n\n"
        f"💰 1 TON = ${ton_price:.2f} USD\n\n"
        f"🔔 Follow @FragmentGiftUpdate for rare gift and market updates."
    )

    async with client:
        await client.send_file(
            target_chat,
            file="ton_logo.png",  # Must be in the same directory
            caption=caption,
            parse_mode="html"
        )

if __name__ == "__main__":
    asyncio.run(send_daily_ton_update())