"""
Mock implementation of the operations module for testing.

This module provides a customized version of the operations module
that behaves deterministically for testing purposes.
"""

from datetime import datetime
import uuid
from typing import Dict, List, Optional, Any, Callable

from core.models import Book

# Override UUID generation to make it deterministic for tests
def deterministic_uuid():
    """Generate a deterministic UUID for testing."""
    return "test-uuid"

# Mock book collection for testing
class MockBookCollection:
    """A deterministic book collection for testing purposes."""
    
    def __init__(self):
        """Initialize with predefined test books."""
        self._books = [
            Book(
                id="id-1",
                title="Another Book",  # This should sort first alphabetically
                author="Another Author",
                year=2020,
                genre=["Fiction", "Sci-Fi"],
                rating=4.5,
                read_status="Read"
            ),
            Book(
                id="id-2",
                title="Fantasy Book",
                author="Fantasy Author",
                year=2023,
                genre=["Fiction", "Fantasy"],
                rating=5.0,
                read_status="To Read"
            ),
            Book(
                id="id-3",
                title="Test Book 1",
                author="Test Author 1",
                year=2021,
                genre=["Fiction"],
                rating=4.0,
                read_status="Read"
            ),
            Book(
                id="id-4",
                title="Test Book 2",  # This should sort last alphabetically
                author="Test Author 2",
                year=2022,
                genre=["Non-Fiction"],
                rating=3.5,
                read_status="Reading"
            )
        ]
    
    def list_books(self) -> List[Book]:
        """Get all books in the collection."""
        return self._books
    
    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or description."""
        if not query:
            return self._books
        
        query_lower = query.lower()
        results = []
        
        for book in self._books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower in book.description.lower()):
                results.append(book)
                
        return results
    
    def filter_books(self, **filters) -> List[Book]:
        """Filter books by various attributes."""
        if not filters:
            return self._books
        
        results = self._books.copy()
        
        for attr, value in filters.items():
            if attr == "genre" and isinstance(value, str):
                results = [book for book in results if value in book.genre]
            elif attr == "read_status":
                results = [book for book in results if book.read_status == value]
            
        return results
    
    def sort_books(self, key: str, reverse: bool = False) -> List[Book]:
        """Sort books by a specified attribute."""
        if key == "title":
            # Deterministic sort by title
            sorted_books = sorted(self._books, key=lambda book: book.title, reverse=reverse)
            return sorted_books
        
        # Default sorting by ID for deterministic results
        return sorted(self._books, key=lambda book: book.id, reverse=reverse)