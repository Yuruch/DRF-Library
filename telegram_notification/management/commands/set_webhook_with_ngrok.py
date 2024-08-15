from django.core.management.base import BaseCommand

from telegram_notification.telegram_bot import TelegramBot
from telegram_notification.utils import get_ngrok_url


class Command(BaseCommand):
    """Django command to set webhook"""

    def handle(self, *args, **options):
        ngrok_url = get_ngrok_url()
        TelegramBot().set_webhook(ngrok_url)
