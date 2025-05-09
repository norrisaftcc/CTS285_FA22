"""
Open Library integration service for the BookSense application.

This module provides functions to interact with the Open Library API
for searching books, retrieving book details, and fetching cover images.
"""

import requests
import urllib.parse
from typing import Dict, List, Optional, Any, Union
import time
from datetime import datetime

from .models import Book


class OpenLibraryService:
    """Service for interacting with the Open Library API."""
    
    # Base URLs for the Open Library API
    SEARCH_URL = "https://openlibrary.org/search.json"
    WORKS_URL = "https://openlibrary.org/works/{}.json"
    EDITIONS_URL = "https://openlibrary.org/works/{}/editions.json"
    COVER_URL = "https://covers.openlibrary.org/b/{}/{}-{}.jpg"
    
    # Default headers for API requests
    DEFAULT_HEADERS = {
        "User-Agent": "BookSense/1.0 (github.com/CTS285_FA22/tool-booksense)"
    }
    
    # Cache for API responses to avoid duplicate requests
    _cache = {}
    _cache_expiry = {}
    CACHE_DURATION = 3600  # Cache duration in seconds (1 hour)
    
    @classmethod
    def _get_cached_or_request(cls, url: str, headers: Optional[Dict] = None, 
                              params: Optional[Dict] = None) -> Dict:
        """Get data from cache or make a new request.
        
        Args:
            url: The URL to request
            headers: Request headers (optional)
            params: Query parameters (optional)
            
        Returns:
            Dict: JSON response or empty dict if error
        """
        # Create a cache key from the URL and params
        cache_key = f"{url}:{str(params)}"
        
        # Check if we have a cached response
        current_time = time.time()
        if cache_key in cls._cache and cls._cache_expiry.get(cache_key, 0) > current_time:
            return cls._cache[cache_key]
        
        # No cache or expired, make a new request
        try:
            # Merge default headers with provided headers
            request_headers = cls.DEFAULT_HEADERS.copy()
            if headers:
                request_headers.update(headers)
            
            # Make the request
            response = requests.get(url, headers=request_headers, params=params, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse JSON response
            data = response.json()
            
            # Cache the response
            cls._cache[cache_key] = data
            cls._cache_expiry[cache_key] = current_time + cls.CACHE_DURATION
            
            return data
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to the Open Library API")
        except requests.exceptions.Timeout:
            print("Timeout Error: The request to Open Library API timed out")
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        except ValueError:  # Includes JSONDecodeError
            print("Error: Could not decode the JSON response from Open Library")
        
        return {}
    
    @classmethod
    def search_books(cls, query: str, search_type: str = "title", 
                  limit: int = 10) -> Dict[str, Any]:
        """Search for books in Open Library.
        
        Args:
            query: The search query
            search_type: Type of search (title, author, subject)
            limit: Maximum number of results to return
            
        Returns:
            Dict: Dictionary containing search results and metadata
        """
        # Encode the query
        encoded_query = urllib.parse.quote(query)
        
        # Determine the search parameter based on search_type
        search_param = {
            "title": "title",
            "author": "author",
            "subject": "subject",
            "isbn": "isbn"
        }.get(search_type.lower(), "q")
        
        # Construct the URL
        if search_type.lower() == "all":
            url = f"{cls.SEARCH_URL}?q={encoded_query}&limit={limit}"
        else:
            url = f"{cls.SEARCH_URL}?{search_param}={encoded_query}&limit={limit}"
        
        # Make the request
        data = cls._get_cached_or_request(url)
        
        # Process the results
        if not data:
            return {"total_found": 0, "books": []}
        
        return {
            "total_found": data.get("numFound", 0),
            "books": data.get("docs", [])
        }
    
    @classmethod
    def get_book_details(cls, olid: str) -> Dict[str, Any]:
        """Get detailed information about a book by its Open Library ID.
        
        Args:
            olid: Open Library ID (works ID)
            
        Returns:
            Dict: Detailed book information
        """
        # Remove '/works/' prefix if present
        olid = olid.replace("/works/", "")
        
        # Construct the URL
        url = cls.WORKS_URL.format(olid)
        
        # Make the request
        return cls._get_cached_or_request(url)
    
    @classmethod
    def get_book_editions(cls, olid: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get editions of a book by its Open Library Work ID.
        
        Args:
            olid: Open Library Work ID
            limit: Maximum number of editions to retrieve
            
        Returns:
            List: List of editions
        """
        # Remove '/works/' prefix if present
        olid = olid.replace("/works/", "")
        
        # Construct the URL
        url = cls.EDITIONS_URL.format(olid)
        
        # Make the request
        data = cls._get_cached_or_request(url, params={"limit": limit})
        
        # Return editions
        return data.get("entries", [])
    
    @classmethod
    def get_cover_url(cls, identifier: str, id_type: str = "isbn", 
                    size: str = "M") -> str:
        """Generate URL for a book cover image.
        
        Args:
            identifier: The book identifier (ISBN, OLID, etc.)
            id_type: Type of identifier ('isbn', 'olid', 'oclc', 'lccn', or 'id')
            size: Size of the image ('S', 'M', or 'L' for small, medium, large)
            
        Returns:
            str: URL to the cover image
        """
        valid_types = ['isbn', 'olid', 'oclc', 'lccn', 'id']
        valid_sizes = ['S', 'M', 'L']
        
        if id_type not in valid_types:
            raise ValueError(f"Invalid id_type. Must be one of: {', '.join(valid_types)}")
        
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {', '.join(valid_sizes)}")
        
        return cls.COVER_URL.format(id_type, identifier, size)
    
    @classmethod
    def extract_book_info(cls, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the most useful information from an Open Library book result.
        
        Args:
            book_data: Book data from Open Library API
            
        Returns:
            Dict: Formatted book information
        """
        result = {
            "title": book_data.get("title", "Unknown"),
            "authors": book_data.get("author_name", ["Unknown"]),
            "first_published": book_data.get("first_publish_year", "Unknown"),
            "languages": book_data.get("language", []),
            "subjects": book_data.get("subject", [])[:5],  # Limit to 5 subjects
            "open_library_work_id": book_data.get("key", "").replace("/works/", ""),
            "open_library_url": f"https://openlibrary.org{book_data.get('key', '')}" if book_data.get("key") else None,
            "editions_count": book_data.get("edition_count", 0)
        }
        
        # Get ISBNs if available
        if "isbn" in book_data and book_data["isbn"]:
            result["isbn"] = book_data["isbn"][0]
            result["cover_url"] = cls.get_cover_url(book_data["isbn"][0], "isbn", "M")
        else:
            result["isbn"] = None
            
            # If no ISBN, try to get cover using Open Library ID
            if "cover_edition_key" in book_data:
                result["cover_url"] = cls.get_cover_url(book_data["cover_edition_key"], "olid", "M")
            else:
                result["cover_url"] = None
        
        return result
    
    @classmethod
    def create_book_from_ol_data(cls, book_data: Dict[str, Any]) -> Book:
        """Create a Book object from Open Library data.
        
        Args:
            book_data: Book data from Open Library API
            
        Returns:
            Book: A Book object
        """
        # Extract key information
        info = cls.extract_book_info(book_data)
        
        # Get the first author or default to "Unknown"
        author = info["authors"][0] if info["authors"] else "Unknown"
        
        # Get the publication year
        year = info["first_published"]
        if not isinstance(year, int) and not str(year).isdigit():
            year = datetime.now().year  # Default to current year if unknown
        
        # Get subjects as genres
        genres = info["subjects"] if info["subjects"] else []
        
        # Create and return a Book object
        return Book(
            title=info["title"],
            author=author,
            year=int(year),
            isbn=info["isbn"],
            genre=genres,
            description=book_data.get("description", ""),
            cover_url=info["cover_url"],
            read_status="To Read"  # Default to "To Read" for new books
        )