from decimal import Decimal
from unittest.mock import patch, Mock

import stripe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from payment_service.models import Payment
from borrowings_service.models import Borrowing
from book_service.models import Book
from django.contrib.auth import get_user_model
from datetime import date, timedelta


class PaymentServiceTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.staff_user = get_user_model().objects.create_superuser(
            email="staffuser@example.com", password="staffpassword"
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
        self.payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://example.com/session",
            session_id="test_session_id",
            money_to_pay=Decimal("14.00"),
        )

    def test_payment_list_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("payment_service:payment-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.payment.id)

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_payment_detail_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("payment_service:payment-detail", args=[self.payment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_success_view(self, mock_retrieve):
        mock_session = Mock()
        mock_session.payment_status = "paid"
        mock_retrieve.return_value = mock_session

        Payment.objects.filter(session_id="test_session_id").delete()

        self.payment = Payment.objects.create(
            session_id="test_session_id",
            status=Payment.Status.PENDING,
            money_to_pay=Decimal("14.00"),
            borrowing=self.borrowing,
        )

        url = reverse("payment_service:payment-success")
        response = self.client.get(url, {"session_id": "test_session_id"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.Status.PAID)
        self.assertEqual(response.data["payment_id"], self.payment.id)

    def test_payment_success_view_invalid_session_id(self):
        url = reverse("payment_service:payment-success")
        response = self.client.get(url, {"session_id": "invalid_session_id"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_payment_success_view_missing_session_id(self):
        url = reverse("payment_service:payment-success")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_payment_cancel_view(self):
        url = reverse("payment_service:payment-cancel")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("message", response.data)
        self.assertEqual(
            response.data["message"],
            "Payment was canceled. You still have to pay within 24h",
        )
