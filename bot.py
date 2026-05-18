from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 беремо дані з Render
TOKEN = os.environ.get("8263855758:AAELXWQ8R5wS8NTypqvk0emd_YCwdOrkuxg")
CHAT_ID = os.environ.get("CHAT_ID")

# 📩 відправка в Telegram
def send_to_telegram(text):
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN missing")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    r = requests.post(url, data=payload)
    print(r.text)

# 🟢 перевірка сервера
@app.route("/", methods=["GET"])
def home():
    return "🟢 BorykNews bot is running 🚀"

# 🔥 webhook для новин
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    title = data.get("title")
    link = data.get("link")

    message = f"📰 <b>{title}</b>\n\n🔗 {link}"
    send_to_telegram(message)

    return "ok"

# 🚀 запуск для Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
