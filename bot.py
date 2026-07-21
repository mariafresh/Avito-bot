import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TG_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL")
TARGET_URL = "https://www.avito.ru/user/2079f9860fb0d9647c5edd3175df709c/profile?view=dg&src=sharing"

def send_telegram(text):
    if not TOKEN or not CHANNEL_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def main():
    # Используем публичный API-прокси для обхода блокировок дата-центров
    api_url = f"https://api.allorigins.win/get?url={requests.utils.quote(TARGET_URL)}"
    
    try:
        response = requests.get(api_url, timeout=30)
        print(f"Статус ответа прокси: {response.status_code}")
        
        data = response.json()
        html_content = data.get("contents", "")
        
        if not html_content:
            print("Не удалось получить содержимое страницы.")
            return

        soup = BeautifulSoup(html_content, 'html.parser')
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
        print(f"Ошибка при запросе: {e}")

if __name__ == "__main__":
    main()
