# BookSense Streamlit Example

## Overview
A simple Streamlit application example for the BookSense tool project that demonstrates how to create a web-based interface for managing book data.

## Revision History

| Version | Date       | Description of Changes                  | Author        |
|---------|------------|----------------------------------------|---------------|
| 0.1.0   | 2023-05-09 | Initial implementation                  | Claude        |

## Release Notes

### Version 0.1.0 (Latest)
- Created basic Streamlit interface for book management
- Implemented sample book database display
- Added filtering by publication year
- Implemented book rating visualization
- Added demo form for adding new books (non-functional)
- Known issues: Data is not persistent, books added through the form are not saved

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions
```bash
# Install required packages
pip install -r requirements.txt
```

## Usage

### Running the Application
Navigate to this directory and run:

```bash
streamlit run app.py
```

This will start the Streamlit server and automatically open the application in your default web browser.

### Features
- **Book Database Display**: View a sample collection of books with their titles, authors, publication years, and ratings
- **Filtering**: Use the sidebar slider to filter books by publication year
- **Visualization**: View book ratings in a bar chart format
- **Book Addition Form**: Demo form to simulate adding new books

## Dependencies
- Streamlit (>= 1.12.0) - Web application framework
- Pandas (>= 1.4.0) - Data manipulation and analysis
- NumPy (>= 1.22.0) - Numerical computing support

## Integration with BookSense
This example demonstrates how a web-based interface could be created for the BookSense tool. It follows the same pattern as other examples in the repository:
- Data representation (using pandas DataFrame)
- Logic (filtering and processing)
- User interface (Streamlit components)

In a full implementation, this could be extended to:
- Read/write from a real database
- Implement more complex book management features
- Connect with other BookSense tools

## Troubleshooting
| Issue                           | Solution                                   |
|---------------------------------|--------------------------------------------|
| Streamlit fails to start        | Check Python version and package installation |
| Charts not displaying correctly | Ensure pandas and numpy are properly installed |

---

*This project is part of the CTS285 Fall 2022 course.*