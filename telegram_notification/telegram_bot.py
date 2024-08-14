import os
import requests

from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
load_dotenv()

class TelegramBot:
    def __init__(self) -> None:
        self._chat_id = int(os.environ["ADMINISTRATION_CHAT_ID"])
        self._api_token = os.environ["TELEGRAM_BOT_KEY"]
        self.base_url = f"https://api.telegram.org/bot{self._api_token}"

    def _send_message(self, to: int, message: str) -> None:
        params = {
            "chat_id": to,
            "text": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        request = requests.post(
            f"{self.base_url}/sendMessage",
            params=params,
            headers=headers
        )
        if request.status_code != 200:
            logging.warning(f"Message is not send: {request.content}")
