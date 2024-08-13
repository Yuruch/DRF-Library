from rest_framework import serializers

from borrowings_service.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "expected_return_date",
            "book",
        )

    def validate(self, attrs):
        if attrs["book"].inventory <= 0:
            raise serializers.ValidationError("The selected book is not available.")
        return attrs


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)

    def validate_actual_return_date(self, value):
        if value and value < self.instance.borrow_date:
            raise serializers.ValidationError("Return date cannot be before borrow date.")
        return value
