from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 ENV VARIABLES (Render)
TOKEN = os.environ.get("8623387819:AAF20O9wm5B2gzAcTn-kxQhG1sPXa26kk-Q")
CHAT_ID = os.environ.get("CHANNEL_USERNAME", "@BorykNews")


# 📩 ВІДПРАВКА В TELEGRAM
def send_to_telegram(text):
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN is missing")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        r = requests.post(url, data=payload, timeout=10)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Telegram error:", e)


# 🟢 ПЕРЕВІРКА СЕРВЕРА (БРАУЗЕР)
@app.route("/", methods=["GET"])
def home():
    return "🟢 BorykNews bot is running 🚀", 200


# 🔥 WEBHOOK (сюди приходять новини)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True)

    if not data:
        return "no data", 400

    title = data.get("title", "Без заголовка")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 Деталі: {link}"

    send_to_telegram(message)

    return "ok", 200


# 🚀 ЗАПУСК ДЛЯ RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
