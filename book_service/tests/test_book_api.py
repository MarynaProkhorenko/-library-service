from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from book_service.models import Book
from rest_framework.test import APIClient

from book_service.serializers import BookSerializer

BOOK_LIST_URL = reverse("book_service:books-list")


def _book_url_with_id(*args) -> str:
    return reverse(
        "book_service:books-detail",
        args=args,
    )


def sample_book(**params):
    defaults = {
        "title": "Harry Potter",
        "author": "Joahn Rowling",
        "cover": "Hard",
        "inventory": 5,
        "daily_fee": 13.25,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class NotAuthenticatedBookAPITests(TestCase):
    """tests for Books API without authenticated"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_book_without_authenticated(self):
        """test API for list book with status code 200"""
        sample_book()
        sample_book()
        response = self.client.get(BOOK_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_without_authenticated(self):
        """test should response status code 401"""
        payload = {
            "title": "Treasure Island",
            "author": "Robert Louis Stevenson",
            "cover": "Soft",
            "inventory": 3,
            "daily_fee": 7.35,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookAPITests(TestCase):
    """tests for Book_service API with authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="qaz1qaz1",
            first_name="Alice",
            last_name="Wonder",
        )
        self.client.force_authenticate(self.user)

    def test_list_book_with_authenticated(self):
        sample_book()
        sample_book()
        response = self.client.get(BOOK_LIST_URL)

        movies = Book.objects.all().order_by("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_with_authenticated(self):
        """test should be status code 403 Forbidden"""
        payload = {
            "title": "title test",
            "author": "full name",
            "cover": "Hard",
            "inventory": 3,
            "daily_fee": 7.00,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserBookAPITests(TestCase):
    """tests for user who have is_staff: true (admin)"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="test@user.com",
            password="testqaz1",
            first_name="Aadam",
            last_name="White",
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "Harry Potter",
            "author": "Joahn Rowling",
            "cover": "Soft",
            "inventory": 2,
            "daily_fee": 2.00,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
