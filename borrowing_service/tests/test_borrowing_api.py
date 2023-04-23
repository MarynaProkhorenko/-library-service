from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from borrowing_service.models import Borrowing

BORROWINGS_URL = reverse("borrowing_service:borrowings-list")
BORROWINGS_RETURN_URL = reverse(
    "borrowing_service:borrowings-return-book", args=[1]
)


def sample_book(**params):
    """create sample books for testing by this params"""
    defaults = {
        "title": "Harry Potter",
        "author": "Joahn Rowling",
        "cover": "Hard",
        "inventory": 22,
        "daily_fee": 13.00,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(user, book, **params):
    """create sample borrowing for testing by this params"""
    defaults = {
        "borrow_date": "2023-01-03",
        "expected_return_date": "2023-01-08",
        "actual_return_date": "2023-01-08",
        "book": book,
        "user": user,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class NotAuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_borrowing_without_auth(self):
        """should be status code 401 if doesn't authenticate"""
        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="vania@test.com",
            password="wsx2wsx2",
            first_name="Vania",
            last_name="Anotov",
        )
        self.client.force_authenticate(self.user)

    def test_list_user_borrowings(self):
        user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="test12345",
            first_name="Kirrilll",
            last_name="testings",
        )
        self.client.force_authenticate(user)

        book1 = sample_book(title="Harry Potter")
        book2 = sample_book(title="Treasure island")

        sample_borrowing(user=user, book=book1)
        sample_borrowing(user=user, book=book2)

        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrowings_with_book(self):
        payload = {
            "borrow_date": "2023-01-03",
            "expected_return_date": "2023-01-08",
            "actual_return_date": "2023-01-08",
            "book": sample_book(),
            "user": self.user.id,
        }
        response = self.client.post(BORROWINGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_inventory_after_borrowing(self):
        book = sample_book(inventory=2)
        payload = {
            "borrow_date": "2023-01-03",
            "expected_return_date": "2023-01-08",
            "actual_return_date": "2023-01-08",
            "book": book.id,
            "user": self.user.id,
        }
        response = self.client.post(BORROWINGS_URL, payload)
        book_after_borrowing = Book.objects.get(id=book.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book_after_borrowing.inventory, 1)

    def test_borrowings_book_inventory_after_returning(self):
        book = sample_book(inventory=7)
        sample_borrowing(self.user, book, actual_return_date=None)
        payload = {
            "actual_return_date": "2023-04-06",
        }
        response = self.client.post(BORROWINGS_RETURN_URL, payload)
        book_after_returning = Book.objects.get(id=book.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book_after_returning.inventory, 8)


class AdminBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin.user@mail.com",
            password="1qazcde3",
            first_name="Bob",
            last_name="Smith",
        )
        self.client.force_authenticate(self.user)

    def test_list_status_code_borrowing_books_by_admin_staff(self):
        user = get_user_model().objects.create_user(
            email="test@count.com",
            password="wsx2wsx2",
            first_name="Nikita",
            last_name="Vorzen",
        )

        book1 = sample_book(title="Harry Potter")
        book2 = sample_book(title="Stalker")

        sample_borrowing(user=user, book=book1)
        sample_borrowing(user=user, book=book2)

        response = self.client.get(BORROWINGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
