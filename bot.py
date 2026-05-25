import requests
import time
import json

# ================= CONFIG =================

TOKEN = "8898513998:AAGRAuFVfv049QDmnaeMlm3W1FfZuR-vUMg"
URL = f"https://api.telegram.org/bot{TOKEN}"

WEBAPP_URL = "https://boryknews.net.ua/app"

offset = 0

# ================= API =================

def get_updates():
    global offset

    try:
        r = requests.get(
            f"{URL}/getUpdates",
            params={
                "offset": offset,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query"]
            },
            timeout=35
        )

        return r.json()

    except Exception as e:
        print("GET UPDATES ERROR:", e)
        return {}


def send_message(chat_id, text, reply_markup=None):

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    try:
        requests.post(
            f"{URL}/sendMessage",
            data=data,
            timeout=15
        )

    except Exception as e:
        print("SEND MESSAGE ERROR:", e)


def edit_message(chat_id, message_id, text, reply_markup=None):

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    try:
        requests.post(
            f"{URL}/editMessageText",
            data=data,
            timeout=15
        )

    except Exception as e:
        print("EDIT MESSAGE ERROR:", e)


def answer_callback(callback_id):

    try:
        requests.post(
            f"{URL}/answerCallbackQuery",
            data={
                "callback_query_id": callback_id
            },
            timeout=10
        )

    except Exception as e:
        print("CALLBACK ERROR:", e)

# ================= MENUS =================

def main_menu():

    return {
        "inline_keyboard": [

            [
                {
                    "text": "🚀 Відкрити BorykNews",
                    "web_app": {
                        "url": WEBAPP_URL
                    }
                }
            ],

            [
                {
                    "text": "🏙 Новини",
                    "callback_data": "news"
                },

                {
                    "text": "🚨 Терміново",
                    "callback_data": "urgent"
                }
            ],

            [
                {
                    "text": "⚠️ Тривоги",
                    "callback_data": "alarm"
                },

                {
                    "text": "🚌 Транспорт",
                    "callback_data": "transport"
                }
            ],

            [
                {
                    "text": "💡 ЖКГ",
                    "callback_data": "utilities"
                },

                {
                    "text": "🌤 Погода",
                    "callback_data": "weather"
                }
            ],

            [
                {
                    "text": "📢 Оголошення",
                    "callback_data": "ads"
                }
            ],

            [
                {
                    "text": "🗺 Карта тривог LIVE",
                    "url": "https://alerts.in.ua"
                }
            ]
        ]
    }


def back_menu():

    return {
        "inline_keyboard": [
            [
                {
                    "text": "⬅️ Назад",
                    "callback_data": "back"
                }
            ]
        ]
    }

# ================= TEXTS =================

def get_text(action):

    texts = {

        "menu":
        "🔥 <b>BorykNews | Бориспіль</b>\n\n"
        "📍 Оперативні новини міста\n"
        "⚡ LIVE оновлення 24/7\n\n"
        "👇 Виберіть розділ:",

        "news":
        "🏙 <b>НОВИНИ БОРИСПОЛЯ</b>\n\n"
        "📰 Оперативні новини міста\n"
        "📍 Події • ДТП • Важливе\n\n"
        "⚡ BorykNews LIVE",

        "urgent":
        "🚨 <b>ТЕРМІНОВО</b>\n\n"
        "⚠️ Важливі події міста\n"
        "📡 LIVE оновлення",

        "alarm":
        "⚠️ <b>ПОВІТРЯНА ТРИВОГА</b>\n\n"
        "🛑 Перейдіть в укриття\n"
        "📡 Слідкуйте за оновленнями",

        "transport":
        "🚌 <b>ТРАНСПОРТ</b>\n\n"
        "▪️ Маршрути\n"
        "▪️ Онлайн рух\n"
        "▪️ Перекриття",

        "utilities":
        "💡 <b>ЖКГ</b>\n\n"
        "▪️ Світло\n"
        "▪️ Вода\n"
        "▪️ Аварії",

        "weather":
        "🌤 <b>ПОГОДА</b>\n\n"
        "📍 Бориспіль\n"
        "🌡 Актуальний прогноз",

        "ads":
        "📢 <b>ОГОЛОШЕННЯ</b>\n\n"
        "▪️ Робота\n"
        "▪️ Оренда\n"
        "▪️ Послуги"
    }

    return texts.get(action, "Помилка")

# ================= START =================

print("🚀 BorykNews BOT запущено...")

# ================= LOOP =================

while True:

    try:

        data = get_updates()

        if "result" in data:

            for update in data["result"]:

                offset = update["update_id"] + 1

                # ================= CALLBACK =================

                if "callback_query" in update:

                    callback = update["callback_query"]

                    callback_id = callback["id"]

                    message = callback["message"]

                    chat_id = message["chat"]["id"]

                    message_id = message["message_id"]

                    data_cb = callback["data"]

                    answer_callback(callback_id)

                    # BACK
                    if data_cb == "back":

                        edit_message(
                            chat_id,
                            message_id,
                            get_text("menu"),
                            reply_markup=main_menu()
                        )

                    else:

                        edit_message(
                            chat_id,
                            message_id,
                            get_text(data_cb),
                            reply_markup=back_menu()
                        )

                # ================= MESSAGE =================

                if "message" in update:

                    message = update["message"]

                    chat_id = message["chat"]["id"]

                    text = message.get("text", "")

                    if text == "/start":

                        send_message(
                            chat_id,
                            get_text("menu"),
                            reply_markup=main_menu()
                        )

                    else:

                        send_message(
                            chat_id,
                            "👇 Натисніть /start"
                        )

    except Exception as e:

        print("MAIN LOOP ERROR:", e)

    time.sleep(1)
