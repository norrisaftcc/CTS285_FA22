"""
Project Structure:

openlibrary_client/
├── __init__.py
├── client.py
├── models.py
├── exceptions.py
├── utils.py
└── config.py
setup.py
README.md
LICENSE
"""

# File: openlibrary_client/__init__.py
"""
OpenLibrary Client - A Python library for the Open Library API.

This library provides a simple interface to the Open Library API,
focusing on book searches and retrieving book information.
"""

__version__ = '0.1.0'
__author__ = 'Your Team'

from .client import OpenLibraryClient
from .models import Book, Author, Edition
from .exceptions import OpenLibraryError, RateLimitError, APIError

# File: openlibrary_client/client.py
"""
Core client for interacting with the Open Library API.
"""

import requests
import urllib.parse
from typing import Dict, List, Optional, Union, Any

from .models import Book, Author, Edition
from .exceptions import OpenLibraryError, RateLimitError, APIError
from .utils import safe_request
from .config import DEFAULT_HEADERS, API_BASE_URL


class OpenLibraryClient:
    """
    Client for interacting with the Open Library API.
    
    This class provides methods for searching books, retrieving book details,
    and accessing book covers.
    
    Attributes:
        app_name (str): The name of your application
        contact_email (str): Your contact email
        base_url (str): The base URL for the Open Library API
        headers (dict): HTTP headers to include in requests
    """
    
    def __init__(self, app_name: str, contact_email: str, 
                 base_url: str = API_BASE_URL):
        """
        Initialize the OpenLibraryClient.
        
        Args:
            app_name (str): The name of your application
            contact_email (str): Your contact email
            base_url (str, optional): The base URL for the Open Library API.
                Defaults to API_BASE_URL.
        """
        self.app_name = app_name
        self.contact_email = contact_email
        self.base_url = base_url
        self.headers = DEFAULT_HEADERS.copy()
        self.headers["User-Agent"] = f"{app_name}/1.0 ({contact_email})"

    def search_books(self, 
                     title: Optional[str] = None, 
                     author: Optional[str] = None,
                     publisher: Optional[str] = None,
                     subject: Optional[str] = None,
                     language: Optional[str] = None,
                     limit: int = 10,
                     page: int = 1) -> Dict[str, Any]:
        """
        Search for books with the given parameters.
        
        Args:
            title (str, optional): Book title to search for
            author (str, optional): Author name to search for
            publisher (str, optional): Publisher to search for
            subject (str, optional): Subject to search for
            language (str, optional): Language code to filter by
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            page (int, optional): Page number for pagination. Defaults to 1.
            
        Returns:
            Dict containing search results with the following keys:
                - total_found: Total number of books matching the search
                - books: List of Book objects matching the search
                
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        params = {}
        
        # Add search parameters if provided
        if title:
            params["title"] = title
        if author:
            params["author"] = author
        if publisher:
            params["publisher"] = publisher
        if subject:
            params["subject"] = subject
        if language:
            params["language"] = language
            
        # Add general query parameter if only title is provided
        if title and not any([author, publisher, subject, language]):
            params["q"] = title
            
        # Add pagination parameters
        params["limit"] = limit
        params["page"] = page
        
        # Ensure at least one search parameter is provided
        if not any([title, author, publisher, subject, language]):
            raise ValueError("At least one search parameter must be provided")
            
        url = f"{self.base_url}/search.json"
        
        response = safe_request("GET", url, headers=self.headers, params=params)
        
        # Process the response
        books = []
        for doc in response.get("docs", []):
            books.append(Book.from_search_result(doc))
            
        return {
            "total_found": response.get("numFound", 0),
            "books": books
        }
    
    def search_by_title(self, title: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """
        Search for books by title.
        
        Args:
            title (str): The title to search for
            limit (int, optional): Maximum number of results to return. Defaults to 10.
            page (int, optional): Page number for pagination. Defaults to 1.
            
        Returns:
            Dict containing search results
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        return self.search_books(title=title, limit=limit, page=page)
    
    def get_book(self, olid: str) -> Book:
        """
        Get detailed information about a book by its Open Library ID.
        
        Args:
            olid (str): Open Library ID (works ID)
            
        Returns:
            Book: Book object with detailed information
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        url = f"{self.base_url}/works/{olid}.json"
        
        response = safe_request("GET", url, headers=self.headers)
        
        return Book.from_work_data(response)
    
    def get_editions(self, work_olid: str, limit: int = 10) -> List[Edition]:
        """
        Get editions of a book by its Open Library Work ID.
        
        Args:
            work_olid (str): Open Library Work ID
            limit (int, optional): Maximum number of editions to retrieve. Defaults to 10.
            
        Returns:
            List[Edition]: List of Edition objects
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        url = f"{self.base_url}/works/{work_olid}/editions.json"
        
        params = {"limit": limit}
        
        response = safe_request("GET", url, headers=self.headers, params=params)
        
        editions = []
        for entry in response.get("entries", []):
            editions.append(Edition.from_data(entry))
            
        return editions
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Get a book by ISBN.
        
        Args:
            isbn (str): ISBN-10 or ISBN-13
            
        Returns:
            Optional[Book]: Book object if found, None otherwise
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        url = f"{self.base_url}/isbn/{isbn}.json"
        
        try:
            response = safe_request("GET", url, headers=self.headers)
            
            # ISBN endpoint returns an edition, not a work
            edition = Edition.from_data(response)
            
            # If the edition has a work ID, get the work data
            if edition.work_olid:
                return self.get_book(edition.work_olid)
            else:
                # Create a minimal Book object from the edition data
                return Book.from_edition(edition)
                
        except OpenLibraryError as e:
            if "404" in str(e):
                return None
            raise
    
    def get_author(self, author_olid: str) -> Author:
        """
        Get information about an author by their Open Library ID.
        
        Args:
            author_olid (str): Open Library Author ID
            
        Returns:
            Author: Author object with detailed information
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        url = f"{self.base_url}/authors/{author_olid}.json"
        
        response = safe_request("GET", url, headers=self.headers)
        
        return Author.from_data(response)
    
    def get_author_works(self, author_olid: str, limit: int = 10) -> List[Book]:
        """
        Get works by an author.
        
        Args:
            author_olid (str): Open Library Author ID
            limit (int, optional): Maximum number of works to retrieve. Defaults to 10.
            
        Returns:
            List[Book]: List of Book objects
            
        Raises:
            OpenLibraryError: If there is an error with the request
        """
        url = f"{self.base_url}/authors/{author_olid}/works.json"
        
        params = {"limit": limit}
        
        response = safe_request("GET", url, headers=self.headers, params=params)
        
        books = []
        for entry in response.get("entries", []):
            # Create a minimal Book object from the work data
            olid = entry.get("key", "").split("/")[-1]
            books.append(Book(
                olid=olid,
                title=entry.get("title", "Unknown"),
                authors=[Author(olid=author_olid)]
            ))
            
        return books
    
    def get_cover_url(self, identifier: str, id_type: str = "isbn", size: str = "M") -> str:
        """
        Generate a URL for a book cover image.
        
        Args:
            identifier (str): The book identifier (ISBN, OLID, etc.)
            id_type (str, optional): Type of identifier. One of: 'isbn', 'olid', 
                'oclc', 'lccn', or 'id'. Defaults to "isbn".
            size (str, optional): Size of the image. One of: 'S', 'M', or 'L' for 
                small, medium, large. Defaults to "M".
            
        Returns:
            str: URL to the cover image
            
        Raises:
            ValueError: If id_type or size is invalid
        """
        valid_types = ['isbn', 'olid', 'oclc', 'lccn', 'id']
        valid_sizes = ['S', 'M', 'L']
        
        if id_type not in valid_types:
            raise ValueError(f"Invalid id_type. Must be one of: {', '.join(valid_types)}")
        
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
        
        return f"https://covers.openlibrary.org/b/{id_type}/{identifier}-{size}.jpg"


# File: openlibrary_client/models.py
"""
Data models for the Open Library API.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field
import datetime


