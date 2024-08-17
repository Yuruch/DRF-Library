import time

from django.core.management.base import BaseCommand

from telegram_notification.telegram_bot import TelegramBot
from telegram_notification.utils import get_ngrok_url


class Command(BaseCommand):
    """Django command to wait for ngrok and setting webhook with it"""

    def handle(self, *args, **options):
        ngrok_url = ""

        self.stdout.write("Waiting for ngrok to be ready...")

        while not ngrok_url:
            ngrok_url = get_ngrok_url()
            time.sleep(1)

        TelegramBot().set_webhook(ngrok_url)
        self.stdout.write(
            self.style.SUCCESS(f"Ngrok is ready! Webhook set to {ngrok_url}")
        )
