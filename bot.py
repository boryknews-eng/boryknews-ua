from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 змінні з Render
TOKEN = os.environ.get("8623387819:AAF20O9wm5B2gzAcTn-kxQhG1sPXa26kk-Q")
CHAT_ID = os.environ.get("CHANNEL_USERNAME", "@BorykNews")


# 📩 відправка в Telegram
def send_to_telegram(text):
    if not TOKEN:
        print("❌ No Telegram token")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


# 🔥 webhook (сюди приходять пости)
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)

    if not data:
        return "no data", 400

    title = data.get("title", "Без заголовка")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 Деталі: {link}"

    send_to_telegram(message)

    return "ok", 200


# 🟢 перевірка що сервер живий
@app.route("/", methods=["GET"])
def home():
    return "BorykNews bot is running 🚀", 200


# 🚀 ОБОВʼЯЗКОВО ДЛЯ RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
