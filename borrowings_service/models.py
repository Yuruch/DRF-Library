from datetime import timedelta

from django.conf import settings
from django.db import models

from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    @property
    def calculate_total_price(self):
        days = (self.expected_return_date - self.borrow_date).days
        daily_fee = self.book.daily_fee

        return days * daily_fee
