import os
import stripe
from django.urls import reverse_lazy
from payment_service.models import Payment

stripe.api_key = os.getenv("STRIPE_TEST_API_KEY")


def create_stripe_session(borrowing, request):
    total_price = borrowing.calculate_total_price
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Library Book Borrowing",
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse_lazy("payment_service:payment-success")
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse_lazy("payment_service:payment-cancel")
        ),
    )

    payment = Payment.objects.create(
        status=Payment.Status.PENDING,
        type=Payment.Type.PAYMENT,
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_price,
    )
    return payment
