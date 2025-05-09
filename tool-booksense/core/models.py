"""
Data models for the BookSense application.

This module defines the core data structures used throughout the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4


@dataclass
class Book:
    """
    Represents a book in the collection.
    
    Attributes:
        id: Unique identifier for the book
        title: Title of the book
        author: Author of the book
        year: Publication year
        isbn: ISBN number (optional)
        genre: List of genres/categories
        rating: User rating (0-5)
        description: Book description
        cover_url: URL to cover image (optional)
        read_status: Reading status ("Read", "Reading", "To Read")
        date_added: When the book was added to the collection
    """
    title: str
    author: str
    year: int
    isbn: Optional[str] = None
    genre: List[str] = field(default_factory=list)
    rating: float = 0.0
    description: str = ""
    cover_url: Optional[str] = None
    read_status: str = "To Read"
    id: str = field(default_factory=lambda: str(uuid4()))
    date_added: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate book data after initialization."""
        if not self.title:
            raise ValueError("Book title cannot be empty")
        
        if not self.author:
            raise ValueError("Book author cannot be empty")
        
        if not isinstance(self.year, int):
            try:
                self.year = int(self.year)
            except (ValueError, TypeError):
                raise ValueError("Book year must be a valid integer")
                
        if self.year < 1000 or self.year > datetime.now().year + 5:
            raise ValueError(f"Book year must be between 1000 and {datetime.now().year + 5}")
            
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Book rating must be between 0 and 5")
            
        valid_statuses = ["Read", "Reading", "To Read"]
        if self.read_status not in valid_statuses:
            raise ValueError(f"Read status must be one of: {', '.join(valid_statuses)}")
    
    def to_dict(self) -> dict:
        """Convert the book to a dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "genre": self.genre,
            "rating": self.rating,
            "description": self.description,
            "cover_url": self.cover_url,
            "read_status": self.read_status,
            "date_added": self.date_added.isoformat() if hasattr(self.date_added, 'isoformat') else self.date_added
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create a book from a dictionary representation."""
        # Handle date conversion
        if 'date_added' in data and isinstance(data['date_added'], str):
            try:
                data['date_added'] = datetime.fromisoformat(data['date_added'])
            except ValueError:
                data['date_added'] = datetime.now()
        
        # Create a new book instance with the data
        return cls(**data)