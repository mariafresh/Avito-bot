
import os
import time
import random
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
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    time.sleep(random.uniform(3, 7))
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.avito.ru/"
    }
    
    resp = scraper.get(URL, headers=headers)
    print(f"Статус ответа: {resp.status_code}")
    
    if resp.status_code != 200:
        print("Авито всё еще блокирует запрос (429).")
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

    print(f"Всего товаров: {found}")

if __name__ == "__main__":
    main()
