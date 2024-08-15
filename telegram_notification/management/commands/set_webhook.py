from django.core.management.base import BaseCommand

from telegram_notification.telegram_bot import TelegramBot


class Command(BaseCommand):
    """Django command to set webhook"""

    def handle(self, *args, **options):
        TelegramBot().set_webhook()
