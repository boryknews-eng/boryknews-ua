from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 TOKEN з Render ENV
TOKEN = os.environ.get("8623387819:AAF20O9wm5B2gzAcTn-kxQhG1sPXa26kk-Q")

# 📢 канал
CHAT_ID = "-1001234567890"


def send_to_telegram(text):
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN is missing")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    r = requests.post(url, data=payload)
    print("Telegram response:", r.text)


@app.route("/", methods=["GET"])
def home():
    return "🟢 BorykNews bot is running 🚀", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)

    if not data:
        return "no data", 400

    title = data.get("title", "Без заголовка")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 {link}"

    send_to_telegram(message)

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
