"""
Unit tests for the SQLite storage implementation.
"""

import os
import unittest
import tempfile
import sqlite3
from datetime import datetime

from core.models import Book
try:
    from core.storage_sqlite import SqliteStorage
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False


@unittest.skipIf(not HAS_SQLITE, "SQLite storage not available")
class TestSqliteStorage(unittest.TestCase):
    """Tests for the SqliteStorage class."""

    def setUp(self):
        """Set up test environment."""
        # Skip if SQLite storage is not available
        if not HAS_SQLITE:
            self.skipTest("SQLite storage not available")
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_books.db")
        self.storage = SqliteStorage(self.db_path)
        
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
                title="Test Book 3",
                author="Test Author 3",
                year=2023,
                genre=["Fiction", "Fantasy"],
                rating=5.0,
                read_status="To Read"
            )
        ]

    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()

    def test_database_creation(self):
        """Test database is created if it doesn't exist."""
        # The database should have been created in setUp
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check that it has the expected tables
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertIn("books", tables)
            self.assertIn("genres", tables)
            self.assertIn("book_genres", tables)

    def test_save_and_load(self):
        """Test saving and loading books."""
        # Save books
        success = self.storage.save(self.test_books)
        self.assertTrue(success)
        
        # Load books
        loaded_books = self.storage.load()
        
        # Check that we have the same number of books
        self.assertEqual(len(loaded_books), len(self.test_books))
        
        # Check that the books have the same IDs
        loaded_ids = [book.id for book in loaded_books]
        original_ids = [book.id for book in self.test_books]
        self.assertEqual(set(loaded_ids), set(original_ids))
        
        # Check book content
        for original_book in self.test_books:
            loaded_book = next((b for b in loaded_books if b.id == original_book.id), None)
            self.assertIsNotNone(loaded_book)
            self.assertEqual(loaded_book.title, original_book.title)
            self.assertEqual(loaded_book.author, original_book.author)
            self.assertEqual(loaded_book.year, original_book.year)
            self.assertEqual(set(loaded_book.genre), set(original_book.genre))
            self.assertEqual(loaded_book.rating, original_book.rating)
            self.assertEqual(loaded_book.read_status, original_book.read_status)

    def test_get_book(self):
        """Test getting a book by ID."""
        # Save books
        self.storage.save(self.test_books)
        
        # Get a book that exists
        book_id = self.test_books[1].id
        book = self.storage.get_book(book_id)
        
        self.assertIsNotNone(book)
        self.assertEqual(book.id, book_id)
        self.assertEqual(book.title, self.test_books[1].title)
        
        # Get a book that doesn't exist
        non_existent_book = self.storage.get_book("non-existent-id")
        self.assertIsNone(non_existent_book)

    def test_add_book(self):
        """Test adding a book."""
        # Save initial books
        self.storage.save(self.test_books)
        
        # Add a new book
        new_book = Book(
            title="New Book",
            author="New Author",
            year=2024,
            genre=["Sci-Fi"],
            rating=4.2,
            read_status="To Read"
        )
        
        success = self.storage.add_book(new_book)
        self.assertTrue(success)
        
        # Load books and check the new one is there
        loaded_books = self.storage.load()
        self.assertEqual(len(loaded_books), len(self.test_books) + 1)
        
        loaded_book = next((b for b in loaded_books if b.id == new_book.id), None)
        self.assertIsNotNone(loaded_book)
        self.assertEqual(loaded_book.title, "New Book")
        self.assertEqual(loaded_book.genre, ["Sci-Fi"])

    def test_add_duplicate_book(self):
        """Test adding a book with an existing ID fails."""
        # Save initial books
        self.storage.save(self.test_books)
        
        # Try to add a book with an existing ID
        duplicate_book = Book(
            title="Duplicate Book",
            author="Duplicate Author",
            year=2025,
            id=self.test_books[0].id  # Use an existing ID
        )
        
        success = self.storage.add_book(duplicate_book)
        self.assertFalse(success)
        
        # Check that the number of books hasn't changed
        loaded_books = self.storage.load()
        self.assertEqual(len(loaded_books), len(self.test_books))

    def test_update_book(self):
        """Test updating a book."""
        # Save initial books
        self.storage.save(self.test_books)
        
        # Update a book
        book_to_update = self.test_books[0]
        book_to_update.title = "Updated Title"
        book_to_update.rating = 4.8
        book_to_update.genre = ["Fiction", "Mystery"]  # Change genres
        
        success = self.storage.update_book(book_to_update)
        self.assertTrue(success)
        
        # Load the updated book
        updated_book = self.storage.get_book(book_to_update.id)
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.rating, 4.8)
        self.assertEqual(set(updated_book.genre), set(["Fiction", "Mystery"]))
        
        # Try to update a non-existent book
        non_existent_book = Book(
            title="Non-existent Book",
            author="Author",
            year=2020,
            id="non-existent-id"
        )
        
        success = self.storage.update_book(non_existent_book)
        self.assertFalse(success)

    def test_delete_book(self):
        """Test deleting a book."""
        # Save initial books
        self.storage.save(self.test_books)
        initial_count = len(self.test_books)
        
        # Delete a book
        book_id = self.test_books[1].id
        success = self.storage.delete_book(book_id)
        self.assertTrue(success)
        
        # Check that the book was deleted
        loaded_books = self.storage.load()
        self.assertEqual(len(loaded_books), initial_count - 1)
        self.assertIsNone(self.storage.get_book(book_id))
        
        # Try to delete a non-existent book
        success = self.storage.delete_book("non-existent-id")
        self.assertFalse(success)
        
        # Check that the count didn't change
        loaded_books = self.storage.load()
        self.assertEqual(len(loaded_books), initial_count - 1)

    def test_genre_handling(self):
        """Test handling of book genres."""
        # Create a book with multiple genres
        book = Book(
            title="Genre Test Book",
            author="Genre Author",
            year=2023,
            genre=["Fiction", "Thriller", "Mystery"]
        )
        
        # Save and load the book
        self.storage.add_book(book)
        loaded_book = self.storage.get_book(book.id)
        
        # Check that all genres were saved and loaded correctly
        self.assertEqual(set(loaded_book.genre), set(["Fiction", "Thriller", "Mystery"]))
        
        # Update the book with different genres
        book.genre = ["Non-Fiction", "Biography"]
        self.storage.update_book(book)
        
        # Check that genres were updated correctly
        updated_book = self.storage.get_book(book.id)
        self.assertEqual(set(updated_book.genre), set(["Non-Fiction", "Biography"]))
        
        # Check that the old genres are no longer associated with the book
        self.assertNotIn("Fiction", updated_book.genre)
        self.assertNotIn("Thriller", updated_book.genre)


if __name__ == "__main__":
    unittest.main()