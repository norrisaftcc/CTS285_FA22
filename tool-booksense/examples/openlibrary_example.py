"""
Example script demonstrating the usage of the Open Library service.

This script shows how to search for books, get book details, and retrieve covers.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.openlibrary_service import OpenLibraryService
from core.models import Book
from core.storage import JsonStorage
from core.operations import BookCollection


def main():
    """Demonstrate the Open Library integration with BookSense."""
    print("BookSense Open Library Integration Example")
    print("------------------------------------------")
    
    # Create a storage for our books
    storage_file = os.path.join(os.path.dirname(__file__), 'ol_example_books.json')
    storage = JsonStorage(storage_file)
    collection = BookCollection(storage)
    
    # Search for books by title
    search_title = "The Great Gatsby"
    print(f"\nSearching for books with title: '{search_title}'...")
    
    search_results = OpenLibraryService.search_books(search_title, search_type="title", limit=5)
    
    print(f"Found {search_results['total_found']} books. Showing first {len(search_results['books'])} results:")
    
    # Display search results and add books to collection
    for i, book_data in enumerate(search_results['books'], 1):
        info = OpenLibraryService.extract_book_info(book_data)
        
        print(f"\n--- Book {i} ---")
        print(f"Title: {info['title']}")
        print(f"Author(s): {', '.join(info['authors'])}")
        print(f"First Published: {info['first_published']}")
        print(f"ISBN: {info['isbn']}")
        
        if info['subjects']:
            print(f"Subjects: {', '.join(info['subjects'])}")
        
        print(f"Open Library URL: {info['open_library_url']}")
        
        if info['cover_url']:
            print(f"Cover image: {info['cover_url']}")
        
        # Create a Book object and add it to our collection
        book = OpenLibraryService.create_book_from_ol_data(book_data)
        collection.add_book(book)
        print(f"Added to collection with ID: {book.id}")
    
    # Search by ISBN
    print("\n\nSearching by ISBN...")
    isbn_search = "9780743273565"  # ISBN for The Great Gatsby
    isbn_results = OpenLibraryService.search_books(isbn_search, search_type="isbn", limit=1)
    
    if isbn_results['books']:
        book_data = isbn_results['books'][0]
        info = OpenLibraryService.extract_book_info(book_data)
        print(f"Found book: {info['title']} by {', '.join(info['authors'])}")
        
        # Get book details
        if info['open_library_work_id']:
            print(f"\nGetting detailed information...")
            details = OpenLibraryService.get_book_details(info['open_library_work_id'])
            
            # Print some details
            if 'description' in details:
                description = details['description']
                if isinstance(description, dict) and 'value' in description:
                    description = description['value']
                print(f"\nDescription: {description[:200]}...")
            
            # Get editions
            print(f"\nGetting editions information...")
            editions = OpenLibraryService.get_book_editions(info['open_library_work_id'], limit=3)
            print(f"Found {len(editions)} editions (limited to 3):")
            
            for i, edition in enumerate(editions, 1):
                print(f"  Edition {i}: {edition.get('title')} ({edition.get('publish_date', 'Unknown date')})")
    
    # List all books in our collection
    books = collection.list_books()
    print(f"\n\nBooks in collection: {len(books)}")
    
    # Save the collection to a JSON file
    print(f"Book collection saved to: {storage_file}")


if __name__ == "__main__":
    main()