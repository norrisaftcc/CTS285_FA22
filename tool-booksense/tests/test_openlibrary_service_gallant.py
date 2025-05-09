"""
Unit tests for the Open Library service, by Gallant.

This module provides comprehensive tests for the OpenLibraryService class,
following best practices for unit testing:
1. Proper test isolation using mocks for external dependencies
2. Complete test coverage including edge cases and error conditions
3. Clear test organization with proper setup and teardown
4. Descriptive assertions that clarify expected outcomes
5. Comprehensive docstrings explaining the purpose of each test

# GOOFUS'S COMMENT:
# This seems like overkill! My tests were much faster to write and they work fine.
# All these mocks and setup methods just make things complicated.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

from core.openlibrary_service import OpenLibraryService
from core.models import Book


class TestOpenLibraryService(unittest.TestCase):
    """Tests for the OpenLibraryService class with proper isolation and coverage."""

    def setUp(self):
        """
        Set up test fixtures and sample data for all tests.
        
        Creates sample API responses that mimic the Open Library API format
        to ensure tests are consistent and don't rely on the actual API.
        
        # GOOFUS'S COMMENT:
        # Using real API data would be more realistic. This is just extra work.
        """
        # Clear the service cache before each test
        OpenLibraryService._cache = {}
        OpenLibraryService._cache_expiry = {}
        
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
            "start": 0,
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
                },
                {
                    "key": "/books/OL7182651M",
                    "title": "The Great Gatsby",
                    "publish_date": "1995"
                }
            ]
        }
        
        # Sample error response
        self.sample_error_response = {
            "error": "Not found"
        }
        
        # Sample empty response
        self.sample_empty_search = {
            "numFound": 0,
            "start": 0,
            "docs": []
        }

    @patch('requests.get')
    def test_search_books_success(self, mock_get):
        """
        Test successful book search with mocked API response.
        
        Verifies that the search method correctly:
        1. Formats the URL with proper encoding
        2. Passes correct parameters and headers
        3. Processes the API response into the expected format
        4. Returns the correct number of results
        
        # GOOFUS'S COMMENT:
        # Wait, we're not even calling the real API? How do we know it works then?
        """
        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_search_results
        mock_get.return_value = mock_response
        
        # Call the method
        results = OpenLibraryService.search_books("The Great Gatsby", search_type="title", limit=10)
        
        # Verify the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("openlibrary.org/search.json", call_args)
        self.assertIn("title=The%20Great%20Gatsby", call_args)
        self.assertIn("limit=10", call_args)
        
        # Verify the results are parsed correctly
        self.assertEqual(results["total_found"], 1)
        self.assertEqual(len(results["books"]), 1)
        self.assertEqual(results["books"][0]["title"], "The Great Gatsby")
        self.assertEqual(results["books"][0]["author_name"], ["F. Scott Fitzgerald"])
        self.assertEqual(results["books"][0]["first_publish_year"], 1925)

    @patch('requests.get')
    def test_search_books_empty_results(self, mock_get):
        """
        Test search with no matching results.
        
        Verifies handling of empty search results:
        1. Formats the response correctly with zero results
        2. Returns empty list instead of None
        
        # GOOFUS'S COMMENT:
        # Empty results? That will never happen in a real app.
        """
        # Configure the mock to return empty results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_empty_search
        mock_get.return_value = mock_response
        
        # Call the method
        results = OpenLibraryService.search_books("NonexistentBookTitle", search_type="title")
        
        # Verify we get a properly structured empty result
        self.assertEqual(results["total_found"], 0)
        self.assertEqual(results["books"], [])

    @patch('requests.get')
    def test_search_books_http_error(self, mock_get):
        """
        Test search with HTTP error response.
        
        Verifies error handling for failed requests:
        1. Returns a properly formatted empty result on error
        2. Doesn't crash when the API returns an error
        
        # GOOFUS'S COMMENT:
        # Error testing? The API always works for me.
        """
        # Configure the mock to raise an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        # Call the method
        results = OpenLibraryService.search_books("The Great Gatsby", search_type="title")
        
        # Verify we get an empty result without exception
        self.assertEqual(results["total_found"], 0)
        self.assertEqual(results["books"], [])

    @patch('requests.get')
    def test_get_book_details_success(self, mock_get):
        """
        Test successful retrieval of book details.
        
        Verifies that the book details method:
        1. Constructs the correct API URL with the work ID
        2. Processes the response correctly
        3. Returns complete book details
        
        # GOOFUS'S COMMENT:
        # These assertions are so verbose. Just check if it's not None!
        """
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_book_details
        mock_get.return_value = mock_response
        
        # Call the method
        details = OpenLibraryService.get_book_details("OL45883W")
        
        # Verify correct URL construction
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertEqual(call_args, "https://openlibrary.org/works/OL45883W.json")
        
        # Verify the details are returned correctly
        self.assertEqual(details["title"], "The Great Gatsby")
        self.assertIn("description", details)
        self.assertEqual(details["description"]["value"], 
                         "The Great Gatsby is a novel by American author F. Scott Fitzgerald.")

    @patch('requests.get')
    def test_get_book_editions_success(self, mock_get):
        """
        Test successful retrieval of book editions.
        
        Verifies that the editions method:
        1. Constructs the correct API URL
        2. Passes the limit parameter correctly
        3. Returns properly structured edition data
        
        # GOOFUS'S COMMENT:
        # Do we really need to test every little parameter detail?
        """
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_book_editions
        mock_get.return_value = mock_response
        
        # Call the method with a specific limit
        editions = OpenLibraryService.get_book_editions("OL45883W", limit=5)
        
        # Verify correct URL and parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertEqual(call_args, "https://openlibrary.org/works/OL45883W/editions.json")
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs.get('params', {}).get('limit'), 5)
        
        # Verify correct parsing of editions
        self.assertEqual(len(editions), 2)
        self.assertEqual(editions[0]["title"], "The Great Gatsby")
        self.assertEqual(editions[0]["publish_date"], "2004")
        self.assertEqual(editions[1]["publish_date"], "1995")

    def test_get_cover_url(self):
        """
        Test generation of cover image URLs.
        
        Verifies:
        1. Correct URL construction for various ID types
        2. Proper handling of different image sizes
        3. Validation of input parameters
        
        # GOOFUS'S COMMENT:
        # Testing all these combinations seems excessive.
        """
        # Test for ISBN identifier
        isbn_url = OpenLibraryService.get_cover_url("9780743273565", "isbn", "M")
        self.assertEqual(isbn_url, 
                         "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg")
        
        # Test for OLID identifier
        olid_url = OpenLibraryService.get_cover_url("OL24312921M", "olid", "L")
        self.assertEqual(olid_url, 
                         "https://covers.openlibrary.org/b/olid/OL24312921M-L.jpg")
        
        # Test for OCLC identifier
        oclc_url = OpenLibraryService.get_cover_url("123456", "oclc", "S")
        self.assertEqual(oclc_url, 
                         "https://covers.openlibrary.org/b/oclc/123456-S.jpg")
        
        # Test for invalid ID type
        with self.assertRaises(ValueError) as context:
            OpenLibraryService.get_cover_url("9780743273565", "invalid", "M")
        self.assertIn("Invalid id_type", str(context.exception))
        
        # Test for invalid size
        with self.assertRaises(ValueError) as context:
            OpenLibraryService.get_cover_url("9780743273565", "isbn", "XL")
        self.assertIn("Invalid size", str(context.exception))

    def test_extract_book_info(self):
        """
        Test extraction of book information from API response.
        
        Verifies:
        1. All expected fields are extracted correctly
        2. Appropriate defaults are provided for missing fields
        3. URLs are properly constructed
        
        # GOOFUS'S COMMENT:
        # Just check if it returns something! All these assertions are overkill.
        """
        # Extract info from sample data
        info = OpenLibraryService.extract_book_info(self.sample_book_data)
        
        # Verify all expected fields
        self.assertEqual(info["title"], "The Great Gatsby")
        self.assertEqual(info["authors"], ["F. Scott Fitzgerald"])
        self.assertEqual(info["first_published"], 1925)
        self.assertEqual(info["isbn"], "9780743273565")
        self.assertEqual(info["open_library_work_id"], "OL45883W")
        self.assertEqual(info["open_library_url"], "https://openlibrary.org/works/OL45883W")
        self.assertEqual(info["editions_count"], 285)
        self.assertEqual(info["subjects"], ["Fiction", "Classic Literature", "Rich people"])
        self.assertEqual(info["cover_url"], 
                         "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg")
        
        # Test with minimal data
        minimal_data = {"title": "Minimal Book"}
        minimal_info = OpenLibraryService.extract_book_info(minimal_data)
        
        self.assertEqual(minimal_info["title"], "Minimal Book")
        self.assertEqual(minimal_info["authors"], ["Unknown"])
        self.assertEqual(minimal_info["first_published"], "Unknown")
        self.assertIsNone(minimal_info["isbn"])
        self.assertIsNone(minimal_info["cover_url"])
        self.assertEqual(minimal_info["subjects"], [])

    def test_create_book_from_ol_data(self):
        """
        Test creation of Book objects from Open Library data.
        
        Verifies:
        1. Correct mapping of API fields to Book attributes
        2. Proper handling of defaults for missing fields
        3. Type conversions (e.g., string to int for year)
        
        # GOOFUS'S COMMENT:
        # We have so many class methods! Can't we just make one big test?
        """
        # Test with complete data
        book = OpenLibraryService.create_book_from_ol_data(self.sample_book_data)
        
        self.assertIsInstance(book, Book)
        self.assertEqual(book.title, "The Great Gatsby")
        self.assertEqual(book.author, "F. Scott Fitzgerald")
        self.assertEqual(book.year, 1925)
        self.assertEqual(book.isbn, "9780743273565")
        self.assertEqual(set(book.genre), set(["Fiction", "Classic Literature", "Rich people"]))
        self.assertEqual(book.read_status, "To Read")
        self.assertEqual(book.cover_url, 
                         "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg")
        
        # Test with minimal data and invalid year
        minimal_data = {
            "title": "Minimal Book",
            "author_name": ["Test Author"],
            "first_publish_year": "Not a year"
        }
        
        book = OpenLibraryService.create_book_from_ol_data(minimal_data)
        
        self.assertEqual(book.title, "Minimal Book")
        self.assertEqual(book.author, "Test Author")
        # Should default to current year for invalid year
        self.assertGreaterEqual(book.year, datetime.now().year)
        self.assertEqual(book.genre, [])
        self.assertEqual(book.rating, 0.0)

    @patch('requests.get')
    def test_caching_mechanism(self, mock_get):
        """
        Test the caching mechanism for API requests.
        
        Verifies:
        1. Identical requests use the cache for subsequent calls
        2. The API is only called once for identical requests
        3. Cache correctly stores and retrieves results
        
        # GOOFUS'S COMMENT:
        # Caching is an implementation detail, do we really need to test it?
        """
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_search_results
        mock_get.return_value = mock_response
        
        # First call should hit the API
        results1 = OpenLibraryService.search_books("The Great Gatsby", search_type="title")
        
        # Second identical call should use the cache
        results2 = OpenLibraryService.search_books("The Great Gatsby", search_type="title")
        
        # Verify the API was only called once
        mock_get.assert_called_once()
        
        # Verify both results are identical
        self.assertEqual(results1, results2)
        
        # Verify cache contains the expected entry
        cache_key = f"https://openlibrary.org/search.json?title=The%20Great%20Gatsby&limit=10:None"
        self.assertIn(cache_key, OpenLibraryService._cache)


if __name__ == "__main__":
    unittest.main()