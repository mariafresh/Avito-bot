           import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TG_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL")
# Используем мобильную версию профиля
URL = "https://m.avito.ru/user/2079f9860fb0d9647c5edd3175df709c/profile"

def send_telegram(text):
    if not TOKEN or not CHANNEL_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code != 200:
            print("Блокировка сохраняется.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', attrs={'data-marker': True})
        
        found = 0
        for item in items:
            marker = item.get('data-marker', '')
            if 'item-' in marker:
                found += 1
                text = item.text.strip()
                print(f"Найдено: {text[:50]}")

        print(f"Всего товаров: {found}")
        
    except Exception as e:
        print(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    main() 
