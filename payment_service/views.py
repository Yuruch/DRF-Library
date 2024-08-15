import stripe
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    search_fields = ("borrowing__book__title",)
    ordering_fields = ("type", "money_to_pay")

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(borrowing_id__in=user.borrowings)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(borrowing_id__in=user.borrowings)


@api_view(["GET"])
def payment_success(request):
    session_id = request.GET.get("session_id")

    if session_id:
        try:
            payment = Payment.objects.get(session_id=session_id)
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment.status = Payment.Status.PAID
                payment.save()

                return Response(
                    {"message": "Payment successful", "payment_id": payment.id}
                )

            return Response(
                {"error": "Payment was not successful"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    return Response(
        {"error": "Session ID not provided"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
def payment_cancel(request):
    return Response(
        {"message": "Payment was canceled. You still have to pay within 24h"},
        status=status.HTTP_202_ACCEPTED,
    )
