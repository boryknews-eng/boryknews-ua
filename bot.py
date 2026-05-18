from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Беремо дані з Render Environment Variables
TOKEN = os.environ.get("8623387819:AAF20O9wm5B2gzAcTn-kxQhG1sPXa26kk-Q")
CHAT_ID = os.environ.get("CHANNEL_USERNAME")

# Відправка в Telegram
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

# Webhook (сюди буде стукати WordPress)
@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    title = data.get("title", "Без заголовка")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 Деталі: {link}"
    send_to_telegram(message)

    return "ok"

# Перевірка чи сервер живий
@app.route("/", methods=["GET"])
def home():
    return "BorykNews bot is running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
