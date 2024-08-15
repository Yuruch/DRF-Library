from django.test import TestCase

from book_service.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="At the Mountains of Madness",
            author="Howard Phillips Lovecraft",
            cover=Book.Cover.HARD,
            inventory=6,
            daily_fee=6.00,
        )

    def test_book_str(self):
        """Test the string representation of the Book model"""
        self.assertEqual(str(self.book), self.book.title)

    def test_book_fields_quantity(self):
        """Test that the Book model has the correct fields"""
        expected_fields = [
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "image",
        ]
        model_fields = [field.name for field in Book._meta.fields]

        for field in expected_fields:
            self.assertIn(field, model_fields)

        self.assertEqual(len(model_fields), len(expected_fields))

    def test_book_cover_choices(self):
        """Test that the cover choices work correctly"""
        book = Book.objects.create(
            title="The Call of Cthulhu",
            author="Howard Phillips Lovecraft",
            cover=Book.Cover.SOFT,
            inventory=10,
            daily_fee=5.00,
        )
        self.assertEqual(book.cover, Book.Cover.SOFT)

        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            book.cover = "PAPERBACK"
            book.full_clean()