@dataclass
class Author:
    """
    Represents an author.
    
    Attributes:
        olid (str): Open Library ID for the author
        name (str): Author's name
        birth_date (str): Author's birth date
        death_date (str): Author's death date
        bio (str): Author's biography
        photos (List[int]): List of photo IDs
    """
    olid: str = None
    name: str = "Unknown"
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    bio: Optional[str] = None
    photos: List[int] = field(default_factory=list)
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Author':
        """
        Create an Author object from API data.
        
        Args:
            data (Dict): Author data from the API
            
        Returns:
            Author: New Author object
        """
        # Extract OLID from the key (e.g., "/authors/OL1234A" -> "OL1234A")
        olid = data.get("key", "").split("/")[-1]
        
        return cls(
            olid=olid,
            name=data.get("name", "Unknown"),
            birth_date=data.get("birth_date"),
            death_date=data.get("death_date"),
            bio=data.get("bio"),
            photos=data.get("photos", [])
        )
    
    @classmethod
    def from_search_result(cls, author_data: Dict[str, Any]) -> 'Author':
        """
        Create an Author object from search result data.
        
        Args:
            author_data (Dict): Author data from search results
            
        Returns:
            Author: New Author object
        """
        # If it's just a name string, create a minimal author object
        if isinstance(author_data, str):
            return cls(name=author_data)
        
        # If it's a dict with a key, extract the OLID
        olid = None
        if "key" in author_data:
            olid = author_data["key"].split("/")[-1]
            
        return cls(
            olid=olid,
            name=author_data.get("name", "Unknown")
        )
    
    def get_photo_url(self, size: str = "M") -> Optional[str]:
        """
        Get the URL for the author's photo.
        
        Args:
            size (str, optional): Size of the image. One of: 'S', 'M', or 'L'
                for small, medium, large. Defaults to "M".
                
        Returns:
            Optional[str]: URL to the photo image, or None if no photos
        """
        if not self.photos:
            return None
            
        valid_sizes = ['S', 'M', 'L']
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
            
        # Use the first photo ID
        photo_id = self.photos[0]
        
        return f"https://covers.openlibrary.org/a/id/{photo_id}-{size}.jpg"


