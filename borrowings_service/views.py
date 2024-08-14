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


class BorrowingViewSet(viewsets.ModelViewSet):
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
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise ValidationError("The selected book is not available.")

        book.inventory -= 1
        book.save()

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.user != request.user:
            raise PermissionDenied("You are not allowed to return this book.")

        if borrowing.actual_return_date:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = datetime.now().date()
        serializer = self.get_serializer(borrowing, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        borrowing.book.inventory += 1
        borrowing.book.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
