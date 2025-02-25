import requests
from fastapi import HTTPException
from config import YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET, YANDEX_REDIRECT_URI

def get_yandex_access_token(code: str):
    """
    Получение access_token от Яндекса, используя authorization code.
    """
    token_url = "https://oauth.yandex.ru/token"
    data = {
        "code": code,
        "client_id": YANDEX_CLIENT_ID,
        "client_secret": YANDEX_CLIENT_SECRET,
        "redirect_uri": YANDEX_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Ошибка при получении токена Яндекса")
    
    return response.json()


def get_user_info(access_token: str):
    """
    Получаем информацию о пользователе с использованием access_token.
    """
    user_info_url = "https://login.yandex.ru/info"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(user_info_url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Ошибка при получении данных пользователя из Яндекса")
    
    return response.json()
