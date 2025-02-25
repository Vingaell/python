import requests
import time
from config import TELEGRAM_BOT_TOKEN

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(TELEGRAM_API_URL + "getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(TELEGRAM_API_URL + "sendMessage", data=data)

def main():
    last_update_id = None
    print("Бот запущен! 🔥")

    while True:
        updates = get_updates(last_update_id)
        
        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                
                send_message(chat_id, f"Ты(я(ты(я(ты(я))))) написал: {text}")

        time.sleep(1)  

if __name__ == "__main__":
    main()

