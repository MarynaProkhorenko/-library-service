from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient


class NotAuthenticatedAPITests(TestCase):
    """test not authenticated user"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_manage_auth_required(self):
        response = self.client.get(reverse("user:manage"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):
        """test should create user"""
        payload = {
            "email": "valentin@test.com",
            "password": "wsx2wsx2",
            "first_name": "TestFirst",
            "last_name": "TestSecond",
        }
        response = self.client.post(reverse("user:create"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticatedAPITests(TestCase):
    """tests with authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="valentin@test.com",
            password="wsx2wsx2",
            first_name="TestFirst",
            last_name="TestSecond",
        )
        self.client.force_authenticate(self.user)

    def test_manage_auth_required(self):
        response = self.client.get(reverse("user:manage"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        """test should check status code 400 Bad request"""
        payload = {
            "email": "valentin@test.com",
            "password": "wsx2wsx2",
            "first_name": "TestFirst",
            "last_name": "TestSecond",
        }
        response = self.client.post(reverse("user:create"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
