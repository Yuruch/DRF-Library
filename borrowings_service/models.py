from datetime import datetime

from django.db import models

from book_service.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateField(default=datetime.now)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
