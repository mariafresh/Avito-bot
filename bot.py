import os
import requests

TOKEN = os.environ.get("TG_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL")
# ID пользователя из ссылки профиля
USER_ID = "2079f9860fb0d9647c5edd3175df709c"

def send_telegram(text):
    if not TOKEN or not CHANNEL_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHANNEL_ID, "text": text})
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def main():
    # Используем мобильный API-метод Авито, который возвращает данные в JSON
    api_url = f"https://m.avito.ru/api/1/items?filter[user]={USER_ID}"
    
    headers = {
        "User-Agent": "Avito/198.0 (Android; 11; Scale/2.75)",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        print(f"Статус ответа API: {response.status_code}")
        
        if response.status_code != 200:
            print("API заблокировало запрос.")
            return

        data = response.json()
        items = data.get("items", [])
        
        found = len(items)
        print(f"Всего товаров через API: {found}")
        
        for item in items:
            title = item.get("title", "Без названия")
            price = item.get("price", {}).get("value", "Цена не указана")
            print(f"Товар: {title} — {price} руб.")
            
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")

if __name__ == "__main__":
    main()
