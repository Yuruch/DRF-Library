from rest_framework import serializers

from borrowings_service.serializers import BorrowingReadSerializer
from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = BorrowingReadSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )
