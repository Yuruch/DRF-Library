import stripe
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    search_fields = ("borrowing__book__title",)
    ordering_fields = ("type", "money_to_pay")
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(
                borrowing__in=user.borrowing_set.all()
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search term for filtering payments by book title",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering",
                description="Comma-separated list of fields to order by",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: PaymentSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized"),
        },
        description="List all payments, with optional filtering and ordering.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(
                borrowing__in=user.borrowing_set.all()
            )

    @extend_schema(
        responses={
            200: PaymentSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Payment not found"),
        },
        description="Retrieve details of a specific payment.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="session_id",
            description="Stripe session ID to check payment status",
            required=True,
            type=str,
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Payment was successful",
            examples={
                "application/json": {
                    "message": "Payment successful",
                    "payment_id": "uuid",
                }
            },
        ),
        400: OpenApiResponse(
            description="Bad request, payment was not successful or session ID not provided",
        ),
        404: OpenApiResponse(
            description="Payment not found",
        ),
    },
    description="Handle Stripe payment success callback and update payment status.",
)
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


@extend_schema(
    responses={
        202: OpenApiResponse(
            description="Payment was canceled, user must pay within 24 hours",
            examples={
                "application/json": {
                    "message": "Payment was canceled. You still have to pay within 24h"
                }
            },
        ),
    },
    description="Handle payment cancellation.",
)
@api_view(["GET"])
def payment_cancel(request):
    return Response(
        {"message": "Payment was canceled. You still have to pay within 24h"},
        status=status.HTTP_202_ACCEPTED,
    )
