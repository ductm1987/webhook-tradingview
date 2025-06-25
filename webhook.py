from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "7732088541:AAHWkqKAo6hn7bQcE2eLEF89PmSuGIWZq4U"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or "-1002894747074"

@app.route('/')
def home():
    return "Webhook is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        entry = data.get("entry")
        sl = data.get("sl")
        tp = data.get("tp")
        message = data.get("message")

        text = message or f"🚀 Entry: {entry}\n🛑 Stop Loss: {sl}\n🎯 Take Profit: {tp}"

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }

        res = requests.post(url, json=payload)
        return {'ok': True, 'telegram_response': res.json()}

    except Exception as e:
        return {'ok': False, 'error': str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sẽ đặt PORT
    app.run(host="0.0.0.0", port=port)
