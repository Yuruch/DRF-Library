from datetime import datetime

from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    BorrowingReadSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)
from payment_service.models import Payment
from payment_service.services.create_payment import create_stripe_session


class BorrowingViewSet(viewsets.ModelViewSet):
    """Manage borrowings for users."""

    FINE_MULTIPLIER = 2
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        elif self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingReadSerializer

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def perform_create(self, serializer):
        """Create a borrowing record."""
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise ValidationError("The selected book is not available.")

        if self.request.user.borrowing_set.filter(
            payments__status=Payment.Status.PENDING
        ).exists():
            raise PermissionDenied("You have to pay for all the borrowings!")

        book.inventory -= 1
        book.save()

        borrowing = serializer.save(user=self.request.user)
        payment = create_stripe_session(
            borrowing=borrowing,
            request=self.request,
            name="Library Book Borrowing",
        )

        self.custom_response = Response(
            {
                "detail": "You have to pay for using the book",
                "session_url": payment.session_url,
            },
            status=status.HTTP_201_CREATED,
        )

    def create(self, request, *args, **kwargs):
        """Override create method to include custom response if needed."""
        response = super().create(request, *args, **kwargs)
        if hasattr(self, "custom_response"):
            return self.custom_response
        return response

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        """Handle the return of a borrowed book and calculate any applicable fine."""
        borrowing = self.get_object()
        expected_date = borrowing.expected_return_date

        if borrowing.user != request.user:
            raise PermissionDenied("You are not allowed to return this book.")

        if borrowing.actual_return_date and borrowing.payments.filter(
            type=Payment.Type.FINE, status=Payment.Status.PAID
        ):
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif (
            borrowing.actual_return_date
            and borrowing.user.payments.filter(
                status=Payment.Status.PENDING
            ).exists()
        ):
            return Response(
                {
                    "detail": "You have returned book but you "
                    "should pay all the pending payments!",
                    "session_url": borrowing.payments.get(
                        type=Payment.Type.FINE
                    ).session_url,
                },
                status=status.HTTP_200_OK,
            )

        borrowing.actual_return_date = datetime.now().date()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        borrowing.book.inventory += 1
        borrowing.book.save()
        actual_date = borrowing.actual_return_date

        if actual_date > expected_date:
            fine = (
                (actual_date - actual_date).days
                * borrowing.book.daily_fee
                * self.FINE_MULTIPLIER
            )
            payment = create_stripe_session(
                fine=fine,
                request=self.request,
                name="Library Book Borrowing",
                borrowing=borrowing,
            )
            return Response(
                {
                    "detail": "You have not return book in time so please pay the fine",
                    "session_url": payment.session_url,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
