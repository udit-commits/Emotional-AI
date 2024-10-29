import requests
import os

token = os.environ["TELEGRAM_BOT_TOKEN"]


def send_message(chat_id, text):
    requests.post(
        url="https://api.telegram.org/bot{0}/sendMessage".format(token),
        data={
            "chat_id": chat_id,
            "text": text,
            "link_preview_options": '{"is_disabled": true}',
        },
    )