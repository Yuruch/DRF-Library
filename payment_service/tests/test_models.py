from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from book_service.models import Book
from borrowings_service.models import Borrowing
from payment_service.models import Payment


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book", daily_fee=Decimal("2.00"), inventory=10
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://example.com/session",
            session_id="test_session_id",
            money_to_pay=Decimal("14.00"),
        )
        self.assertEqual(str(payment), "PAYMENT - PENDING - $14.00")
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertEqual(payment.type, Payment.Type.PAYMENT)
        self.assertEqual(payment.borrowing, self.borrowing)
        self.assertEqual(payment.session_url, "https://example.com/session")
        self.assertEqual(payment.session_id, "test_session_id")
        self.assertEqual(payment.money_to_pay, Decimal("14.00"))

    def test_payment_money_to_pay_validation(self):
        with self.assertRaises(ValidationError):
            payment = Payment(
                status=Payment.Status.PENDING,
                type=Payment.Type.PAYMENT,
                borrowing=self.borrowing,
                session_url="https://example.com/session",
                session_id="test_session_id",
                money_to_pay=Decimal("0.00"),
            )
            payment.full_clean()

    def test_payment_related_name(self):
        payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://example.com/session",
            session_id="test_session_id",
            money_to_pay=Decimal("14.00"),
        )
        self.assertIn(payment, self.borrowing.payments.all())
