from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    """tests to check user model"""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email="user@test.com",
            password="wsx2wsx2",
            first_name="Valentin",
            last_name="Cuker",
        )
        self.client.force_login(self.user)

    def test_user_str(self):
        """test should retrieve representation str method in models"""
        self.assertEqual(
            str(self.user), f"{self.user.first_name} {self.user.last_name}"
        )

    def test_superuser_create(self):
        """test should check creating  admin user by models"""
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_user_create(self):
        """test should check crating sample user by models"""
        user = get_user_model().objects.create_user(
            email="valera@test.com",
            password="wsx2wsx2",
        )

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_user_fields_forms(self):
        """should test equal to forms in user models"""
        expected_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        ]
        models_fields = [field.name for field in get_user_model()._meta.fields]

        for field in expected_fields:
            self.assertIn(field, models_fields)
