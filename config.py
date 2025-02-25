from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kafka import KafkaProducer
import json

DB_HOST = "localhost"
DB_NAME = "auth_db"
DB_USER = "postgres"
DB_PASSWORD = "123"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TELEGRAM_BOT_TOKEN = "ата та"
TELEGRAM_CHAT_ID = "милые котята"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "user_registered"

YANDEX_CLIENT_ID = "чикиряу"
YANDEX_CLIENT_SECRET = "не расскажу"
YANDEX_REDIRECT_URI = "http://127.0.0.1:8000/auth/yandex/callback"

kafka_producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS ],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


