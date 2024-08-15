import os
import logging

from dotenv import load_dotenv
import requests
from borrowings_service.models import Borrowing


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

    def borrow_administration_notification(self, borrowing: Borrowing):
        """send notification to administration about new and overdue borrow"""
        message = (
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}\n"
            f"Book: {borrowing.book}\n"
            f"User: {borrowing.user}"
        )
        self._send_message(self._chat_id, message)

    def borrow_user_notification(self, borrowing: Borrowing, telegram_id: int):
        """send notification to user about their borrowing"""
        message = (
            f"Borrow date: {borrowing.borrow_date}\n"
            f"Expected return date: {borrowing.expected_return_date}\n"
            f"Book: {borrowing.book}\n"
            f"User: {borrowing.user}"
        )
        self._send_message(telegram_id, message)

    def multiple_borrow_administration_notification(
        self, borrowing_list: list[Borrowing]
    ):
        for borrowing in borrowing_list:
            self.borrow_administration_notification(borrowing)

    def successful_payment_administration_notification(self, payment: "Payment"):
        """send notification to administration about succesful payment"""
        message = (
            f"User: {payment.borrowing.user}\n"
            f"Paid: {payment.type}\n"
            f"For: {payment.borrowing.book}\n"
            f"The amount: {payment.money_to_pay}$"
        )
        self._send_message(self._chat_id, message)

    def set_webhook(self, server_url=os.environ["SERVER_URL"]):
        webhook_url = f"{server_url}/api/telegram/reviece_telegram_messages/"
        response = requests.post(
            f"{self.base_url}/setWebhook",
            params={"url": webhook_url, "drop_pending_updates": True},
        )
        if response.status_code != 200:
            logging.warning(f"Webhook wasn't set: {response.content}")

    def send_connection_confirm_message_to_user(self, to: int):
        self._send_message(to, "Successful connected")
