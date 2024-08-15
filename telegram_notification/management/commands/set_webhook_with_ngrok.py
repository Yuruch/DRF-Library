import requests
from django.core.management.base import BaseCommand
import logging

from telegram_notification.telegram_bot import TelegramBot


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django command to set webhook"""

    def handle(self, *args, **options):
        response = requests.get("http://host.docker.internal:4040/api/tunnels")
        if response.status_code == 200:
            data = response.json()
            if data["tunnels"]:
                ngrok_url = data["tunnels"][0]["public_url"]
                TelegramBot().set_webhook(ngrok_url)
                logger.info(f"Ngrok url: {ngrok_url}")
            else:
                logger.warning("No tunnels found.")
        else:
            logger.warning(f"Failed to get tunnels: {response.status_code}")
