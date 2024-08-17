import os

import stripe
from django.http import HttpRequest
from django.urls import reverse
from dotenv import load_dotenv

from borrowings_service.models import Borrowing
from payment_service.models import Payment


load_dotenv()
stripe.api_key = os.getenv("STRIPE_TEST_API_KEY")


def create_stripe_session(
    request: HttpRequest,
    name: str,
    borrowing: Borrowing = None,
    fine: int = None,
) -> Payment:
    if fine:
        total_price = fine
        payment_type = Payment.Type.FINE
    else:
        total_price = borrowing.calculate_total_price
        payment_type = Payment.Type.PAYMENT
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": name,
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("payment_service:payment-success")
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("payment_service:payment-cancel")
        ),
    )
    payment = Payment.objects.create(
        status=Payment.Status.PENDING,
        type=payment_type,
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_price,
    )
    return payment
