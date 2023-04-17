from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book_service.models import Book
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


class BorrowingCreateSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book")
            borrowing = Borrowing.objects.create(**validated_data)
            book.inventory -= 1
            book.save()

            return borrowing

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Borrowing.validated_date(
            attrs["borrow_date"],
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            ValidationError
        )
        return data

    def validate_book(self, book: Book):
        if book.inventory == 0:
            raise serializers.ValidationError("This book is not available now")
        return book


