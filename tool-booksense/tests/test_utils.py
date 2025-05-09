"""
Unit tests for the utility functions module.
"""

import unittest
import json
from datetime import datetime

from core.models import Book
from core.utils import (
    export_to_json,
    import_from_json,
    export_to_csv,
    import_from_csv,
    generate_sample_books
)


class TestUtils(unittest.TestCase):
    """Tests for the utility functions."""

    def setUp(self):
        """Set up test environment."""
        # Create some test books
        self.test_books = [
            Book(
                title="Test Book 1",
                author="Test Author 1",
                year=2021,
                isbn="1234567890",
                genre=["Fiction", "Adventure"],
                rating=4.0,
                description="A test book",
                read_status="Read",
                id="test-id-1",
                date_added=datetime(2023, 1, 1)
            ),
            Book(
                title="Test Book 2",
                author="Test Author 2",
                year=2022,
                genre=["Non-Fiction"],
                rating=3.5,
                read_status="Reading",
                id="test-id-2",
                date_added=datetime(2023, 2, 1)
            )
        ]

    def test_export_to_json(self):
        """Test exporting books to JSON."""
        # Export with pretty printing
        json_str = export_to_json(self.test_books, pretty=True)
        
        # Check that the JSON string contains book data
        self.assertIn("Test Book 1", json_str)
        self.assertIn("Test Author 1", json_str)
        self.assertIn("test-id-1", json_str)
        self.assertIn("Fiction", json_str)
        self.assertIn("Adventure", json_str)
        
        # Export without pretty printing
        json_str_compact = export_to_json(self.test_books, pretty=False)
        
        # Check that the compact JSON is shorter
        self.assertTrue(len(json_str_compact) < len(json_str))
        
        # Check that it still contains the data
        self.assertIn("Test Book 1", json_str_compact)
        self.assertIn("Test Author 1", json_str_compact)

    def test_import_from_json(self):
        """Test importing books from JSON."""
        # Export books to JSON
        json_str = export_to_json(self.test_books)
        
        # Import books from JSON
        imported_books = import_from_json(json_str)
        
        # Check that all books were imported
        self.assertEqual(len(imported_books), len(self.test_books))
        
        # Check book data
        for original_book in self.test_books:
            imported_book = next((b for b in imported_books if b.id == original_book.id), None)
            self.assertIsNotNone(imported_book)
            self.assertEqual(imported_book.title, original_book.title)
            self.assertEqual(imported_book.author, original_book.author)
            self.assertEqual(imported_book.year, original_book.year)
            self.assertEqual(imported_book.genre, original_book.genre)
            self.assertEqual(imported_book.rating, original_book.rating)
            self.assertEqual(imported_book.read_status, original_book.read_status)
        
        # Test import with invalid JSON
        invalid_json = "This is not valid JSON"
        imported_books = import_from_json(invalid_json)
        self.assertEqual(imported_books, [])

    def test_export_to_csv(self):
        """Test exporting books to CSV."""
        # Export books to CSV
        csv_str = export_to_csv(self.test_books)
        
        # Check that the CSV string contains headers and data
        csv_lines = csv_str.strip().split("\n")
        self.assertGreaterEqual(len(csv_lines), 3)  # Header + 2 books
        
        # Check headers
        headers = csv_lines[0].split(",")
        self.assertIn("title", headers)
        self.assertIn("author", headers)
        self.assertIn("year", headers)
        self.assertIn("genre", headers)
        self.assertIn("rating", headers)
        self.assertIn("read_status", headers)
        
        # Check data
        data_line = csv_lines[1]
        self.assertIn("Test Book 1", data_line)
        self.assertIn("Test Author 1", data_line)
        self.assertIn("Fiction,Adventure", data_line.replace('"', ''))
        
        # Test empty book list
        empty_csv = export_to_csv([])
        self.assertEqual(empty_csv, "")

    def test_import_from_csv(self):
        """Test importing books from CSV."""
        # Create a CSV string manually for more control
        csv_str = (
            "id,title,author,year,isbn,genre,rating,description,cover_url,read_status,date_added\n"
            "csv-id-1,CSV Book 1,CSV Author 1,2021,1111111111,\"Fiction,Adventure\",4.0,A CSV book,http://example.com/1.jpg,Read,2023-01-01T00:00:00\n"
            "csv-id-2,CSV Book 2,CSV Author 2,2022,,\"Non-Fiction\",3.5,,http://example.com/2.jpg,Reading,2023-02-01T00:00:00"
        )
        
        # Import books from CSV
        imported_books = import_from_csv(csv_str)
        
        # Check that all books were imported
        self.assertEqual(len(imported_books), 2)
        
        # Check book titles
        book_titles = [b.title for b in imported_books]
        self.assertIn("CSV Book 1", book_titles)
        self.assertIn("CSV Book 2", book_titles)
        
        # Find the imported books
        book1 = next((b for b in imported_books if b.title == "CSV Book 1"), None)
        book2 = next((b for b in imported_books if b.title == "CSV Book 2"), None)
        
        self.assertIsNotNone(book1)
        self.assertIsNotNone(book2)
        
        # Check data for book 1
        self.assertEqual(book1.id, "csv-id-1")
        self.assertEqual(book1.author, "CSV Author 1")
        self.assertEqual(book1.year, 2021)
        self.assertEqual(book1.isbn, "1111111111")
        self.assertEqual(set(book1.genre), set(["Fiction", "Adventure"]))
        self.assertEqual(book1.rating, 4.0)
        self.assertEqual(book1.read_status, "Read")
        
        # Check data for book 2
        self.assertEqual(book2.id, "csv-id-2")
        self.assertEqual(book2.author, "CSV Author 2")
        self.assertEqual(book2.year, 2022)
        self.assertEqual(set(book2.genre), set(["Non-Fiction"]))
        self.assertEqual(book2.rating, 3.5)
        self.assertEqual(book2.read_status, "Reading")
        
        # Test import with invalid CSV
        invalid_csv = "This is not valid CSV"
        imported_books = import_from_csv(invalid_csv)
        self.assertEqual(imported_books, [])
        
        # Test import with empty CSV
        empty_books = import_from_csv("")
        self.assertEqual(empty_books, [])

    def test_generate_sample_books(self):
        """Test generating sample books."""
        # Generate sample books
        sample_books = generate_sample_books()
        
        # Check that books were generated
        self.assertGreater(len(sample_books), 0)
        
        # Check that the books have the expected structure
        for book in sample_books:
            self.assertIsInstance(book, Book)
            self.assertTrue(book.title)
            self.assertTrue(book.author)
            self.assertIsInstance(book.year, int)
            self.assertIsInstance(book.genre, list)
            self.assertIsInstance(book.rating, float)
            self.assertTrue(book.description)
            self.assertIn(book.read_status, ["Read", "Reading", "To Read"])


if __name__ == "__main__":
    unittest.main()