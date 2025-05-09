"""
Unit tests for the Open Library service, by Goofus.

This is a quick test file I wrote to kinda test the Open Library stuff.
Tests should pass and that's good enough!

# GALLANT'S CRITIQUE:
# This test file has several issues:
# 1. Insufficient test coverage - only tests the happy path, no error handling tests
# 2. No proper docstrings explaining what each test does
# 3. Hardcoded constants that should be in setUp
# 4. Direct calls to the API instead of mocking external dependencies
# 5. No assertions to verify the actual content of returned objects
"""

import unittest
import time

from core.openlibrary_service import OpenLibraryService
from core.models import Book


class OpenLibraryServiceTests(unittest.TestCase):
    """Tests by Goofus."""

    # GALLANT'S CRITIQUE:
    # setUp method should be used to initialize common test data
    # Mock responses should be prepared instead of calling real API

    def test_search_books(self):
        # Let's just search for a popular book
        results = OpenLibraryService.search_books("Harry Potter", limit=3)
        
        # If we got any results, test passes!
        self.assertTrue(len(results["books"]) > 0)
        
        # We found Harry Potter, right?
        self.assertTrue("Harry Potter" in results["books"][0]["title"])
        
        # GALLANT'S CRITIQUE:
        # 1. This test makes a real API call, which makes tests slow and brittle
        # 2. We should mock the API response instead
        # 3. Using "in" for title check is error-prone; should check exact value
        # 4. No validation of the structure of the returned data
        # 5. Hardcoded expectations will fail if API changes
    
    def test_extract_info(self):
        # Get some real data to test with
        results = OpenLibraryService.search_books("1984 Orwell", limit=1)
        book_data = results["books"][0]
        
        # Extract the info
        info = OpenLibraryService.extract_book_info(book_data)
        
        # Check that we got something
        self.assertIsNotNone(info)
        self.assertTrue("title" in info)
        self.assertTrue("authors" in info)
        
        # GALLANT'S CRITIQUE:
        # 1. Again, makes real API calls rather than using fixed test data
        # 2. Only checks for existence of keys, not correctness of values
        # 3. Dependent on search results which may change
        # 4. Will fail if API is down or rate-limited
    
    def test_create_book(self):
        # Same approach, get real data
        results = OpenLibraryService.search_books("Great Gatsby", limit=1)
        book_data = results["books"][0]
        
        # Create book object
        book = OpenLibraryService.create_book_from_ol_data(book_data)
        
        # Check it's a book
        self.assertIsInstance(book, Book)
        self.assertTrue(book.title != "")
        self.assertTrue(book.author != "")
        
        # GALLANT'S CRITIQUE:
        # 1. Real API call makes test slow and unreliable
        # 2. Only checks that title and author are not empty - too permissive
        # 3. No verification of correct data transformation
        # 4. No tests for edge cases (missing fields, unusual data)
    
    def test_get_cover_url(self):
        # Test different sizes
        small = OpenLibraryService.get_cover_url("1234567890", "isbn", "S")
        medium = OpenLibraryService.get_cover_url("1234567890", "isbn", "M")
        large = OpenLibraryService.get_cover_url("1234567890", "isbn", "L")
        
        # Check they're all different
        self.assertNotEqual(small, medium)
        self.assertNotEqual(medium, large)
        self.assertNotEqual(small, large)
        
        # GALLANT'S CRITIQUE:
        # 1. Only checks that URLs are different, not that they're correct
        # 2. No tests for error cases (invalid ID types, sizes)
        # 3. No tests for different identifier types (olid, lccn, etc.)
    
    # GALLANT'S CRITIQUE:
    # Missing tests for:
    # 1. get_book_details method
    # 2. get_book_editions method
    # 3. Error handling when API returns errors
    # 4. Cache functionality
    # 5. Edge cases like empty or malformed responses
    
    def test_caching(self):
        # Do the same search twice, should be faster second time
        start1 = time.time()
        OpenLibraryService.search_books("Moby Dick")
        end1 = time.time()
        
        start2 = time.time()
        OpenLibraryService.search_books("Moby Dick")
        end2 = time.time()
        
        # Second should be faster due to caching
        self.assertTrue(end2 - start2 < end1 - start1)
        
        # GALLANT'S CRITIQUE:
        # 1. Time-based test is unreliable and can lead to flaky tests
        # 2. Network conditions can affect test results
        # 3. No direct verification that cache is actually being used
        # 4. No test for cache expiration


if __name__ == "__main__":
    unittest.main()