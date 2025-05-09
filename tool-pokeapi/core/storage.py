"""
Storage implementations for the PokeSense application.

This module provides various backends for storing and retrieving Pokemon data.
"""

import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Union

from .models import Pokemon


class StorageInterface(ABC):
    """Abstract base class for storage implementations."""

    @abstractmethod
    def load(self) -> List[Pokemon]:
        """Load Pokemon from storage."""
        pass

    @abstractmethod
    def save(self, pokemon_list: List[Pokemon]) -> bool:
        """Save Pokemon to storage."""
        pass

    @abstractmethod
    def get_pokemon(self, pokemon_id: str) -> Optional[Pokemon]:
        """Get a specific Pokemon by ID."""
        pass

    @abstractmethod
    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """Add a new Pokemon to storage."""
        pass

    @abstractmethod
    def update_pokemon(self, pokemon: Pokemon) -> bool:
        """Update an existing Pokemon."""
        pass

    @abstractmethod
    def delete_pokemon(self, pokemon_id: str) -> bool:
        """Delete a Pokemon by ID."""
        pass


class JsonStorage(StorageInterface):
    """JSON file-based storage implementation."""

    def __init__(self, file_path: str):
        """Initialize with the path to the JSON file.
        
        Args:
            file_path: Path to the JSON file for Pokemon storage
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the storage file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            # Create the directory if it doesn't exist
            directory = os.path.dirname(self.file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Create an empty Pokemon list
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def load(self) -> List[Pokemon]:
        """Load Pokemon from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                pokemon_data = json.load(f)
                return [Pokemon.from_dict(data) for data in pokemon_data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading Pokemon: {e}")
            return []

    def save(self, pokemon_list: List[Pokemon]) -> bool:
        """Save Pokemon to the JSON file."""
        try:
            pokemon_data = [pokemon.to_dict() for pokemon in pokemon_list]
            
            # Use a temporary file to prevent data corruption
            temp_file = f"{self.file_path}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(pokemon_data, f, indent=2)
            
            # Replace the original file with the temporary file
            os.replace(temp_file, self.file_path)
            return True
        except Exception as e:
            print(f"Error saving Pokemon: {e}")
            return False

    def get_pokemon(self, pokemon_id: str) -> Optional[Pokemon]:
        """Get a specific Pokemon by ID."""
        pokemon_list = self.load()
        for pokemon in pokemon_list:
            if pokemon.id == pokemon_id:
                return pokemon
        return None

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """Add a new Pokemon to storage."""
        pokemon_list = self.load()
        
        # Check if a Pokemon with this ID already exists
        if any(p.id == pokemon.id for p in pokemon_list):
            return False
        
        pokemon_list.append(pokemon)
        return self.save(pokemon_list)

    def update_pokemon(self, pokemon: Pokemon) -> bool:
        """Update an existing Pokemon."""
        pokemon_list = self.load()
        
        # Find the index of the Pokemon with matching ID
        for i, p in enumerate(pokemon_list):
            if p.id == pokemon.id:
                pokemon_list[i] = pokemon
                return self.save(pokemon_list)
        
        return False  # Pokemon not found

    def delete_pokemon(self, pokemon_id: str) -> bool:
        """Delete a Pokemon by ID."""
        pokemon_list = self.load()
        initial_count = len(pokemon_list)
        
        # Filter out the Pokemon with the specified ID
        pokemon_list = [pokemon for pokemon in pokemon_list if pokemon.id != pokemon_id]
        
        if len(pokemon_list) < initial_count:
            return self.save(pokemon_list)
        
        return False  # Pokemon not found