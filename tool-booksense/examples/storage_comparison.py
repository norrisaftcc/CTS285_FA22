"""
Example script demonstrating the different storage implementations.

This script compares JSON and SQLite storage performance for various operations.
"""

import os
import sys
import time
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Book
from core.storage_factory import StorageFactory
from core.operations import BookCollection
from core.utils import generate_sample_books


def time_operation(operation_name, func, *args, **kwargs):
    """Time a function call and print the result."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"{operation_name}: {(end_time - start_time)*1000:.2f} ms")
    return result


def main():
    """Compare the performance of different storage implementations."""
    # Create storage files
    storage_dir = os.path.join(os.path.dirname(__file__), 'storage_test')
    os.makedirs(storage_dir, exist_ok=True)
    
    json_path = os.path.join(storage_dir, 'books.json')
    sqlite_path = os.path.join(storage_dir, 'books.db')
    
    # Get available storage types
    storage_types = StorageFactory.get_available_storage_types()
    print("Available storage types:")
    for storage_type, description in storage_types.items():
        print(f"- {storage_type}: {description}")
    print()
    
    # Create sample books (100 books)
    base_books = generate_sample_books()
    sample_books = []
    
    # Generate more books based on the samples
    for i in range(20):
        for book in base_books:
            new_book = Book(
                title=f"{book.title} - Edition {i+1}",
                author=book.author,
                year=book.year,
                isbn=book.isbn,
                genre=book.genre,
                rating=book.rating,
                description=book.description,
                cover_url=book.cover_url,
                read_status=book.read_status
            )
            sample_books.append(new_book)
    
    print(f"Generated {len(sample_books)} sample books")
    print()
    
    # Test storage implementations
    for storage_type in storage_types:
        print(f"=== Testing {storage_type.upper()} Storage ===")
        
        # Create storage and collection
        storage_path = json_path if storage_type == 'json' else sqlite_path
        storage = StorageFactory.create_storage(storage_type, storage_path)
        collection = BookCollection(storage)
        
        # Clear any existing books
        collection.storage.save([])
        
        # Test adding books
        print("Adding books:")
        time_operation("  Add all books", lambda: [collection.add_book(book) for book in sample_books])
        
        # Test loading books
        print("\nLoading books:")
        books = time_operation("  Load all books", collection.list_books)
        
        # Test filtering books
        print("\nFiltering books:")
        time_operation("  Filter by year range", collection.filter_books, year={'min': 1940, 'max': 1960})
        time_operation("  Filter by rating", collection.filter_books, rating={'min': 4.0})
        time_operation("  Filter by read status", collection.filter_books, read_status="Read")
        
        # Test searching books
        print("\nSearching books:")
        time_operation("  Search by title", collection.search_books, "Gatsby")
        time_operation("  Search by author", collection.search_books, "Orwell")
        
        # Test updating books
        print("\nUpdating books:")
        if books:
            book_to_update = books[0]
            book_to_update.rating = 5.0
            time_operation("  Update a book", collection.update_book, book_to_update)
        
        # Test deleting books
        print("\nDeleting books:")
        if books:
            book_to_delete = books[-1]
            time_operation("  Delete a book", collection.delete_book, book_to_delete.id)
        
        # Test statistics
        print("\nCalculating statistics:")
        time_operation("  Get statistics", collection.get_statistics)
        
        print("\n")
    
    print(f"Comparison completed. Storage files are in: {storage_dir}")


if __name__ == "__main__":
    main()