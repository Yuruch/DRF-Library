import stripe
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics

from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(borrowing__user=user)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(borrowing__user=user)


def payment_success(request):
    session_id = request.GET.get("session_id")

    if session_id:
        try:
            payment = Payment.objects.get(session_id=session_id)

            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment.status = Payment.Status.PAID
                payment.save()
                return render(
                    request, "payment/success.html", {"payment": payment}
                )
            else:
                return HttpResponse("Payment was not successful", status=400)
        except Payment.DoesNotExist:
            return HttpResponse("Payment not found", status=404)

    return HttpResponse("Session ID not provided", status=400)


def payment_cancel(request):
    return render(request, "payment/cancel.html")
