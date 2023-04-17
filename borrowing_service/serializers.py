from rest_framework import serializers

from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
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


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.StringRelatedField(many=False, read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user = serializers.CharField(source="user", read_only=True)
