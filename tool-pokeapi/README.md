# PokeSense

A comprehensive Pokémon management application that demonstrates integration with the PokeAPI.

## Project Overview

PokeSense helps Pokémon researchers and enthusiasts search, collect, and analyze Pokémon data through an intuitive interface. Built for Professor Oak's Pokémon Research Lab, this application demonstrates a clean separation between GUI, business logic, and data layers.

## Features

- Search for Pokémon by name and type
- View detailed Pokémon information (stats, types, abilities, etc.)
- Add Pokémon to your personal collection
- Mark favorites and add personal notes
- Display type-based statistics and analysis

## Project Structure

The project follows a three-tier architecture:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│     GUI     │ ↔  │    Logic    │ ↔  │    Data     │
│  (Streamlit)│    │   (Core)    │    │  (Storage)  │
└─────────────┘    └─────────────┘    └─────────────┘
```

Directory structure:

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
├── docs/                 # Documentation
│   ├── presentation/     # Presentation materials
│   └── TODO.md           # Development roadmap
└── tests/                # Unit tests
```

## Team Members and Responsibilities

- **Ash (Project Lead)** - Architecture, integration, and project oversight
- **Misty (Technical Architect)** - Business logic and PokeAPI integration
- **Brock (Frontend Developer)** - UI design and Streamlit implementation
- **Serena (Quality Assurance)** - Data layer and testing

## Installation

1. Clone the repository
2. Install requirements:

```bash
pip install -r requirements.txt
```

## Usage

To run the Streamlit web interface:

```bash
cd interfaces/streamlit_app
streamlit run pokeapi_app.py
```

## Development

The team uses a round-robin development approach to ensure all members gain experience across the full stack. See `docs/presentation/TASK_ASSIGNMENTS.md` for details on our workflow and current task assignments.

### API Testing

The application connects to the [PokeAPI](https://pokeapi.co/) to retrieve Pokémon data. Our service layer handles:

- HTTP requests with proper error handling
- Response parsing and data transformation
- Caching to minimize API calls
- Conversion between API data and our internal models

### Data Format

PokeSense uses JSON for data storage with a schema that extends the PokeAPI format to include collection-specific fields like favorites and notes. Example:

```json
{
  "pokemon": [
    {
      "id": "uuid-string",
      "name": "pikachu",
      "pokemon_id": 25,
      "types": ["electric"],
      "sprites": { "front_default": "url-to-sprite" },
      "favorite": true,
      "notes": "First Pokemon caught"
    }
  ]
}
```

## Upcoming Features

See our [TODO list](docs/TODO.md) for planned features and enhancements.

## Credits

- [PokeAPI](https://pokeapi.co/) - The RESTful Pokémon API used in this project
- Built as part of CTS285 Fall 2022

---

> "Understanding Pokémon is the work of a lifetime. The better our tools, the deeper our understanding can grow." — Professor Oak