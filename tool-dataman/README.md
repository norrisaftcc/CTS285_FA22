# Dataman Tool Project

## Overview
Dataman is a comprehensive math problem solver and trainer application built as part of the CTS285 course for Fall 2022. The project demonstrates modern software architecture with a modular design and multiple interface options, allowing users to practice and improve their math skills.

## Revision History

| Version | Date       | Description of Changes                       | Author            |
|---------|------------|--------------------------------------------|-------------------|
| 0.1.0   | 2023-08-10 | Initial project setup with core functionality | Claude           |
| 0.2.0   | 2023-08-11 | Added storage implementations and CLI interface | Claude         |
| 0.3.0   | 2023-08-12 | Added Streamlit web interface                | Claude           |
| 0.3.1   | 2023-08-12 | Added test suite and documentation           | Claude           |

## Features

### Core Functionality
- Math problem model with validation and solving
- Multiple storage backends (JSON and SQLite)
- Complete CRUD operations for problem management
- Problem set organization and statistics
- Timed drill mode for speed practice

### User Interfaces
- Command-line interface for terminal-based operation
- Streamlit web interface with responsive design
- Problem visualization and statistics
- Interactive problem solving and feedback

### Math Operations Support
- Addition, subtraction, multiplication, and division
- Customizable difficulty levels
- Problem validation and verification
- Statistics and performance tracking

## Project Structure

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

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone [repository-url]

# Navigate to the project directory
cd tool-dataman

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Command Line Interface
```bash
# Run the CLI version
python -m dataman.interfaces.cli.dataman_cli
```

#### Streamlit Web Interface
```bash
# Run the Streamlit web interface
cd interfaces/streamlit_app
streamlit run dataman_app.py
```

## Using the Application

### Answer Checker
- Enter a math problem to check if the answer is correct
- Format: "2 + 2 = 4"
- Supported operators: +, -, *, /

### Memory Bank
- Create and manage collections of math problems
- Practice solving saved problems
- Track your progress and performance

### Problem Sets
- Organize problems into themed sets
- Generate random problem sets based on difficulty
- Import and export problem sets

### Timed Drill
- Test your speed and accuracy with timed drills
- Customize difficulty and problem types
- View performance statistics and improvements

## Development Guidelines

1. Follow the modular architecture with separation of concerns
2. Write comprehensive tests for all new functionality
3. Document code with detailed docstrings and type hints
4. Keep user interfaces separate from business logic
5. Use the storage factory pattern for backend flexibility

## Team Members

- **User (Project Lead)**: Project direction and architecture decisions
- **Claude (Technical Architect)**: Core implementation and interface development
- **Dataman Team**: Testing and quality assurance

## Future Plans

Future development will include:
- Desktop GUI application
- Advanced statistics and visualization
- Multi-user support with profiles
- More complex math operations (exponents, roots, etc.)
- Educational content and learning paths

---

*This project is part of the CTS285 Fall 2022 course.*