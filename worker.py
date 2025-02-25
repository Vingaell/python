import json
from kafka import KafkaConsumer
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, KAFKA_BOOTSTRAP_SERVERS

consumer = KafkaConsumer(
    "user_registered",  
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(text):
    """ Функция отправки сообщения в Telegram """
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(TELEGRAM_API_URL, data=data)
    print("Ответ от Telegram:", response.json())  
    return response.json()

print("👀 Worker запущен, слушает Kafka...")

for message in consumer:
    event = message.value
    print(f"🔥 Получено событие из Kafka: {event}")

    if event.get("event") == "user_registered":
        user_name = event.get("user_name", "Неизвестный пользователь")
        user_email = event.get("user_email", "нет email")

        telegram_text = f"👤 Новый пользователь зарегистрирован!\n\nИмя: {user_name}\nEmail: {user_email}"
        send_telegram_message(telegram_text)




