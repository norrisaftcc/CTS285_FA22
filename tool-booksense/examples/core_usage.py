"""
Example script demonstrating the usage of the BookSense core module.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Book
from core.storage import JsonStorage
from core.operations import BookCollection
from core.utils import generate_sample_books, export_to_json


def main():
    """Demonstrate the core functionality of BookSense."""
    # Create a temporary storage file
    storage_file = os.path.join(os.path.dirname(__file__), 'books.json')
    
    # Initialize storage and collection
    storage = JsonStorage(storage_file)
    collection = BookCollection(storage)
    
    print(f"Storage initialized at: {storage_file}")
    
    # Add sample books
    print("\nAdding sample books...")
    sample_books = generate_sample_books()
    for book in sample_books:
        collection.add_book(book)
    
    # List all books
    books = collection.list_books()
    print(f"\nTotal books: {len(books)}")
    
    # Display book details
    print("\nBook details:")
    for book in books:
        print(f"- {book.title} by {book.author} ({book.year}) - Rating: {book.rating}")
    
    # Search for books
    search_term = "gatsby"
    print(f"\nSearching for '{search_term}':")
    search_results = collection.search_books(search_term)
    for book in search_results:
        print(f"- {book.title} by {book.author}")
    
    # Filter books
    print("\nFiltering books published after 1950:")
    filtered_books = collection.filter_books(year={'min': 1950})
    for book in filtered_books:
        print(f"- {book.title} ({book.year})")
    
    # Sort books
    print("\nSorting books by rating (highest first):")
    sorted_books = collection.sort_books('rating', reverse=True)
    for book in sorted_books:
        print(f"- {book.title} - Rating: {book.rating}")
    
    # Calculate statistics
    stats = collection.get_statistics()
    print("\nCollection statistics:")
    print(f"- Total books: {stats['total_books']}")
    print(f"- Read: {stats['read_books']}")
    print(f"- Reading: {stats['reading_books']}")
    print(f"- To Read: {stats['to_read_books']}")
    print(f"- Average rating: {stats['average_rating']:.2f}")
    
    # Export to JSON
    json_export = export_to_json(books)
    print("\nJSON export (first 300 characters):")
    print(json_export[:300] + "...")
    
    # Add a new book
    new_book = Book(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        year=1937,
        isbn="9780547928227",
        genre=["Fiction", "Fantasy", "Adventure"],
        rating=4.28,
        description="A great modern classic and the prelude to The Lord of the Rings.",
        cover_url="https://covers.openlibrary.org/b/id/12005383-L.jpg",
        read_status="Read"
    )
    collection.add_book(new_book)
    print(f"\nAdded new book: {new_book.title}")
    
    # Update a book
    if search_results:
        book_to_update = search_results[0]
        book_to_update.rating = 4.5
        collection.update_book(book_to_update)
        print(f"\nUpdated book rating: {book_to_update.title} - New rating: {book_to_update.rating}")
    
    # Final book count
    final_books = collection.list_books()
    print(f"\nFinal book count: {len(final_books)}")
    
    print(f"\nExample completed. You can examine the book data at: {storage_file}")


if __name__ == "__main__":
    main()