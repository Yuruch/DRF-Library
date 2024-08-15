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

    overdue_borrowings_with_telegram_id = overdue_borrowings.filter(
        user__telegram_id__isnull=False
    )

    bot = TelegramBot()

    if overdue_borrowings.exists():
        bot.multiple_borrow_administration_notification(overdue_borrowings)

    for borrowing in overdue_borrowings_with_telegram_id:
        bot.borrow_user_notification(borrowing, borrowing.user.telegram_id)