@dataclass
class Edition:
    """
    Represents a specific edition of a book.
    
    Attributes:
        olid (str): Open Library ID for the edition
        title (str): Edition title
        publishers (List[str]): List of publishers
        publish_date (str): Publication date
        isbn_10 (List[str]): List of ISBN-10 identifiers
        isbn_13 (List[str]): List of ISBN-13 identifiers
        work_olid (str): Open Library ID for the work this edition belongs to
        covers (List[int]): List of cover image IDs
        number_of_pages (int): Number of pages
        physical_format (str): Physical format of the book
        languages (List[str]): List of languages
    """
    olid: str = None
    title: str = "Unknown"
    subtitle: Optional[str] = None
    publishers: List[str] = field(default_factory=list)
    publish_date: Optional[str] = None
    isbn_10: List[str] = field(default_factory=list)
    isbn_13: List[str] = field(default_factory=list)
    work_olid: Optional[str] = None
    covers: List[int] = field(default_factory=list)
    number_of_pages: Optional[int] = None
    physical_format: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Edition':
        """
        Create an Edition object from API data.
        
        Args:
            data (Dict): Edition data from the API
            
        Returns:
            Edition: New Edition object
        """
        # Extract OLID from the key (e.g., "/books/OL1234M" -> "OL1234M")
        olid = data.get("key", "").split("/")[-1]
        
        # Extract work OLID if available
        work_olid = None
        if "works" in data and data["works"]:
            works_key = data["works"][0].get("key", "")
            if works_key:
                work_olid = works_key.split("/")[-1]
                
        # Extract languages
        languages = []
        if "languages" in data and data["languages"]:
            for lang in data["languages"]:
                if isinstance(lang, dict) and "key" in lang:
                    languages.append(lang["key"].split("/")[-1])
        
        return cls(
            olid=olid,
            title=data.get("title", "Unknown"),
            subtitle=data.get("subtitle"),
            publishers=data.get("publishers", []),
            publish_date=data.get("publish_date"),
            isbn_10=data.get("isbn_10", []),
            isbn_13=data.get("isbn_13", []),
            work_olid=work_olid,
            covers=data.get("covers", []),
            number_of_pages=data.get("number_of_pages"),
            physical_format=data.get("physical_format"),
            languages=languages
        )
    
    def get_cover_url(self, size: str = "M") -> Optional[str]:
        """
        Get the URL for the edition's cover image.
        
        Args:
            size (str, optional): Size of the image. One of: 'S', 'M', or 'L'
                for small, medium, large. Defaults to "M".
                
        Returns:
            Optional[str]: URL to the cover image, or None if no covers
        """
        if not self.covers:
            # Try ISBN as a fallback
            if self.isbn_13:
                return f"https://covers.openlibrary.org/b/isbn/{self.isbn_13[0]}-{size}.jpg"
            if self.isbn_10:
                return f"https://covers.openlibrary.org/b/isbn/{self.isbn_10[0]}-{size}.jpg"
            # If no ISBN, try OLID
            if self.olid:
                return f"https://covers.openlibrary.org/b/olid/{self.olid}-{size}.jpg"
            return None
            
        valid_sizes = ['S', 'M', 'L']
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
            
        # Use the first cover ID
        cover_id = self.covers[0]
        
        return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"


