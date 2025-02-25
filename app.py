from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse  
from sqlalchemy.orm import Session
import requests
import jwt
import datetime
from models import User, LoginHistory, SessionLocal, init_db
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, kafka_producer, KAFKA_TOPIC, YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET, YANDEX_REDIRECT_URI
from pydantic import BaseModel
from yandex_oauth import get_yandex_access_token, get_user_info  
import json

app = FastAPI()

SECRET_KEY = "mysecret"

init_db()

class UserCreate(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    print("Ответ Telegram:", response.json())

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь уже существует")

        user_data = User(email=user.email, password_hash=user.password, role="user")
        db.add(user_data)
        db.commit()
        db.refresh(user_data)

        event = {"event": "user_registered", "user_email": user.email}
        kafka_producer.send(KAFKA_TOPIC, event)
        kafka_producer.flush()



    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or user.password_hash != password:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256",
        )

        history = LoginHistory(user_id=user.id, ip_address="127.0.0.1")
        db.add(history)
        db.commit()

        return {"access_token": token}

    except Exception as e:
        print(f"Ошибка при попытке входа: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@app.get("/auth/yandex")
def yandex_auth():
    """
    Перенаправляет пользователя на страницу авторизации Яндекса.
    """
    yandex_auth_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={YANDEX_CLIENT_ID}&redirect_uri={YANDEX_REDIRECT_URI}"
    return RedirectResponse(url=yandex_auth_url)

@app.get("/auth/yandex/callback")
def yandex_callback(code: str, db: Session = Depends(get_db)):
    """
    Обрабатывает колбэк после авторизации через Яндекс.
    Получает access_token и информацию о пользователе.
    """
    try:
        token_response = get_yandex_access_token(code)
        access_token = token_response["access_token"]
        
        user_data = get_user_info(access_token)
        
        existing_user = db.query(User).filter(User.email == user_data["default_email"]).first()
        if not existing_user:

            user = User(email=user_data["default_email"], password_hash="", role="user")
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            user = existing_user

        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256",
        )

        send_telegram_message(f"👤 Новый пользователь авторизовался через Яндекс!\n\nEmail: {user_data['default_email']}")

        return {"access_token": token}
    
    except Exception as e:
        print(f"Ошибка при авторизации через Яндекс: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при авторизации через Яндекс")






