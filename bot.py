import os
import time
import cloudscraper
from bs4 import BeautifulSoup
import requests

TOKEN = os.environ.get("TG_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL")
URL = "https://www.avito.ru/user/2079f9860fb0d9647c5edd3175df709c/profile?view=dg&src=sharing"

def send_telegram(text):
    if not TOKEN or not CHANNEL_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def main():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    time.sleep(2)
    resp = scraper.get(URL)
    print(f"Статус ответа: {resp.status_code}")
    
    if resp.status_code != 200:
        print("Авито заблокировал запрос.")
        return

    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.find_all('div', attrs={'data-marker': True})
    
    found = 0
    for item in items:
        marker = item.get('data-marker', '')
        if 'item-' in marker:
            found += 1
            text = item.text.strip()
            print(f"Найдено: {text[:50]}")
            # send_telegram(f"📢 Новое объявление:\n{text}")

    print(f"Всего товаров: {found}")

if __name__ == "__main__":
    main()
