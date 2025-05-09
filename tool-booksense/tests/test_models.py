"""
Unit tests for the models module.
"""

import unittest
from datetime import datetime
from uuid import uuid4

from core.models import Book


class TestBookModel(unittest.TestCase):
    """Tests for the Book class."""

    def test_create_book_with_required_fields(self):
        """Test creating a Book with only required fields."""
        book = Book(
            title="Test Book",
            author="Test Author",
            year=2023
        )
        
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.isbn, None)
        self.assertEqual(book.genre, [])
        self.assertEqual(book.rating, 0.0)
        self.assertEqual(book.description, "")
        self.assertEqual(book.cover_url, None)
        self.assertEqual(book.read_status, "To Read")
        self.assertIsNotNone(book.id)
        self.assertIsInstance(book.date_added, datetime)

    def test_create_book_with_all_fields(self):
        """Test creating a Book with all fields."""
        book_id = str(uuid4())
        date_added = datetime(2023, 1, 1)
        
        book = Book(
            title="Complete Book",
            author="Complete Author",
            year=2023,
            isbn="1234567890",
            genre=["Fiction", "Sci-Fi"],
            rating=4.5,
            description="A test book",
            cover_url="http://example.com/cover.jpg",
            read_status="Read",
            id=book_id,
            date_added=date_added
        )
        
        self.assertEqual(book.title, "Complete Book")
        self.assertEqual(book.author, "Complete Author")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(book.genre, ["Fiction", "Sci-Fi"])
        self.assertEqual(book.rating, 4.5)
        self.assertEqual(book.description, "A test book")
        self.assertEqual(book.cover_url, "http://example.com/cover.jpg")
        self.assertEqual(book.read_status, "Read")
        self.assertEqual(book.id, book_id)
        self.assertEqual(book.date_added, date_added)

    def test_validation_empty_title(self):
        """Test validation rejects empty title."""
        with self.assertRaises(ValueError):
            Book(title="", author="Author", year=2023)

    def test_validation_empty_author(self):
        """Test validation rejects empty author."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="", year=2023)

    def test_validation_invalid_year_string(self):
        """Test validation rejects non-integer year."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year="invalid")

    def test_validation_year_conversion(self):
        """Test validation converts string year to int."""
        book = Book(title="Title", author="Author", year="2023")
        self.assertEqual(book.year, 2023)
        self.assertIsInstance(book.year, int)

    def test_validation_year_too_early(self):
        """Test validation rejects year before 1000."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year=999)

    def test_validation_year_too_future(self):
        """Test validation rejects year too far in future."""
        future_year = datetime.now().year + 10
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year=future_year)

    def test_validation_rating_too_low(self):
        """Test validation rejects rating below 0."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year=2023, rating=-1)

    def test_validation_rating_too_high(self):
        """Test validation rejects rating above 5."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year=2023, rating=6)

    def test_validation_invalid_read_status(self):
        """Test validation rejects invalid read status."""
        with self.assertRaises(ValueError):
            Book(title="Title", author="Author", year=2023, read_status="Invalid")

    def test_to_dict(self):
        """Test conversion to dictionary."""
        book_id = "test-id"
        date_added = datetime(2023, 1, 1)
        
        book = Book(
            title="Dict Book",
            author="Dict Author",
            year=2023,
            isbn="1234567890",
            genre=["Fiction"],
            rating=4.0,
            description="A test book for dict conversion",
            cover_url="http://example.com/cover.jpg",
            read_status="Reading",
            id=book_id,
            date_added=date_added
        )
        
        book_dict = book.to_dict()
        
        self.assertEqual(book_dict["title"], "Dict Book")
        self.assertEqual(book_dict["author"], "Dict Author")
        self.assertEqual(book_dict["year"], 2023)
        self.assertEqual(book_dict["isbn"], "1234567890")
        self.assertEqual(book_dict["genre"], ["Fiction"])
        self.assertEqual(book_dict["rating"], 4.0)
        self.assertEqual(book_dict["description"], "A test book for dict conversion")
        self.assertEqual(book_dict["cover_url"], "http://example.com/cover.jpg")
        self.assertEqual(book_dict["read_status"], "Reading")
        self.assertEqual(book_dict["id"], book_id)
        self.assertEqual(book_dict["date_added"], date_added.isoformat())

    def test_from_dict(self):
        """Test creation from dictionary."""
        book_dict = {
            "title": "FromDict Book",
            "author": "FromDict Author",
            "year": 2023,
            "isbn": "0987654321",
            "genre": ["Non-Fiction", "History"],
            "rating": 3.5,
            "description": "A test book from dict",
            "cover_url": "http://example.com/other-cover.jpg",
            "read_status": "To Read",
            "id": "from-dict-id",
            "date_added": "2023-02-01T12:00:00"
        }
        
        book = Book.from_dict(book_dict)
        
        self.assertEqual(book.title, "FromDict Book")
        self.assertEqual(book.author, "FromDict Author")
        self.assertEqual(book.year, 2023)
        self.assertEqual(book.isbn, "0987654321")
        self.assertEqual(book.genre, ["Non-Fiction", "History"])
        self.assertEqual(book.rating, 3.5)
        self.assertEqual(book.description, "A test book from dict")
        self.assertEqual(book.cover_url, "http://example.com/other-cover.jpg")
        self.assertEqual(book.read_status, "To Read")
        self.assertEqual(book.id, "from-dict-id")
        self.assertEqual(book.date_added, datetime.fromisoformat("2023-02-01T12:00:00"))

    def test_from_dict_invalid_date(self):
        """Test creation from dictionary with invalid date."""
        book_dict = {
            "title": "Invalid Date Book",
            "author": "Author",
            "year": 2023,
            "date_added": "invalid-date"
        }
        
        book = Book.from_dict(book_dict)
        
        self.assertEqual(book.title, "Invalid Date Book")
        self.assertIsInstance(book.date_added, datetime)


if __name__ == "__main__":
    unittest.main()