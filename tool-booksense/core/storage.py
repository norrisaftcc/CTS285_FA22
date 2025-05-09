"""
Storage implementations for the BookSense application.

This module provides various backends for storing and retrieving book data.
"""

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Union

from .models import Book


class StorageInterface(ABC):
    """Abstract base class for storage implementations."""

    @abstractmethod
    def load(self) -> List[Book]:
        """Load books from storage."""
        pass

    @abstractmethod
    def save(self, books: List[Book]) -> bool:
        """Save books to storage."""
        pass

    @abstractmethod
    def get_book(self, book_id: str) -> Optional[Book]:
        """Get a specific book by ID."""
        pass

    @abstractmethod
    def add_book(self, book: Book) -> bool:
        """Add a new book to storage."""
        pass

    @abstractmethod
    def update_book(self, book: Book) -> bool:
        """Update an existing book."""
        pass

    @abstractmethod
    def delete_book(self, book_id: str) -> bool:
        """Delete a book by ID."""
        pass


class JsonStorage(StorageInterface):
    """JSON file-based storage implementation."""

    def __init__(self, file_path: str):
        """Initialize with the path to the JSON file.
        
        Args:
            file_path: Path to the JSON file for book storage
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the storage file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            # Create the directory if it doesn't exist
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Create an empty books list
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def load(self) -> List[Book]:
        """Load books from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                books_data = json.load(f)
                return [Book.from_dict(data) for data in books_data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading books: {e}")
            return []

    def save(self, books: List[Book]) -> bool:
        """Save books to the JSON file."""
        try:
            books_data = [book.to_dict() for book in books]
            
            # Use a temporary file to prevent data corruption
            temp_file = f"{self.file_path}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(books_data, f, indent=2)
            
            # Replace the original file with the temporary file
            os.replace(temp_file, self.file_path)
            return True
        except Exception as e:
            print(f"Error saving books: {e}")
            return False

    def get_book(self, book_id: str) -> Optional[Book]:
        """Get a specific book by ID."""
        books = self.load()
        for book in books:
            if book.id == book_id:
                return book
        return None

    def add_book(self, book: Book) -> bool:
        """Add a new book to storage."""
        books = self.load()
        
        # Check if a book with this ID already exists
        if any(b.id == book.id for b in books):
            return False
        
        books.append(book)
        return self.save(books)

    def update_book(self, book: Book) -> bool:
        """Update an existing book."""
        books = self.load()
        
        # Find the index of the book with matching ID
        for i, b in enumerate(books):
            if b.id == book.id:
                books[i] = book
                return self.save(books)
        
        return False  # Book not found

    def delete_book(self, book_id: str) -> bool:
        """Delete a book by ID."""
        books = self.load()
        initial_count = len(books)
        
        # Filter out the book with the specified ID
        books = [book for book in books if book.id != book_id]
        
        if len(books) < initial_count:
            return self.save(books)
        
        return False  # Book not found