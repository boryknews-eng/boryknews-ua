from flask import Flask, request
import requests
import os

app = Flask(__name__)

# беремо змінні з Render
TOKEN = os.environ.get("8623387819:AAF20O9wm5B2gzAcTn-kxQhG1sPXa26kk-Q")
CHAT_ID = os.environ.get("CHANNEL_USERNAME")

# якщо щось не задано — не падаємо
if not TOKEN:
    TOKEN = ""
if not CHAT_ID:
    CHAT_ID = "@BorykNews"


def send_to_telegram(text):
    if not TOKEN:
        print("No Telegram token!")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


# 🔥 webhook від WordPress
@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return "no data", 400

    title = data.get("title", "Без заголовка")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 Деталі: {link}"
    send_to_telegram(message)

    return "ok", 200


# 🟢 перевірка чи сервер живий
@app.route("/", methods=["GET"])
def home():
    return "BorykNews bot is running 🚀", 200


# 🚀 ВАЖЛИВО ДЛЯ RENDER (це вирішує помилки запуску)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
