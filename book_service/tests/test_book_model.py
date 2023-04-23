from django.test import TestCase

from book_service.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Lady with dragon tatoo",
            author="David Fincher",
            cover="Hard",
            inventory=9,
            daily_fee=18.00,
        )

    def test_user_str(self):
        """test should check representation method in models, book_service"""
        self.assertEqual(str(self.book), f"{self.book.title} {self.book.author}")
