from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from borrowing_service.notifications_bot import send_message


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


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(many=False, read_only=True)
    user = serializers.StringRelatedField(many=False, read_only=True)

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


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

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
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book")
            borrowing = Borrowing.objects.create(**validated_data)
            book.inventory -= 1
            book.save()
            message = (
                f"New borrowing created at {borrowing.borrow_date}\n"
                f"Book: {book.title}( {book.author})\n"
                f"Expected return date: {borrowing.expected_return_date}\n"
                f"User: {borrowing.user}"
            )
            send_message(message)

            return borrowing

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Borrowing.validated_date(
            attrs.get("borrow_date"),
            attrs.get("expected_return_date"),
            attrs.get("actual_return_date"),
            ValidationError,
        )
        return data

    def validate_book(self, book: Book):
        if book.inventory == 0:
            raise serializers.ValidationError("This book is not available now")
        return book


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
