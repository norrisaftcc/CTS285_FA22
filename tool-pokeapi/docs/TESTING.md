# PokeSense Testing Guide

## Overview

PokeSense uses a comprehensive testing approach to ensure code quality and reliability. The test suite covers all critical components including data models, storage implementations, business logic, and API integration.

## Test Structure

Tests are organized by component, with separate test files for each core module:

- **test_models.py**: Tests for the Pokemon data model
- **test_storage.py**: Tests for the JSON storage implementation
- **test_operations.py**: Tests for the Pokemon collection operations
- **test_pokeapi_service.py**: Tests for the PokeAPI integration

## Running Tests

### Running All Tests

To run the complete test suite:

```bash
python run_tests.py
```

This script will:
1. Discover and run all tests in the `tests` directory
2. Generate a coverage report (if the `coverage` module is installed)
3. Create HTML coverage reports in the `coverage_html` directory

### Running Individual Test Files

To run tests for a specific component:

```bash
python -m unittest tests/test_models.py
python -m unittest tests/test_storage.py
python -m unittest tests/test_operations.py
python -m unittest tests/test_pokeapi_service.py
```

## Coverage Requirements

The project aims to maintain high test coverage:

- **Core Models**: 100% coverage
- **Storage Layer**: 95%+ coverage
- **Business Logic**: 90%+ coverage
- **API Integration**: 85%+ coverage

## Mock Strategy

The tests use strategic mocking to isolate components and avoid actual API calls:

- **Storage Tests**: Use temporary files and clean up after tests
- **API Tests**: Mock HTTP responses to simulate PokeAPI
- **Operations Tests**: Mock the storage layer to focus on business logic

## Continuous Integration

Tests should be run:
- Before committing changes
- After pulling changes from the repository
- As part of any code review process

## Writing New Tests

When adding new features:

1. Write tests before implementing the feature (TDD approach)
2. Ensure proper isolation using mocks where appropriate
3. Test both successful paths and error conditions
4. Verify edge cases and boundary conditions

## Testing UI Components

While the core functionality has automated tests, Streamlit components require manual testing:

1. Verify that UI elements display correctly
2. Test responsive behavior on different screen sizes
3. Ensure proper error handling for user inputs
4. Check that UI state changes correctly based on actions