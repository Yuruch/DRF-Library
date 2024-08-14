from celery import shared_task
from django.utils import timezone

from borrowings_service.models import Borrowing
from telegram_notification.telegram_bot import TelegramBot


@shared_task
def check_overdue_borrowings():
    """Checks whether there are overdue borrowings and runs periodic task"""
    now = timezone.now()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=now,
        actual_return_date__isnull=True
    )

    if overdue_borrowings.exists():
        bot = TelegramBot()
        bot.multiple_borrow_administration_notification(overdue_borrowings)
