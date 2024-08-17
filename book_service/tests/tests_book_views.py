from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book


class BookViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book1 = Book.objects.create(
            title="Python Cookbook",
            author="David Beazley & Brian K. Jones",
            cover=Book.Cover.SOFT,
            inventory=10,
            daily_fee=1.50,
        )
        self.book2 = Book.objects.create(
            title="Learning Python",
            author="Mark Lutz",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=2.00,
        )
        self.book3 = Book.objects.create(
            title="Effective Python",
            author="Brett Slatkin",
            cover=Book.Cover.SOFT,
            inventory=8,
            daily_fee=1.75,
        )

    def test_list_books(self):
        url = reverse("book_service:book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filter_books_by_title(self):
        url = reverse("book_service:book-list")
        response = self.client.get(url, {"title": "Python Cookbook"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", [])
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["title"], "Python Cookbook")

    def test_filter_books_by_author(self):
        url = reverse("book_service:book-list")
        response = self.client.get(
            url, {"author": "David Beazley & Brian K. Jones"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", [])
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["author"], "David Beazley & Brian K. Jones")

    def test_filter_books_by_cover(self):
        url = reverse("book_service:book-list")
        response = self.client.get(url, {"cover": "SOFT"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_book(self):
        url = reverse("book_service:book-detail", args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)