@dataclass
class Book:
    """
    Represents a book (work).
    
    Attributes:
        olid (str): Open Library ID for the work
        title (str): Book title
        subtitle (str): Book subtitle
        authors (List[Author]): List of authors
        description (str): Book description
        subjects (List[str]): List of subjects
        subject_places (List[str]): List of subject places
        subject_times (List[str]): List of subject times
        subject_people (List[str]): List of subject people
        first_publish_date (str): First publication date
        covers (List[int]): List of cover image IDs
        editions_count (int): Number of editions
    """
    olid: str = None
    title: str = "Unknown"
    subtitle: Optional[str] = None
    authors: List[Author] = field(default_factory=list)
    description: Optional[str] = None
    subjects: List[str] = field(default_factory=list)
    subject_places: List[str] = field(default_factory=list)
    subject_times: List[str] = field(default_factory=list)
    subject_people: List[str] = field(default_factory=list)
    first_publish_date: Optional[str] = None
    covers: List[int] = field(default_factory=list)
    editions_count: int = 0
    
    @classmethod
    def from_work_data(cls, data: Dict[str, Any]) -> 'Book':
        """
        Create a Book object from work API data.
        
        Args:
            data (Dict): Work data from the API
            
        Returns:
            Book: New Book object
        """
        # Extract OLID from the key (e.g., "/works/OL1234W" -> "OL1234W")
        olid = data.get("key", "").split("/")[-1]
        
        # Process authors
        authors = []
        if "authors" in data and data["authors"]:
            for author_data in data["authors"]:
                if "author" in author_data and "key" in author_data["author"]:
                    author_key = author_data["author"]["key"]
                    author_olid = author_key.split("/")[-1]
                    authors.append(Author(olid=author_olid))
        
        # Process description
        description = None
        if "description" in data:
            # Description can be a string or an object with a value field
            if isinstance(data["description"], str):
                description = data["description"]
            elif isinstance(data["description"], dict) and "value" in data["description"]:
                description = data["description"]["value"]
        
        return cls(
            olid=olid,
            title=data.get("title", "Unknown"),
            subtitle=data.get("subtitle"),
            authors=authors,
            description=description,
            subjects=data.get("subjects", []),
            subject_places=data.get("subject_places", []),
            subject_times=data.get("subject_times", []),
            subject_people=data.get("subject_people", []),
            first_publish_date=data.get("first_publish_date"),
            covers=data.get("covers", [])
        )
    
    @classmethod
    def from_search_result(cls, data: Dict[str, Any]) -> 'Book':
        """
        Create a Book object from search result data.
        
        Args:
            data (Dict): Book data from search results
            
        Returns:
            Book: New Book object
        """
        # Extract OLID from the key (e.g., "/works/OL1234W" -> "OL1234W")
        olid = data.get("key", "").replace("/works/", "")
        
        # Process authors
        authors = []
        if "author_name" in data and "author_key" in data:
            for i, author_name in enumerate(data["author_name"]):
                if i < len(data["author_key"]):
                    authors.append(Author(
                        olid=data["author_key"][i],
                        name=author_name
                    ))
                else:
                    authors.append(Author(name=author_name))
        elif "author_name" in data:
            for author_name in data["author_name"]:
                authors.append(Author(name=author_name))
        
        return cls(
            olid=olid,
            title=data.get("title", "Unknown"),
            subtitle=data.get("subtitle"),
            authors=authors,
            subjects=data.get("subject", []),
            subject_places=data.get("place", []),
            subject_times=data.get("time", []),
            subject_people=data.get("person", []),
            first_publish_date=data.get("first_publish_year"),
            covers=[data.get("cover_i")] if data.get("cover_i") else [],
            editions_count=data.get("edition_count", 0)
        )
    
    @classmethod
    def from_edition(cls, edition: Edition) -> 'Book':
        """
        Create a minimal Book object from an Edition.
        
        This is used when we only have edition data but need a Book object.
        
        Args:
            edition (Edition): Edition object
            
        Returns:
            Book: New Book object with minimal data
        """
        return cls(
            olid=edition.work_olid,
            title=edition.title,
            subtitle=edition.subtitle,
            covers=edition.covers
        )
    
    def get_cover_url(self, size: str = "M") -> Optional[str]:
        """
        Get the URL for the book's cover image.
        
        Args:
            size (str, optional): Size of the image. One of: 'S', 'M', or 'L'
                for small, medium, large. Defaults to "M".
                
        Returns:
            Optional[str]: URL to the cover image, or None if no covers
        """
        if not self.covers:
            # Try OLID as a fallback
            if self.olid:
                return f"https://covers.openlibrary.org/b/olid/{self.olid}-{size}.jpg"
            return None
            
        valid_sizes = ['S', 'M', 'L']
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
            
        # Use the first cover ID
        cover_id = self.covers[0]
        
        return f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"


