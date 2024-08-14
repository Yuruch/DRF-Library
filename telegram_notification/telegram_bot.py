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
        params = {"chat_id": to, "text": message}
        headers = {"Content-Type": "application/json"}
        request = requests.post(
            f"{self.base_url}/sendMessage", params=params, headers=headers
        )
        if request.status_code != 200:
            logging.warning(f"Message is not send: {request.content}")

    def borrow_administration_notification(self, borrow: "Borrow"):
        """send notification to administration about new and overdue borrow"""
        message = (
            f"Borrow date: {borrow.borrow_date}\n"
            f"Expected return date: {borrow.expected_return_date}\n"
            f"Book: {borrow.book}\n"
            f"User: {borrow.user}"
        )
        self._send_message(self._chat_id, message)

    def multiple_borrow_administration_notification(self, borrows: list["Borrow"]):
        for borrow in borrows:
            self.borrow_administration_notification(borrow)

    def successful_payment_administration_notification(self, payment: "Payment"):
        """send notification to administration about succesful payment"""
        message = (
            f"User: {payment.borrowing.user}\n"
            f"Paid: {payment.type}\n"
            f"For: {payment.borrowing.book}\n"
            f"The amount: {payment.money_to_pay}$"
        )
        self._send_message(self._chat_id, message)
