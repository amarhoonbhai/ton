
import time
import requests
import json
import os

from config import CHANNEL_USERNAME
from detector import detect_upgrade_changes
from poster import send_gift_post

API_URL = "https://fragment.com/api/gift/"
CACHE_DIR = "gift_cache"
GIFT_IDS = ["5837059369300132790", "5167939598143193218"]  # Add more gift IDs here

os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_gift_data(gift_id):
    try:
        response = requests.get(f"{API_URL}{gift_id}")
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch gift {gift_id}: {e}")
        return None

def load_cached_gift(gift_id):
    path = os.path.join(CACHE_DIR, f"{gift_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_gift_cache(gift_id, data):
    path = os.path.join(CACHE_DIR, f"{gift_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_bot():
    while True:
        for gift_id in GIFT_IDS:
            new_data = fetch_gift_data(gift_id)
            if not new_data:
                continue

            old_data = load_cached_gift(gift_id)
            change_lines = detect_upgrade_changes(old_data, new_data)

            if change_lines:
                gift_name = new_data.get("name", "Unknown Gift")
                send_gift_post(gift_name, gift_id, change_lines)
                save_gift_cache(gift_id, new_data)

        time.sleep(60)

if __name__ == "__main__":
    run_bot()