# File: openlibrary_client/exceptions.py
"""
Exceptions for the Open Library API client.
"""

class OpenLibraryError(Exception):
    """Base exception for all Open Library API errors."""
    pass

class RateLimitError(OpenLibraryError):
    """Raised when the API rate limit is exceeded."""
    pass

class APIError(OpenLibraryError):
    """Raised when the API returns an error response."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


# File: openlibrary_client/utils.py
"""
Utility functions for the Open Library API client.
"""

import requests
from typing import Dict, Any, Optional
import time
import json

from .exceptions import OpenLibraryError, RateLimitError, APIError


def safe_request(method: str, url: str, 
                 headers: Optional[Dict[str, str]] = None, 
                 params: Optional[Dict[str, Any]] = None, 
                 data: Optional[Dict[str, Any]] = None,
                 retries: int = 3, 
                 retry_delay: float = 1.0) -> Dict[str, Any]:
    """
    Make a safe HTTP request with error handling and retries.
    
    Args:
        method (str): HTTP method (GET, POST, etc.)
        url (str): URL to request
        headers (Dict[str, str], optional): HTTP headers. Defaults to None.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        data (Dict[str, Any], optional): Request body data. Defaults to None.
        retries (int, optional): Number of retries on failure. Defaults to 3.
        retry_delay (float, optional): Delay between retries in seconds. Defaults to 1.0.
        
    Returns:
        Dict[str, Any]: Response JSON data
        
    Raises:
        OpenLibraryError: If there is an error with the request
        RateLimitError: If the API rate limit is exceeded
        APIError: If the API returns an error response
    """
    attempt = 0
    
    while attempt < retries:
        try:
            response = requests.request(
                method, 
                url, 
                headers=headers, 
                params=params, 
                json=data,
                timeout=10
            )
            
            # Handle rate limiting
            if response.status_code == 403:
                raise RateLimitError("API rate limit exceeded. Try again later.")
            
            # Handle other errors
            if response.status_code >= 400:
                raise APIError(
                    response.status_code, 
                    f"Error accessing {url}: {response.text}"
                )
            
            # Parse JSON response
            return response.json()
            
        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt >= retries:
                raise OpenLibraryError(f"Request failed after {retries} attempts: {str(e)}")
            
            # Exponential backoff: increase delay with each retry
            time.sleep(retry_delay * (2 ** (attempt - 1)))
            
        except json.JSONDecodeError:
            raise OpenLibraryError(f"Invalid JSON response from {url}")


def normalize_isbn(isbn: str) -> str:
    """
    Normalize an ISBN by removing hyphens and spaces.
    
    Args:
        isbn (str): ISBN to normalize
        
    Returns:
        str: Normalized ISBN
    """
    # Remove hyphens, spaces, and other non-alphanumeric characters
    return ''.join(c for c in isbn if c.isalnum())


# File: openlibrary_client/config.py
"""
Configuration for the Open Library API client.
"""

API_BASE_URL = "https://openlibrary.org"

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# File: setup.py
"""
Setup script for the openlibrary-client package.
"""

from setuptools import setup, find_packages

setup(
    name="openlibrary-client",
    version="0.1.0",
    description="Python client for the Open Library API",
    author="Your Team",
    author_email="team@example.com",
    url="https://github.com/yourteam/openlibrary-client",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)


# File: README.md
"""
# Open Library Client

