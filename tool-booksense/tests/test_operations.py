"""
Unit tests for the book operations module.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from core.models import Book
from core.operations import BookCollection


class MockStorage:
    """Mock storage for testing operations."""
    
    def __init__(self):
        self.books = []
    
    def load(self):
        return self.books
    
    def save(self, books):
        self.books = books
        return True
    
    def get_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def add_book(self, book):
        if any(b.id == book.id for b in self.books):
            return False
        self.books.append(book)
        return True
    
    def update_book(self, book):
        for i, b in enumerate(self.books):
            if b.id == book.id:
                self.books[i] = book
                return True
        return False
    
    def delete_book(self, book_id):
        initial_count = len(self.books)
        self.books = [b for b in self.books if b.id != book_id]
        return len(self.books) < initial_count


class TestBookCollection(unittest.TestCase):
    """Tests for the BookCollection class."""

    def setUp(self):
        """Set up test environment."""
        self.storage = MockStorage()
        self.collection = BookCollection(self.storage)
        
        # Create some test books
        self.test_books = [
            Book(
                title="Test Book 1",
                author="Test Author 1",
                year=2021,
                genre=["Fiction"],
                rating=4.0,
                read_status="Read"
            ),
            Book(
                title="Test Book 2",
                author="Test Author 2",
                year=2022,
                genre=["Non-Fiction"],
                rating=3.5,
                read_status="Reading"
            ),
            Book(
                title="Another Book",
                author="Another Author",
                year=2020,
                genre=["Fiction", "Sci-Fi"],
                rating=4.5,
                read_status="Read"
            ),
            Book(
                title="Fantasy Book",
                author="Fantasy Author",
                year=2023,
                genre=["Fiction", "Fantasy"],
                rating=5.0,
                read_status="To Read"
            )
        ]
        
        # Add books to storage
        for book in self.test_books:
            self.storage.add_book(book)

    def test_list_books(self):
        """Test listing all books."""
        books = self.collection.list_books()
        
        self.assertEqual(len(books), len(self.test_books))
        self.assertEqual(set(b.id for b in books), set(b.id for b in self.test_books))

    def test_get_book(self):
        """Test getting a book by ID."""
        book_id = self.test_books[0].id
        book = self.collection.get_book(book_id)
        
        self.assertIsNotNone(book)
        self.assertEqual(book.id, book_id)
        self.assertEqual(book.title, self.test_books[0].title)
        
        # Test getting a non-existent book
        self.assertIsNone(self.collection.get_book("non-existent-id"))

    def test_add_book(self):
        """Test adding a book."""
        new_book = Book(
            title="New Book",
            author="New Author",
            year=2024
        )
        
        success = self.collection.add_book(new_book)
        self.assertTrue(success)
        
        # Check that the book was added
        added_book = self.collection.get_book(new_book.id)
        self.assertIsNotNone(added_book)
        self.assertEqual(added_book.title, "New Book")

    def test_update_book(self):
        """Test updating a book."""
        book_to_update = self.test_books[0]
        book_to_update.title = "Updated Title"
        book_to_update.rating = 4.8
        
        success = self.collection.update_book(book_to_update)
        self.assertTrue(success)
        
        # Check that the book was updated
        updated_book = self.collection.get_book(book_to_update.id)
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.rating, 4.8)
        
        # Test updating a non-existent book
        non_existent_book = Book(
            title="Non-existent Book",
            author="Author",
            year=2020,
            id="non-existent-id"
        )
        
        success = self.collection.update_book(non_existent_book)
        self.assertFalse(success)

    def test_delete_book(self):
        """Test deleting a book."""
        book_id = self.test_books[1].id
        initial_count = len(self.collection.list_books())
        
        success = self.collection.delete_book(book_id)
        self.assertTrue(success)
        
        # Check that the book was deleted
        self.assertIsNone(self.collection.get_book(book_id))
        self.assertEqual(len(self.collection.list_books()), initial_count - 1)
        
        # Test deleting a non-existent book
        success = self.collection.delete_book("non-existent-id")
        self.assertFalse(success)
        self.assertEqual(len(self.collection.list_books()), initial_count - 1)

    def test_search_books(self):
        """Test searching for books."""
        # Search by title
        results = self.collection.search_books("Another")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Another Book")
        
        # Search by author
        results = self.collection.search_books("Fantasy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Fantasy Author")
        
        # Search by description (add a description first)
        self.test_books[0].description = "This is a test description with a unique word xylophone"
        self.collection.update_book(self.test_books[0])
        
        results = self.collection.search_books("xylophone")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, self.test_books[0].id)
        
        # Search with no matches
        results = self.collection.search_books("nonexistent")
        self.assertEqual(len(results), 0)
        
        # Search with empty query
        results = self.collection.search_books("")
        self.assertEqual(len(results), len(self.test_books))

    def test_filter_books(self):
        """Test filtering books by various attributes."""
        # Filter by year
        results = self.collection.filter_books(year=2022)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2022)
        
        # Filter by year range
        results = self.collection.filter_books(year={'min': 2022})
        self.assertEqual(len(results), 2)
        self.assertTrue(all(b.year >= 2022 for b in results))
        
        results = self.collection.filter_books(year={'max': 2021})
        self.assertEqual(len(results), 2)
        self.assertTrue(all(b.year <= 2021 for b in results))
        
        results = self.collection.filter_books(year={'min': 2021, 'max': 2022})
        self.assertEqual(len(results), 2)
        self.assertTrue(all(2021 <= b.year <= 2022 for b in results))
        
        # Filter by rating
        results = self.collection.filter_books(rating=4.5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].rating, 4.5)
        
        # Filter by rating range
        results = self.collection.filter_books(rating={'min': 4.0})
        self.assertEqual(len(results), 3)
        self.assertTrue(all(b.rating >= 4.0 for b in results))
        
        # Filter by genre (single value)
        results = self.collection.filter_books(genre="Sci-Fi")
        self.assertEqual(len(results), 1)
        self.assertTrue(all("Sci-Fi" in b.genre for b in results))
        
        # Filter by genre (multiple values)
        results = self.collection.filter_books(genre=["Fiction"])
        self.assertEqual(len(results), 3)
        self.assertTrue(all("Fiction" in b.genre for b in results))
        
        # Filter by read status
        results = self.collection.filter_books(read_status="Read")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(b.read_status == "Read" for b in results))
        
        # Filter by multiple criteria
        results = self.collection.filter_books(
            genre="Fiction",
            read_status="Read"
        )
        self.assertEqual(len(results), 2)
        self.assertTrue(all(
            "Fiction" in b.genre and b.read_status == "Read" 
            for b in results
        ))
        
        # Filter with no matches
        results = self.collection.filter_books(year=1900)
        self.assertEqual(len(results), 0)
        
        # Filter with invalid attribute
        results = self.collection.filter_books(invalid_attribute="value")
        self.assertEqual(len(results), len(self.test_books))

    def test_sort_books(self):
        """Test sorting books by various attributes."""
        # Sort by title (ascending)
        results = self.collection.sort_books("title")
        self.assertEqual(len(results), len(self.test_books))
        self.assertEqual(results[0].title, "Another Book")
        self.assertEqual(results[-1].title, "Test Book 2")
        
        # Sort by title (descending)
        results = self.collection.sort_books("title", reverse=True)
        self.assertEqual(results[0].title, "Test Book 2")
        self.assertEqual(results[-1].title, "Another Book")
        
        # Sort by year (ascending)
        results = self.collection.sort_books("year")
        self.assertEqual(results[0].year, 2020)
        self.assertEqual(results[-1].year, 2023)
        
        # Sort by rating (descending)
        results = self.collection.sort_books("rating", reverse=True)
        self.assertEqual(results[0].rating, 5.0)
        self.assertEqual(results[-1].rating, 3.5)
        
        # Sort by invalid attribute
        results = self.collection.sort_books("invalid_attribute")
        self.assertEqual(len(results), len(self.test_books))

    def test_get_statistics(self):
        """Test calculating statistics."""
        stats = self.collection.get_statistics()
        
        # Check basic counts
        self.assertEqual(stats["total_books"], 4)
        self.assertEqual(stats["read_books"], 2)
        self.assertEqual(stats["reading_books"], 1)
        self.assertEqual(stats["to_read_books"], 1)
        
        # Check average rating
        expected_avg = sum(b.rating for b in self.test_books) / len(self.test_books)
        self.assertEqual(stats["average_rating"], expected_avg)
        
        # Check genre counts
        self.assertEqual(stats["genres"]["Fiction"], 3)
        self.assertEqual(stats["genres"]["Non-Fiction"], 1)
        self.assertEqual(stats["genres"]["Sci-Fi"], 1)
        self.assertEqual(stats["genres"]["Fantasy"], 1)
        
        # Check year counts
        self.assertEqual(stats["books_by_year"][2020], 1)
        self.assertEqual(stats["books_by_year"][2021], 1)
        self.assertEqual(stats["books_by_year"][2022], 1)
        self.assertEqual(stats["books_by_year"][2023], 1)
        
        # Check author counts
        self.assertEqual(stats["books_by_author"]["Test Author 1"], 1)
        self.assertEqual(stats["books_by_author"]["Test Author 2"], 1)
        self.assertEqual(stats["books_by_author"]["Another Author"], 1)
        self.assertEqual(stats["books_by_author"]["Fantasy Author"], 1)


if __name__ == "__main__":
    unittest.main()