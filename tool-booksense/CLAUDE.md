# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BookSense is a comprehensive book management application built as part of the CTS285 course for Fall 2022. The project demonstrates different programming approaches and interfaces for managing book collections.

The application features:
- Core functionality for book data management
- Multiple user interfaces (Streamlit web app, CLI, API, GUI)
- Open Library API integration for book search and metadata retrieval
- Data persistence using JSON and SQLite storage backends

## Development Environment

This is a Python project that uses a virtual environment:

```bash
# Activate the virtual environment
source toolvenv/bin/activate  # On Unix/Mac
toolvenv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# To deactivate the virtual environment when done
deactivate
```

To run the Streamlit web interface:
```bash
cd streamlit_example
streamlit run app.py  # Basic example
streamlit run openlibrary_app.py  # Advanced example with Open Library integration
```

## Code Structure

The project follows a modular architecture with clear separation of concerns:

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
├── interfaces/
│   ├── streamlit_app/  # Streamlit web interface
│   ├── cli/            # Command-line interface
│   ├── gui/            # Desktop GUI application
│   └── api/            # REST API implementation
├── examples/           # Example scripts demonstrating usage
├── tests/              # Unit tests
└── docs/               # Documentation
```

## Running Tests

The project includes comprehensive unit tests. To run them:

```bash
# Run all tests with coverage report
python run_tests.py

# Run a specific test file
python -m unittest tests/test_models.py
```

## Team Members and Contributions

This project has been developed by a team of contributors:

1. **User (Project Lead)**
   - Project direction and requirements
   - Architecture decisions
   - Code review and quality assurance

2. **Claude (Technical Architect)**
   - Core module implementation
   - Documentation and examples
   - Open Library API integration
   - Test framework setup

3. **Goofus (Pragmatic Developer)**
   - Rapid prototyping and testing
   - Feature suggestions and implementations
   - Prioritization of user-facing features

4. **Gallant (Quality Specialist)**
   - Comprehensive test coverage
   - Code quality improvements
   - Best practices enforcement
   - Documentation quality

## Open Library API Integration

The project integrates with the Open Library API:

```python
# Search for books
results = OpenLibraryService.search_books("The Great Gatsby", search_type="title")

# Get book details
details = OpenLibraryService.get_book_details(work_id)

# Get cover image URL
cover_url = OpenLibraryService.get_cover_url(isbn, "isbn", "M")
```

## Development Guidelines

1. Follow the modular architecture and maintain separation of concerns
2. Write comprehensive unit tests for all new functionality
3. Document all functions and classes with clear docstrings
4. Use type hints for function parameters and return values
5. Handle errors gracefully with proper exception handling
6. Maintain backward compatibility with existing interfaces
7. Consider performance implications for large book collections