"""
Utility functions for the BookSense application.

This module provides helper functions used across the application.
"""

import csv
import json
from datetime import datetime
from io import StringIO
from typing import Dict, List, Optional, Union

from .models import Book


def export_to_json(books: List[Book], pretty: bool = True) -> str:
    """Export books to a JSON string.
    
    Args:
        books: List of books to export
        pretty: Whether to format the JSON with indentation
        
    Returns:
        str: JSON representation of the books
    """
    books_data = [book.to_dict() for book in books]
    indent = 2 if pretty else None
    return json.dumps(books_data, indent=indent)


def import_from_json(json_str: str) -> List[Book]:
    """Import books from a JSON string.
    
    Args:
        json_str: JSON string containing book data
        
    Returns:
        List[Book]: Imported books
    """
    try:
        books_data = json.loads(json_str)
        return [Book.from_dict(data) for data in books_data]
    except json.JSONDecodeError:
        return []


def export_to_csv(books: List[Book]) -> str:
    """Export books to a CSV string.
    
    Args:
        books: List of books to export
        
    Returns:
        str: CSV representation of the books
    """
    if not books:
        return ""
    
    output = StringIO()
    fields = list(books[0].to_dict().keys())
    
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    
    for book in books:
        book_dict = book.to_dict()
        # Convert list fields to comma-separated strings
        for key, value in book_dict.items():
            if isinstance(value, list):
                book_dict[key] = ",".join(value)
        writer.writerow(book_dict)
    
    return output.getvalue()


def import_from_csv(csv_str: str) -> List[Book]:
    """Import books from a CSV string.
    
    Args:
        csv_str: CSV string containing book data
        
    Returns:
        List[Book]: Imported books
    """
    if not csv_str.strip():
        return []
    
    try:
        input_data = StringIO(csv_str)
        reader = csv.DictReader(input_data)
        books = []
        
        for row in reader:
            # Process each row
            book_data = {}
            
            # Process string fields
            for key, value in row.items():
                if key in ["id", "title", "author", "isbn", "description", "cover_url", "read_status", "date_added"]:
                    book_data[key] = value
                
                # Convert genre string to list
                elif key == "genre" and value:
                    book_data[key] = value.split(",")
                
                # Convert numeric fields
                elif key == "year" and value:
                    try:
                        book_data[key] = int(value)
                    except ValueError:
                        pass  # Will use default value
                
                elif key == "rating" and value:
                    try:
                        book_data[key] = float(value)
                    except ValueError:
                        pass  # Will use default value
            
            try:
                # Set default empty list for genre if not provided
                if "genre" not in book_data or not book_data["genre"]:
                    book_data["genre"] = []
                
                books.append(Book.from_dict(book_data))
            except Exception as e:
                print(f"Error importing book: {e}")
        
        return books
    except Exception as e:
        print(f"Error loading books: {e}")
        return []


def generate_sample_books() -> List[Book]:
    """Generate a list of sample books.
    
    Returns:
        List[Book]: Sample books
    """
    return [
        Book(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            year=1960,
            isbn="9780061120084",
            genre=["Fiction", "Classic", "Historical"],
            rating=4.27,
            description="The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.",
            cover_url="https://covers.openlibrary.org/b/id/8231488-L.jpg",
            read_status="Read"
        ),
        Book(
            title="1984",
            author="George Orwell",
            year=1949,
            isbn="9780451524935",
            genre=["Fiction", "Classic", "Dystopian"],
            rating=4.19,
            description="Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that grows more haunting as its futuristic purgatory becomes more real.",
            cover_url="https://covers.openlibrary.org/b/id/8575173-L.jpg",
            read_status="Read"
        ),
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            year=1925,
            isbn="9780743273565",
            genre=["Fiction", "Classic", "Literature"],
            rating=3.93,
            description="A portrait of the Jazz Age in all of its decadence and excess.",
            cover_url="https://covers.openlibrary.org/b/id/8410768-L.jpg",
            read_status="Reading"
        ),
        Book(
            title="Pride and Prejudice",
            author="Jane Austen",
            year=1813,
            isbn="9780141439518",
            genre=["Fiction", "Classic", "Romance"],
            rating=4.25,
            description="Since its immediate success in 1813, Pride and Prejudice has remained one of the most popular novels in the English language.",
            cover_url="https://covers.openlibrary.org/b/id/8701802-L.jpg",
            read_status="To Read"
        ),
        Book(
            title="The Catcher in the Rye",
            author="J.D. Salinger",
            year=1951,
            isbn="9780316769488",
            genre=["Fiction", "Classic", "Coming of Age"],
            rating=3.81,
            description="The hero-narrator of The Catcher in the Rye is an ancient child of sixteen, a native New Yorker named Holden Caulfield.",
            cover_url="https://covers.openlibrary.org/b/id/12645114-L.jpg",
            read_status="To Read"
        )
    ]