# BookSense Tool Project

## Overview
BookSense is a comprehensive book management application that allows users to search for books, build personal collections, and manage their reading. The project demonstrates modern software architecture with a modular design and multiple interface options. It features integration with the Open Library API for book search and metadata retrieval.

## Revision History

| Version | Date       | Description of Changes                       | Author            |
|---------|------------|--------------------------------------------|-------------------|
| 0.1.0   | 2023-05-09 | Initial project setup with Streamlit example | Claude           |
| 0.2.0   | 2023-05-10 | Added core functionality and SQLite storage  | Claude & Gallant |
| 0.3.0   | 2023-05-11 | Added Open Library API integration          | Claude           |
| 0.3.1   | 2023-05-11 | Fixed Streamlit sample search functionality  | Claude           |

## Features

### Core Functionality
- Book data model with validation
- Multiple storage backends (JSON and SQLite)
- Complete CRUD operations for book management
- Advanced search and filtering capabilities
- Collection statistics and metadata

### User Interfaces
- Streamlit web interface with responsive design
- Open Library integration for book search
- Book cover image display
- Collection management tools

### Open Library Integration
- Search books by title, author, subject, or ISBN
- Retrieve book covers and metadata
- Add books from Open Library to personal collection

## Project Structure

```
tool-booksense/
├── core/               # Core functionality
│   ├── models.py       # Data models (Book class)
│   ├── storage.py      # Storage interface and JSON implementation
│   ├── storage_sqlite.py  # SQLite storage implementation
│   ├── storage_factory.py # Factory for creating storage instances
│   ├── operations.py   # Book collection operations
│   ├── openlibrary_service.py  # Open Library API integration
│   └── utils.py        # Utility functions
├── streamlit_example/  # Streamlit web interfaces
│   ├── app.py          # Basic example app
│   └── openlibrary_app.py  # Advanced app with Open Library integration
├── examples/           # Example scripts demonstrating usage
├── tests/              # Unit tests
└── docs/               # Documentation
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone [repository-url]

# Navigate to the project directory
cd tool-booksense

# Activate the virtual environment
source toolvenv/bin/activate  # On Unix/Mac
toolvenv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the basic Streamlit example
cd streamlit_example
streamlit run app.py

# Run the advanced Streamlit example with Open Library integration
cd streamlit_example
streamlit run openlibrary_app.py
```

## Using the Application

### Search for Books
- Use the search form in the sidebar to search by title, author, subject, or ISBN
- View search results with book covers and essential information
- Add books to your collection with one click

### Manage Your Collection
- View all books in your collection
- Update reading status (Read, Reading, To Read)
- Add ratings to books
- Remove books from your collection

### View Book Details
- See detailed information about each book
- View book covers and publication information
- Track reading progress and personal ratings

## Development Guidelines

1. Follow the modular architecture with separation of concerns
2. Write comprehensive tests for all new functionality
3. Document code with detailed docstrings and type hints
4. Keep user interfaces separate from business logic
5. Use the storage factory pattern for backend flexibility

## Team Members

- **User (Project Lead)**: Project direction and architecture decisions
- **Claude (Technical Architect)**: Core implementation and API integration
- **Goofus (Pragmatic Developer)**: Rapid prototyping and feature development
- **Gallant (Quality Specialist)**: Testing strategy and code quality

## Future Plans

Future development will include:
- Command-line interface for terminal-based management
- RESTful API for programmatic access
- Desktop GUI application
- Advanced collection analytics and visualization
- Import/export functionality

---

*This project is part of the CTS285 Fall 2022 course.*