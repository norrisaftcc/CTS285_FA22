# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository appears to be part of a "BookSense" tool project, possibly related to the CTS285 course for Fall 2022. The repository contains a Python virtual environment (`toolvenv`) but no actual application code yet.

The parent repository contains several example projects:
- ProcMan - Procedure-based design without objects (Python)
- CppMan - Similar design in C++, using structs to hold problems
- Dataman - A Python application with data, logic, UI, and main modules

## Development Environment

This is a Python project that uses a virtual environment:

```bash
# Activate the virtual environment
source toolvenv/bin/activate  # On Unix/Mac
toolvenv\Scripts\activate     # On Windows

# To deactivate the virtual environment when done
deactivate
```

## Code Structure

The project appears to be in early stages with only a virtual environment set up. Based on the parent repository examples, it may follow a similar modular design pattern:
- Data management
- Logic/business rules
- User interface
- Main application entry point

## Future Development

When developing this tool, follow these guidelines:
1. Use clear, descriptive names for functions and variables
2. Follow the modular design pattern seen in other examples
3. Keep UI code separate from business logic
4. Document functions and modules with clear docstrings