from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from book_service.models import Book
from borrowings_service.models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

        # Create a book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            daily_fee=5.00,
            inventory=10
        )

        # Create a borrowing instance
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=timezone.now().date() + timedelta(days=10)
        )

    def test_borrowing_fields(self):
        self.assertEqual(self.borrowing.book, self.book)
        self.assertEqual(self.borrowing.user, self.user)
        self.assertTrue(self.borrowing.borrow_date)
        self.assertEqual(
            self.borrowing.expected_return_date,
            (timezone.now() + timedelta(days=10)).date()
        )
        self.assertIsNone(self.borrowing.actual_return_date)

    def test_calculate_total_price(self):
        self.borrowing.borrow_date = timezone.now().date() - timedelta(days=5)
        self.borrowing.save()

        expected_total_price = (
                5.00 *
                (self.borrowing.expected_return_date
                 - self.borrowing.borrow_date).days
        )
        self.assertEqual(
            self.borrowing.calculate_total_price,
            expected_total_price
        )

    def test_borrowing_creation(self):
        borrowing = Borrowing.objects.get(id=self.borrowing.id)
        self.assertIsNotNone(borrowing)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(
            borrowing.expected_return_date,
            (timezone.now() + timedelta(days=10)).date()
        )
