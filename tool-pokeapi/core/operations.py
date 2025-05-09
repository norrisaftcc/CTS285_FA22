"""
Pokemon collection operations for the PokeSense application.

This module provides high-level operations for managing Pokemon collections.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import re

from .models import Pokemon
from .storage import StorageInterface


class PokemonCollection:
    """Manages a collection of Pokemon with various operations."""

    def __init__(self, storage: StorageInterface):
        """Initialize with a storage implementation.
        
        Args:
            storage: A storage implementation for persisting Pokemon
        """
        self.storage = storage
        self._pokemon_list = self.storage.load()
    
    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """Add a new Pokemon to the collection.
        
        Args:
            pokemon: The Pokemon to add
            
        Returns:
            bool: True if the Pokemon was added successfully, False otherwise
        """
        result = self.storage.add_pokemon(pokemon)
        if result:
            self._pokemon_list = self.storage.load()
        return result
    
    def get_pokemon(self, pokemon_id: str) -> Optional[Pokemon]:
        """Get a Pokemon by its ID.
        
        Args:
            pokemon_id: The unique identifier of the Pokemon
            
        Returns:
            Optional[Pokemon]: The Pokemon if found, None otherwise
        """
        return self.storage.get_pokemon(pokemon_id)
    
    def update_pokemon(self, pokemon: Pokemon) -> bool:
        """Update an existing Pokemon in the collection.
        
        Args:
            pokemon: The updated Pokemon data (must have the same ID as an existing Pokemon)
            
        Returns:
            bool: True if the Pokemon was updated successfully, False otherwise
        """
        result = self.storage.update_pokemon(pokemon)
        if result:
            self._pokemon_list = self.storage.load()
        return result
    
    def delete_pokemon(self, pokemon_id: str) -> bool:
        """Remove a Pokemon from the collection.
        
        Args:
            pokemon_id: The unique identifier of the Pokemon to delete
            
        Returns:
            bool: True if the Pokemon was deleted successfully, False otherwise
        """
        result = self.storage.delete_pokemon(pokemon_id)
        if result:
            self._pokemon_list = self.storage.load()
        return result
    
    def list_pokemon(self) -> List[Pokemon]:
        """Get all Pokemon in the collection.
        
        Returns:
            List[Pokemon]: All Pokemon in the collection
        """
        self._pokemon_list = self.storage.load()  # Refresh the cache
        return self._pokemon_list
    
    def search_pokemon(self, query: str) -> List[Pokemon]:
        """Search for Pokemon by name.
        
        Args:
            query: The search query
            
        Returns:
            List[Pokemon]: Pokemon matching the search criteria
        """
        self._pokemon_list = self.storage.load()  # Refresh the cache
        
        if not query:
            return self._pokemon_list
        
        query_lower = query.lower()
        results = []
        
        for pokemon in self._pokemon_list:
            # Check if the query appears in name or notes
            if (query_lower in pokemon.name.lower() or 
                query_lower in pokemon.notes.lower()):
                results.append(pokemon)
                
        return results
    
    def filter_pokemon(self, **filters) -> List[Pokemon]:
        """Filter Pokemon by various attributes.
        
        Args:
            **filters: Attribute-value pairs to filter by
            
        Returns:
            List[Pokemon]: Pokemon matching the filter criteria
        """
        self._pokemon_list = self.storage.load()  # Refresh the cache
        
        if not filters:
            return self._pokemon_list
        
        results = self._pokemon_list
        
        for attr, value in filters.items():
            if attr not in vars(Pokemon):
                continue
            
            if attr == 'types':
                if isinstance(value, list):
                    results = [p for p in results if set(value).issubset(set(p.types))]
                else:
                    results = [p for p in results if value in p.types]
            
            elif attr == 'favorite':
                results = [p for p in results if p.favorite == value]
            
            else:
                results = [p for p in results if getattr(p, attr, None) == value]
        
        return results
    
    def sort_pokemon(self, key: str, reverse: bool = False) -> List[Pokemon]:
        """Sort Pokemon by a specified attribute.
        
        Args:
            key: The attribute to sort by
            reverse: Whether to sort in descending order
            
        Returns:
            List[Pokemon]: Sorted Pokemon
        """
        self._pokemon_list = self.storage.load()  # Refresh the cache
        
        if not hasattr(Pokemon, key):
            return self._pokemon_list
        
        return sorted(self._pokemon_list, key=lambda pokemon: getattr(pokemon, key), reverse=reverse)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics about the Pokemon collection.
        
        Returns:
            Dict[str, Any]: Various statistics about the collection
        """
        self._pokemon_list = self.storage.load()  # Refresh the cache
        
        stats = {
            'total_pokemon': len(self._pokemon_list),
            'favorite_pokemon': len([p for p in self._pokemon_list if p.favorite]),
            'types': {},
            'pokemon_by_type': {}
        }
        
        # Count Pokemon by type
        for pokemon in self._pokemon_list:
            for type_name in pokemon.types:
                stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
        
        # Group Pokemon by primary type
        for pokemon in self._pokemon_list:
            if pokemon.types:  # If the Pokemon has types
                primary_type = pokemon.types[0]  # Take the first type as primary
                if primary_type not in stats['pokemon_by_type']:
                    stats['pokemon_by_type'][primary_type] = []
                stats['pokemon_by_type'][primary_type].append(pokemon.name)
        
        return stats