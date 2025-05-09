"""
SQLite storage implementation for the BookSense application.

This module provides a SQLite-based backend for storing and retrieving book data.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Union

from .models import Book
from .storage import StorageInterface


class SqliteStorage(StorageInterface):
    """SQLite database storage implementation."""

    def __init__(self, db_path: str):
        """Initialize with the path to the SQLite database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Create the database and tables if they don't exist."""
        # Create the directory if it doesn't exist
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Connect to the database (will create it if it doesn't exist)
        with sqlite3.connect(self.db_path) as conn:
            # Create the books table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    isbn TEXT,
                    rating REAL,
                    description TEXT,
                    cover_url TEXT,
                    read_status TEXT,
                    date_added TEXT
                )
            ''')
            
            # Create the genres table (many-to-many relationship)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            ''')
            
            # Create the book_genres table (junction table)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS book_genres (
                    book_id TEXT,
                    genre_id INTEGER,
                    PRIMARY KEY (book_id, genre_id),
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (genre_id) REFERENCES genres (id)
                )
            ''')
            
            # Create indexes for better performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_books_title ON books (title)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_books_author ON books (author)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_books_year ON books (year)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_books_read_status ON books (read_status)')
            
            conn.commit()

    def _book_from_row(self, row: tuple, genres: List[str]) -> Book:
        """Convert a database row to a Book object.
        
        Args:
            row: Database row with book data
            genres: List of genres for the book
            
        Returns:
            Book: A Book object created from the row data
        """
        # Create a dictionary from the row
        book_data = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'year': row[3],
            'isbn': row[4],
            'rating': row[5],
            'description': row[6],
            'cover_url': row[7],
            'read_status': row[8],
            'date_added': row[9],
            'genre': genres
        }
        
        # Handle None values
        for key, value in book_data.items():
            if value is None and key not in ['isbn', 'cover_url']:
                if key == 'rating':
                    book_data[key] = 0.0
                elif key == 'description':
                    book_data[key] = ""
                elif key == 'read_status':
                    book_data[key] = "To Read"
                elif key == 'date_added':
                    book_data[key] = datetime.now().isoformat()
        
        # Create a Book object
        return Book.from_dict(book_data)

    def _get_book_genres(self, conn: sqlite3.Connection, book_id: str) -> List[str]:
        """Get all genres for a specific book.
        
        Args:
            conn: SQLite connection
            book_id: The book ID to get genres for
            
        Returns:
            List[str]: List of genre names
        """
        cursor = conn.execute('''
            SELECT g.name
            FROM genres g
            JOIN book_genres bg ON g.id = bg.genre_id
            WHERE bg.book_id = ?
        ''', (book_id,))
        
        return [row[0] for row in cursor.fetchall()]

    def _save_book_genres(self, conn: sqlite3.Connection, book: Book):
        """Save the genres for a book.
        
        Args:
            conn: SQLite connection
            book: The book with genres to save
        """
        # Delete existing genres for this book
        conn.execute('DELETE FROM book_genres WHERE book_id = ?', (book.id,))
        
        # Add each genre
        for genre in book.genre:
            # First, ensure the genre exists in the genres table
            cursor = conn.execute('SELECT id FROM genres WHERE name = ?', (genre,))
            result = cursor.fetchone()
            
            if result:
                genre_id = result[0]
            else:
                cursor = conn.execute('INSERT INTO genres (name) VALUES (?)', (genre,))
                genre_id = cursor.lastrowid
            
            # Now add the book-genre relationship
            conn.execute('INSERT INTO book_genres (book_id, genre_id) VALUES (?, ?)',
                      (book.id, genre_id))

    def load(self) -> List[Book]:
        """Load all books from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT * FROM books')
                books = []
                
                for row in cursor.fetchall():
                    # Get genres for this book
                    genres = self._get_book_genres(conn, row[0])
                    
                    # Create a Book object
                    book = self._book_from_row(row, genres)
                    books.append(book)
                
                return books
        except sqlite3.Error as e:
            print(f"Error loading books from database: {e}")
            return []

    def save(self, books: List[Book]) -> bool:
        """Save all books to the database.
        
        This method completely replaces the database content with the given books.
        
        Args:
            books: List of books to save
            
        Returns:
            bool: True if the operation was successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Begin transaction
                conn.execute('BEGIN TRANSACTION')
                
                # Clear existing data
                conn.execute('DELETE FROM book_genres')
                conn.execute('DELETE FROM books')
                
                # Don't delete genres - they might be referenced by other books in the future
                
                # Add each book
                for book in books:
                    self._add_book_to_db(conn, book)
                
                # Commit transaction
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error saving books to database: {e}")
            return False

    def get_book(self, book_id: str) -> Optional[Book]:
        """Get a specific book by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,))
                row = cursor.fetchone()
                
                if row:
                    # Get genres for this book
                    genres = self._get_book_genres(conn, row[0])
                    
                    # Create a Book object
                    return self._book_from_row(row, genres)
                
                return None
        except sqlite3.Error as e:
            print(f"Error getting book from database: {e}")
            return None

    def _add_book_to_db(self, conn: sqlite3.Connection, book: Book) -> bool:
        """Add a book to the database.
        
        Args:
            conn: SQLite connection
            book: The book to add
            
        Returns:
            bool: True if the operation was successful
        """
        # Insert the book
        conn.execute('''
            INSERT INTO books (
                id, title, author, year, isbn, rating, 
                description, cover_url, read_status, date_added
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            book.id, 
            book.title, 
            book.author, 
            book.year,
            book.isbn, 
            book.rating, 
            book.description, 
            book.cover_url,
            book.read_status,
            book.date_added.isoformat() if hasattr(book.date_added, 'isoformat') else book.date_added
        ))
        
        # Save the book's genres
        self._save_book_genres(conn, book)
        
        return True

    def add_book(self, book: Book) -> bool:
        """Add a new book to storage."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check if a book with this ID already exists
                cursor = conn.execute('SELECT id FROM books WHERE id = ?', (book.id,))
                if cursor.fetchone():
                    return False
                
                # Begin transaction
                conn.execute('BEGIN TRANSACTION')
                
                # Add the book
                self._add_book_to_db(conn, book)
                
                # Commit transaction
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error adding book to database: {e}")
            return False

    def update_book(self, book: Book) -> bool:
        """Update an existing book."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check if the book exists
                cursor = conn.execute('SELECT id FROM books WHERE id = ?', (book.id,))
                if not cursor.fetchone():
                    return False
                
                # Begin transaction
                conn.execute('BEGIN TRANSACTION')
                
                # Update the book
                conn.execute('''
                    UPDATE books SET
                        title = ?,
                        author = ?,
                        year = ?,
                        isbn = ?,
                        rating = ?,
                        description = ?,
                        cover_url = ?,
                        read_status = ?,
                        date_added = ?
                    WHERE id = ?
                ''', (
                    book.title, 
                    book.author, 
                    book.year,
                    book.isbn, 
                    book.rating, 
                    book.description, 
                    book.cover_url,
                    book.read_status,
                    book.date_added.isoformat() if hasattr(book.date_added, 'isoformat') else book.date_added,
                    book.id
                ))
                
                # Update the book's genres
                self._save_book_genres(conn, book)
                
                # Commit transaction
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error updating book in database: {e}")
            return False

    def delete_book(self, book_id: str) -> bool:
        """Delete a book by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check if the book exists
                cursor = conn.execute('SELECT id FROM books WHERE id = ?', (book_id,))
                if not cursor.fetchone():
                    return False
                
                # Begin transaction
                conn.execute('BEGIN TRANSACTION')
                
                # Delete the book's genres
                conn.execute('DELETE FROM book_genres WHERE book_id = ?', (book_id,))
                
                # Delete the book
                conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
                
                # Commit transaction
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting book from database: {e}")
            return False