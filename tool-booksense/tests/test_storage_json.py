"""
Unit tests for the JSON storage implementation.
"""

import os
import json
import unittest
import tempfile
from datetime import datetime

from core.models import Book
from core.storage import JsonStorage


class TestJsonStorage(unittest.TestCase):
    """Tests for the JsonStorage class."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = os.path.join(self.temp_dir.name, "test_books.json")
        self.storage = JsonStorage(self.storage_path)
        
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

    def test_file_creation(self):
        """Test storage file is created if it doesn't exist."""
        # The file should have been created in setUp
        self.assertTrue(os.path.exists(self.storage_path))
        
        # Check that it's a valid JSON file with an empty array
        with open(self.storage_path, "r") as f:
            data = json.load(f)
            self.assertEqual(data, [])

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
            self.assertEqual(loaded_book.genre, original_book.genre)
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
        
        success = self.storage.update_book(book_to_update)
        self.assertTrue(success)
        
        # Load the updated book
        updated_book = self.storage.get_book(book_to_update.id)
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.rating, 4.8)
        
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

    def test_error_handling(self):
        """Test error handling for corrupted files."""
        # Write invalid JSON to the file
        with open(self.storage_path, "w") as f:
            f.write("This is not valid JSON")
        
        # Try to load books
        loaded_books = self.storage.load()
        self.assertEqual(loaded_books, [])


if __name__ == "__main__":
    unittest.main()