"""
Data models for the PokeSense application.

This module defines the core data structures used throughout the application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from uuid import uuid4


@dataclass
class Pokemon:
    """
    Represents a Pokemon in the collection.
    
    Attributes:
        id: Unique identifier for the collection entry
        name: Name of the Pokemon
        pokemon_id: PokeAPI ID of the Pokemon
        types: List of Pokemon types
        sprites: Dict containing image URLs
        height: Height of the Pokemon
        weight: Weight of the Pokemon
        stats: List of stats (hp, attack, defense, etc.)
        abilities: List of abilities
        moves: List of moves
        favorite: Whether the Pokemon is marked as favorite
        notes: User notes about the Pokemon
        date_added: When the Pokemon was added to the collection
    """
    name: str
    pokemon_id: int
    types: List[str] = field(default_factory=list)
    sprites: Dict[str, str] = field(default_factory=dict)
    height: int = 0
    weight: int = 0
    stats: List[Dict[str, any]] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    moves: List[str] = field(default_factory=list)
    favorite: bool = False
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    date_added: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate Pokemon data after initialization."""
        if not self.name:
            raise ValueError("Pokemon name cannot be empty")
        
        if not isinstance(self.pokemon_id, int):
            try:
                self.pokemon_id = int(self.pokemon_id)
            except (ValueError, TypeError):
                raise ValueError("Pokemon ID must be a valid integer")
                
        if not isinstance(self.favorite, bool):
            self.favorite = bool(self.favorite)
    
    def to_dict(self) -> dict:
        """Convert the Pokemon to a dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "pokemon_id": self.pokemon_id,
            "types": self.types,
            "sprites": self.sprites,
            "height": self.height,
            "weight": self.weight,
            "stats": self.stats,
            "abilities": self.abilities,
            "moves": self.moves,
            "favorite": self.favorite,
            "notes": self.notes,
            "date_added": self.date_added.isoformat() if hasattr(self.date_added, 'isoformat') else self.date_added
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Pokemon':
        """Create a Pokemon from a dictionary representation."""
        # Handle date conversion
        if 'date_added' in data and isinstance(data['date_added'], str):
            try:
                data['date_added'] = datetime.fromisoformat(data['date_added'])
            except ValueError:
                data['date_added'] = datetime.now()
        
        # Create a new Pokemon instance with the data
        return cls(**data)