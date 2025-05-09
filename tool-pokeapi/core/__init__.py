"""
Core module for the PokeSense application.

This package contains the core functionality of the PokeSense application,
including data models, storage implementations, and API integrations.
"""

from .models import Pokemon
from .storage import StorageInterface, JsonStorage
from .operations import PokemonCollection
from .pokeapi_service import PokeApiService

__all__ = [
    'Pokemon',
    'StorageInterface',
    'JsonStorage',
    'PokemonCollection',
    'PokeApiService'
]