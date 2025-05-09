"""
Book collection operations for the BookSense application.

This module provides high-level operations for managing book collections.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import re

from .models import Book
from .storage import StorageInterface


class BookCollection:
    """Manages a collection of books with various operations."""

    def __init__(self, storage: StorageInterface):
        """Initialize with a storage implementation.
        
        Args:
            storage: A storage implementation for persisting books
        """
        self.storage = storage
        self._books = self.storage.load()
    
    def add_book(self, book: Book) -> bool:
        """Add a new book to the collection.
        
        Args:
            book: The book to add
            
        Returns:
            bool: True if the book was added successfully, False otherwise
        """
        result = self.storage.add_book(book)
        if result:
            self._books = self.storage.load()
        return result
    
    def get_book(self, book_id: str) -> Optional[Book]:
        """Get a book by its ID.
        
        Args:
            book_id: The unique identifier of the book
            
        Returns:
            Optional[Book]: The book if found, None otherwise
        """
        return self.storage.get_book(book_id)
    
    def update_book(self, book: Book) -> bool:
        """Update an existing book in the collection.
        
        Args:
            book: The updated book data (must have the same ID as an existing book)
            
        Returns:
            bool: True if the book was updated successfully, False otherwise
        """
        result = self.storage.update_book(book)
        if result:
            self._books = self.storage.load()
        return result
    
    def delete_book(self, book_id: str) -> bool:
        """Remove a book from the collection.
        
        Args:
            book_id: The unique identifier of the book to delete
            
        Returns:
            bool: True if the book was deleted successfully, False otherwise
        """
        result = self.storage.delete_book(book_id)
        if result:
            self._books = self.storage.load()
        return result
    
    def list_books(self) -> List[Book]:
        """Get all books in the collection.
        
        Returns:
            List[Book]: All books in the collection
        """
        self._books = self.storage.load()  # Refresh the cache
        return self._books
    
    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or description.
        
        Args:
            query: The search query
            
        Returns:
            List[Book]: Books matching the search criteria
        """
        self._books = self.storage.load()  # Refresh the cache
        
        if not query:
            return self._books
        
        query_lower = query.lower()
        results = []
        
        for book in self._books:
            # Check if the query appears in title, author, or description
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower in book.description.lower()):
                results.append(book)
                
        return results
    
    def filter_books(self, **filters) -> List[Book]:
        """Filter books by various attributes.
        
        Args:
            **filters: Attribute-value pairs to filter by
            
        Returns:
            List[Book]: Books matching the filter criteria
        """
        self._books = self.storage.load()  # Refresh the cache
        
        if not filters:
            return self._books
        
        results = self._books
        
        for attr, value in filters.items():
            if attr not in vars(Book):
                continue
            
            if attr == 'year':
                if isinstance(value, dict):
                    min_year = value.get('min')
                    max_year = value.get('max')
                    
                    if min_year is not None:
                        results = [book for book in results if book.year >= min_year]
                    if max_year is not None:
                        results = [book for book in results if book.year <= max_year]
                else:
                    results = [book for book in results if book.year == value]
            
            elif attr == 'rating':
                if isinstance(value, dict):
                    min_rating = value.get('min')
                    max_rating = value.get('max')
                    
                    if min_rating is not None:
                        results = [book for book in results if book.rating >= min_rating]
                    if max_rating is not None:
                        results = [book for book in results if book.rating <= max_rating]
                else:
                    results = [book for book in results if book.rating == value]
            
            elif attr == 'genre':
                if isinstance(value, list):
                    results = [book for book in results if set(value).issubset(set(book.genre))]
                else:
                    results = [book for book in results if value in book.genre]
            
            else:
                results = [book for book in results if getattr(book, attr, None) == value]
        
        return results
    
    def sort_books(self, key: str, reverse: bool = False) -> List[Book]:
        """Sort books by a specified attribute.
        
        Args:
            key: The attribute to sort by
            reverse: Whether to sort in descending order
            
        Returns:
            List[Book]: Sorted books
        """
        self._books = self.storage.load()  # Refresh the cache
        
        if not hasattr(Book, key):
            return self._books
        
        return sorted(self._books, key=lambda book: getattr(book, key), reverse=reverse)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics about the book collection.
        
        Returns:
            Dict[str, Any]: Various statistics about the collection
        """
        self._books = self.storage.load()  # Refresh the cache
        
        stats = {
            'total_books': len(self._books),
            'read_books': len([b for b in self._books if b.read_status == "Read"]),
            'reading_books': len([b for b in self._books if b.read_status == "Reading"]),
            'to_read_books': len([b for b in self._books if b.read_status == "To Read"]),
            'average_rating': 0,
            'genres': {},
            'books_by_year': {},
            'books_by_author': {}
        }
        
        # Calculate average rating
        if stats['total_books'] > 0:
            stats['average_rating'] = sum(b.rating for b in self._books) / stats['total_books']
        
        # Count books by genre
        for book in self._books:
            for genre in book.genre:
                stats['genres'][genre] = stats['genres'].get(genre, 0) + 1
        
        # Count books by year
        for book in self._books:
            stats['books_by_year'][book.year] = stats['books_by_year'].get(book.year, 0) + 1
        
        # Count books by author
        for book in self._books:
            stats['books_by_author'][book.author] = stats['books_by_author'].get(book.author, 0) + 1
        
        return stats