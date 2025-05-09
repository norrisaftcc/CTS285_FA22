"""
Unit tests for the Open Library service.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from core.openlibrary_service import OpenLibraryService
from core.models import Book


class TestOpenLibraryService(unittest.TestCase):
    """Tests for the OpenLibraryService class."""

    def setUp(self):
        """Set up test environment."""
        # Sample book data from Open Library API
        self.sample_book_data = {
            "key": "/works/OL45883W",
            "title": "The Great Gatsby",
            "author_name": ["F. Scott Fitzgerald"],
            "first_publish_year": 1925,
            "isbn": ["9780743273565", "0743273567"],
            "publisher": ["Scribner"],
            "cover_edition_key": "OL24312921M",
            "language": ["eng"],
            "subject": ["Fiction", "Classic Literature", "Rich people"],
            "edition_count": 285
        }
        
        # Sample search results
        self.sample_search_results = {
            "numFound": 1,
            "docs": [self.sample_book_data]
        }
        
        # Sample book details
        self.sample_book_details = {
            "key": "/works/OL45883W",
            "title": "The Great Gatsby",
            "created": {
                "type": "/type/datetime",
                "value": "2009-10-28T06:25:33.382961"
            },
            "description": {
                "type": "/type/text",
                "value": "The Great Gatsby is a novel by American author F. Scott Fitzgerald."
            }
        }
        
        # Sample book editions
        self.sample_book_editions = {
            "entries": [
                {
                    "key": "/books/OL24312921M",
                    "title": "The Great Gatsby",
                    "publish_date": "2004"
                }
            ]
        }

    @patch('requests.get')
    def test_search_books(self, mock_get):
        """Test searching for books."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_search_results
        mock_get.return_value = mock_response
        
        # Call the method
        results = OpenLibraryService.search_books("The Great Gatsby", search_type="title", limit=10)
        
        # Check that the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("openlibrary.org/search.json", call_args)
        self.assertIn("title=The%20Great%20Gatsby", call_args)
        
        # Check the results
        self.assertEqual(results["total_found"], 1)
        self.assertEqual(len(results["books"]), 1)
        self.assertEqual(results["books"][0]["title"], "The Great Gatsby")

    @patch('requests.get')
    def test_get_book_details(self, mock_get):
        """Test getting book details."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_book_details
        mock_get.return_value = mock_response
        
        # Call the method
        details = OpenLibraryService.get_book_details("OL45883W")
        
        # Check that the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("openlibrary.org/works/OL45883W.json", call_args)
        
        # Check the details
        self.assertEqual(details["title"], "The Great Gatsby")
        self.assertIn("description", details)
        self.assertEqual(details["description"]["value"], 
                        "The Great Gatsby is a novel by American author F. Scott Fitzgerald.")

    @patch('requests.get')
    def test_get_book_editions(self, mock_get):
        """Test getting book editions."""
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_book_editions
        mock_get.return_value = mock_response
        
        # Call the method
        editions = OpenLibraryService.get_book_editions("OL45883W", limit=5)
        
        # Check that the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("openlibrary.org/works/OL45883W/editions.json", call_args)
        
        # Check the editions
        self.assertEqual(len(editions), 1)
        self.assertEqual(editions[0]["title"], "The Great Gatsby")
        self.assertEqual(editions[0]["publish_date"], "2004")

    def test_get_cover_url(self):
        """Test generating cover URLs."""
        # Test ISBN cover URL
        isbn_url = OpenLibraryService.get_cover_url("9780743273565", "isbn", "M")
        self.assertEqual(isbn_url, 
                         "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg")
        
        # Test OLID cover URL
        olid_url = OpenLibraryService.get_cover_url("OL24312921M", "olid", "L")
        self.assertEqual(olid_url, 
                         "https://covers.openlibrary.org/b/olid/OL24312921M-L.jpg")
        
        # Test invalid ID type
        with self.assertRaises(ValueError):
            OpenLibraryService.get_cover_url("9780743273565", "invalid", "M")
        
        # Test invalid size
        with self.assertRaises(ValueError):
            OpenLibraryService.get_cover_url("9780743273565", "isbn", "XL")

    def test_extract_book_info(self):
        """Test extracting book information."""
        # Call the method
        info = OpenLibraryService.extract_book_info(self.sample_book_data)
        
        # Check the extracted information
        self.assertEqual(info["title"], "The Great Gatsby")
        self.assertEqual(info["authors"], ["F. Scott Fitzgerald"])
        self.assertEqual(info["first_published"], 1925)
        self.assertEqual(info["isbn"], "9780743273565")
        self.assertEqual(info["open_library_work_id"], "OL45883W")
        self.assertEqual(info["open_library_url"], "https://openlibrary.org/works/OL45883W")
        self.assertIn("cover_url", info)
        self.assertIn("subjects", info)
        self.assertEqual(len(info["subjects"]), 3)

    def test_create_book_from_ol_data(self):
        """Test creating a Book object from Open Library data."""
        # Call the method
        book = OpenLibraryService.create_book_from_ol_data(self.sample_book_data)
        
        # Check the Book object
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "The Great Gatsby")
        self.assertEqual(book.author, "F. Scott Fitzgerald")
        self.assertEqual(book.year, 1925)
        self.assertEqual(book.isbn, "9780743273565")
        self.assertEqual(book.genre, ["Fiction", "Classic Literature", "Rich people"])
        self.assertEqual(book.read_status, "To Read")


if __name__ == "__main__":
    unittest.main()