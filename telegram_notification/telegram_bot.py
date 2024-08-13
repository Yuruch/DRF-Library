import os
import requests

from dotenv import load_dotenv


load_dotenv()

class TelegramBot:
    def __init__(self):
        self._api_token = os.environ["TELEGRAM_BOT_KEY"]
        self._chat_id = os.environ["ADMINISTRATION_CHAT_ID"]
        if not self._chat_id or not self._chat_id.isnumeric():
            # todo raise error that dont interupt whole django project
            pass
        if not self._api_token:
            # todo raise error
            pass

    def _send_message(self, to: int, message: str):
        params = {
            "chat_id": to,
            "text": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        request = requests.post(
            f"https://api.telegram.org/bot{self._api_token}/sendMessage",
            params=params,
            headers=headers
        )
