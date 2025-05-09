# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

PokeSense is a comprehensive Pokémon management application built as part of the CTS285 course for Fall 2022. The project demonstrates different programming approaches and interfaces for managing Pokémon collections.

The application features:
- Core functionality for Pokémon data management
- Streamlit web interface
- PokeAPI integration for Pokémon search and metadata retrieval
- Data persistence using JSON storage

## Team Members and Contributions

This project has been developed by a team of contributors:

1. **Ash (Project Lead)**
   - Project direction and requirements
   - Architecture decisions
   - Code review and quality assurance
   - User experience design

2. **Misty (Technical Architect)**
   - Core module implementation
   - Documentation and examples
   - PokeAPI integration
   - Test framework setup

3. **Brock (Frontend Developer)**
   - Streamlit interface implementation
   - Data visualization components
   - UI/UX improvements
   - Demo preparation

4. **Serena (Quality Assurance)**
   - Comprehensive test coverage
   - Code quality improvements
   - Bug tracking and resolution
   - Performance optimizations

## Development Environment

This is a Python project that uses:

```bash
# Install dependencies
pip install -r requirements.txt
```

To run the Streamlit web interface:
```bash
cd interfaces/streamlit_app
streamlit run pokeapi_app.py
```

## Code Structure

The project follows a modular architecture with clear separation of concerns:

```
tool-pokeapi/
├── core/                 # Core functionality
│   ├── models.py         # Data models (Pokemon class)
│   ├── storage.py        # Storage interface and JSON implementation
│   ├── operations.py     # Pokemon collection operations
│   ├── pokeapi_service.py  # PokeAPI integration
│   └── __init__.py       # Package initialization
├── interfaces/
│   ├── streamlit_app/    # Streamlit web interface
│       └── pokeapi_app.py # Main streamlit application
├── examples/             # Example scripts demonstrating usage
└── tests/                # Unit tests
```

## PokeAPI Integration

The project integrates with the PokeAPI:

```python
# Search for Pokémon
results = PokeApiService.search_pokemon("pikachu")

# Get Pokémon details
details = PokeApiService.get_pokemon_details("pikachu")

# Get Pokémon sprite URL
sprite_url = pokemon.sprites.get('front_default')
```

## Development Guidelines

1. Follow the modular architecture and maintain separation of concerns
2. Document all functions and classes with clear docstrings
3. Use type hints for function parameters and return values
4. Handle errors gracefully with proper exception handling
5. Maintain backward compatibility with existing interfaces
6. Consider the UI/UX implications of any changes