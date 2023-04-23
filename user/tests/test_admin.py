from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    """tests for admin site"""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="wsx2wsx2",
            first_name="Valentin",
            last_name="Testings",
        )
        self.client.force_login(self.user)

    def test_admin_site_email(self):
        """test should check email in changelist"""
        url = reverse("admin:user_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.email)

    def test_admin_detail_email(self):
        """test should check email in detail page"""
        url = reverse("admin:user_user_change", args=[1])
        response = self.client.get(url)

        self.assertContains(response, self.user.email)

    def test_admin_create_email(self):
        """test should check email in addition page"""
        url = reverse("admin:user_user_add")
        response = self.client.get(url)

        self.assertContains(response, "email")
