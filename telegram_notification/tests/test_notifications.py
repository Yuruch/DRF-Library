from django.test import TestCase
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from telegram_notification.telegram_bot import TelegramBot
from borrowings_service.models import Borrowing
from book_service.models import Book


class BorrowingNotificationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@test.test")
        self.bot = TelegramBot()
        self.book = Book.objects.create(
            title="asd", author="das", cover="HARD", inventory=5, daily_fee=32.3
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=datetime.now().date(), book=self.book, user=self.user
        )

    def test_borrowing_notification_administration(self):
        self.bot.borrow_administration_notification(self.borrowing)
