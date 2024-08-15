from datetime import timedelta, date
from unittest.mock import patch, MagicMock

from django.test import TestCase, RequestFactory
from django.urls import reverse

from book_service.models import Book
from borrowings_service.models import Borrowing
from payment_service.models import Payment
from payment_service.services.create_payment import create_stripe_session
from user.models import User


class CreateStripeSessionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get(
            reverse("payment_service:payment-list")
        )
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=10,
            daily_fee=5.0,
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=7),
        )

    @patch("stripe.checkout.Session.create")
    def test_create_stripe_session_for_borrowing(self, mock_stripe_create):
        mock_session = MagicMock()
        mock_session.id = "test_session_id"
        mock_session.url = "https://checkout.stripe.com/test-session-url"
        mock_stripe_create.return_value = mock_session

        payment = create_stripe_session(
            request=self.request,
            name="Library Book Borrowing",
            borrowing=self.borrowing,
        )

        mock_stripe_create.assert_called_once()
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertEqual(payment.type, Payment.Type.PAYMENT)
        self.assertEqual(payment.borrowing, self.borrowing)
        self.assertEqual(
            payment.session_url, "https://checkout.stripe.com/test-session-url"
        )
        self.assertEqual(payment.session_id, "test_session_id")
        self.assertEqual(
            payment.money_to_pay, self.borrowing.calculate_total_price
        )

    @patch("stripe.checkout.Session.create")
    def test_create_stripe_session_for_fine(self, mock_stripe_create):
        mock_session = MagicMock()
        mock_session.id = "test_fine_session_id"
        mock_session.url = "https://checkout.stripe.com/test-fine-session-url"
        mock_stripe_create.return_value = mock_session

        fine_amount = 500

        payment = create_stripe_session(
            borrowing=self.borrowing,
            request=self.request,
            name="Library Fine Payment",
            fine=fine_amount,
        )

        mock_stripe_create.assert_called_once()
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertEqual(payment.type, Payment.Type.FINE)
        self.assertEqual(
            payment.session_url,
            "https://checkout.stripe.com/test-fine-session-url",
        )
        self.assertEqual(payment.session_id, "test_fine_session_id")
        self.assertEqual(payment.money_to_pay, fine_amount)
