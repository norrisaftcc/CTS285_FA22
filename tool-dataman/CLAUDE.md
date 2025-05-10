# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dataman is a comprehensive math problem solver and trainer application built as part of the CTS285 course for Fall 2022. The project demonstrates different programming approaches and interfaces for managing math problems and practicing arithmetic skills.

The application features:
- Core functionality for math problem data management
- Multiple user interfaces (CLI, Streamlit web app)
- Data persistence using JSON and SQLite storage backends
- Problem validation and solution checking
- Timed drills and performance statistics

## Development Environment

This is a Python project that uses the following structure:

```
tool-dataman/
├── core/               # Core functionality
│   ├── models.py       # Data models (Problem, ProblemSet classes)
│   ├── storage.py      # Storage interface and JSON implementation
│   ├── storage_sqlite.py  # SQLite storage implementation
│   ├── storage_factory.py # Factory for creating storage instances
│   ├── operations.py   # Problem set operations and business logic
│   └── utils.py        # Utility functions
├── interfaces/
│   ├── cli/            # Command-line interface
│   │   └── dataman_cli.py  # CLI implementation
│   └── streamlit_app/  # Streamlit web interface
│       └── dataman_app.py  # Streamlit app implementation
├── examples/           # Example scripts demonstrating usage
├── tests/              # Unit tests
└── docs/               # Documentation
```

To set up the development environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests
```

To run the application:

```bash
# Run the CLI version
python -m dataman.interfaces.cli.dataman_cli

# Run the Streamlit web interface
cd interfaces/streamlit_app
streamlit run dataman_app.py
```

## Code Structure

The project follows a modular architecture with clear separation of concerns:

1. **Core Modules**
   - `models.py`: Defines the data models (Problem and ProblemSet classes)
   - `storage.py`: Defines the storage interface and JSON implementation
   - `storage_sqlite.py`: SQLite storage implementation
   - `storage_factory.py`: Factory for creating storage instances
   - `operations.py`: Business logic for problem management
   - `utils.py`: Utility functions

2. **User Interfaces**
   - CLI: Command-line interface in `interfaces/cli/dataman_cli.py`
   - Web: Streamlit web interface in `interfaces/streamlit_app/dataman_app.py`

3. **Tests**
   - Unit tests for all core functionality

## Running Tests

The project includes comprehensive unit tests. To run them:

```bash
# Run all tests
python -m unittest discover tests

# Run a specific test file
python -m unittest tests/test_models.py
```

## Key Concepts

1. **Problem Class**
   - Represents a math problem with first operand, operator, second operand, and answer
   - Supports addition, subtraction, multiplication, and division
   - Provides methods for checking answers and formatting

2. **ProblemSet Class**
   - Represents a collection of related math problems
   - Supports adding, removing, and iterating over problems
   - Includes metadata like name and description

3. **Storage Interface**
   - Abstract interface for data persistence
   - Implementations for JSON and SQLite storage
   - Factory pattern for creating appropriate storage instances

4. **Operations**
   - Business logic for managing problem sets
   - Methods for creating, loading, and saving problem sets
   - Statistics and performance tracking

## Development Guidelines

1. Follow the modular architecture and maintain separation of concerns
2. Write comprehensive unit tests for all new functionality
3. Document all functions and classes with clear docstrings
4. Use type hints for function parameters and return values
5. Handle errors gracefully with proper exception handling
6. Maintain backward compatibility with existing interfaces
7. Consider performance implications for large problem sets

## Common Tasks

Here are examples of common tasks you might need to perform:

```python
# Create a problem
from dataman.core.models import Problem
problem = Problem(2, "+", 2)  # 2 + 2 = 4

# Check an answer
is_correct = problem.check_answer(4)  # True

# Create a problem set
from dataman.core.models import ProblemSet
problem_set = ProblemSet("Addition Practice")
problem_set.add_problem(problem)

# Save to JSON storage
from dataman.core.storage import JSONStorage
storage = JSONStorage("problems.json")
storage.save_problem_set(problem_set)

# Load from storage
loaded_set = storage.load_problem_set("Addition Practice")

# Use the operations class
from dataman.core.operations import DatamanOperations
from dataman.core.storage_factory import StorageFactory

storage = StorageFactory.create_storage("json", file_path="problems.json")
operations = DatamanOperations(storage)

# Generate a random problem set
operations.generate_problem_set("Random Set", num_problems=10, difficulty="easy")

# Get statistics
stats = operations.get_statistics()
```

## Future Development

Planned future enhancements include:
1. Desktop GUI application
2. Advanced statistics and visualization
3. Multi-user support with profiles
4. More complex math operations
5. Educational content and learning paths