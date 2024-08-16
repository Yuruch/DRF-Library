import sys
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    """Django command to run migrations and then start the server"""

    help = "Runs migrations before starting the development server"

    def handle(self, *args, **options):
        call_command("migrate")
        call_command("runserver", "0.0.0.0:8000")