A Python client library for the Open Library API.

## Installation

```bash
pip install openlibrary-client
```

## Quick Start

```python
from openlibrary_client import OpenLibraryClient

# Initialize the client with your app name and contact email
client = OpenLibraryClient(
    app_name="MyAwesomeApp",
    contact_email="contact@example.com"
)

# Search for books by title
results = client.search_by_title("The Great Gatsby")

# Print results
print(f"Found {results['total_found']} books")
for book in results['books']:
    print(f"Title: {book.title}")
    print(f"Author(s): {', '.join(author.name for author in book.authors)}")
    print(f"First Published: {book.first_publish_date}")
    print(f"Open Library ID: {book.olid}")
    print(f"Cover URL: {book.get_cover_url()}")
    print("---")

# Get book details by OLID
book = client.get_book("OL23109W")  # The Great Gatsby
print(f"Title: {book.title}")
print(f"Description: {book.description}")

# Get editions
editions = client.get_editions("OL23109W", limit=5)
for edition in editions:
    print(f"Edition: {edition.title}")
    print(f"Publisher: {', '.join(edition.publishers)}")
    print(f"Publish Date: {edition.publish_date}")
    print(f"ISBN-13: {edition.isbn_13}")
    print("---")

# Get book by ISBN
book = client.get_book_by_isbn("9780743273565")  # The Great Gatsby
if book:
    print(f"Found book: {book.title}")
```

## Features

- Search for books by title, author, publisher, and more
- Get detailed information about books, authors, and editions
- Retrieve book covers and author photos
- Handle rate limiting and errors gracefully
- Fully typed with Python type hints

## Documentation

For more detailed documentation, see the [full documentation](https://github.com/yourteam/openlibrary-client).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""


# File: LICENSE
"""
MIT License

Copyright (c) 2023 Your Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Usage Examples

"""
# Basic Usage Examples

# 1. Simple title search
from openlibrary_client import OpenLibraryClient

client = OpenLibraryClient(
    app_name="MyBookApp", 
    contact_email="dev@example.com"
)

# Search for books by title
results = client.search_by_title("The Hobbit")

print(f"Found {results['total_found']} books")
for book in results['books']:
    print(f"Title: {book.title}")
    print(f"Author(s): {', '.join(author.name for author in book.authors)}")
    print(f"Open Library ID: {book.olid}")
    print(f"Cover URL: {book.get_cover_url()}")
    print("---")

# 2. Advanced search with multiple criteria
advanced_results = client.search_books(
    title="Lord of the Rings",
    author="Tolkien",
    limit=5
)

# 3. Get a book by Open Library ID
book = client.get_book("OL27448W")  # The Hobbit
print(f"Title: {book.title}")
print(f"Description: {book.description}")
print(f"Subjects: {', '.join(book.subjects[:5])}")

# 4. Get editions of a book
editions = client.get_editions("OL27448W", limit=3)
for edition in editions:
    print(f"Edition: {edition.title}")
    print(f"Publisher: {', '.join(edition.publishers)}")
    print(f"ISBN-13: {', '.join(edition.isbn_13)}")
    print("---")

# 5. Get a book by ISBN
book_by_isbn = client.get_book_by_isbn("9780547928227")  # The Hobbit
if book_by_isbn:
    print(f"Found book by ISBN: {book_by_isbn.title}")
"""
