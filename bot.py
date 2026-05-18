from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 ENV VARIABLES (Render)
TOKEN = os.environ.get("8263855758:AAELXWQ8R5wS8NTypqvk0emd_YCwdOrkuxg")
CHAT_ID = os.environ.get("@BorykNews")

# 📩 Telegram send function
def send_to_telegram(text):
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN missing")
        return

    if not CHAT_ID:
        print("❌ CHAT_ID missing")
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

# 🟢 Home route
@app.route("/", methods=["GET"])
def home():
    return "🟢 BorykNews bot is running 🚀"

# 🔥 Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return "no data", 400

    title = data.get("title", "No title")
    link = data.get("link", "")

    message = f"📰 <b>{title}</b>\n\n🔗 {link}"

    send_to_telegram(message)

    return "ok", 200


# 🚀 Run (Render ignores this)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
