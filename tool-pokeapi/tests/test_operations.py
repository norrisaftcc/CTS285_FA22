"""
Tests for Pokemon collection operations.
"""

import unittest
from unittest.mock import MagicMock, patch
from core.models import Pokemon
from core.operations import PokemonCollection


class TestPokemonCollection(unittest.TestCase):
    """Test cases for the PokemonCollection class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock storage
        self.mock_storage = MagicMock()
        
        # Create a PokemonCollection with the mock storage
        self.collection = PokemonCollection(self.mock_storage)
        
        # Create some test Pokemon
        self.pikachu = Pokemon(
            name="Pikachu",
            pokemon_id=25,
            types=["electric"]
        )
        
        self.charizard = Pokemon(
            name="Charizard",
            pokemon_id=6,
            types=["fire", "flying"],
            favorite=True
        )
        
        self.bulbasaur = Pokemon(
            name="Bulbasaur",
            pokemon_id=1,
            types=["grass", "poison"]
        )
        
        # Set up mock storage responses
        self.mock_storage.load.return_value = [self.pikachu, self.charizard, self.bulbasaur]
    
    def test_list_pokemon(self):
        """Test listing all Pokemon in the collection."""
        # Act
        result = self.collection.list_pokemon()
        
        # Assert
        self.assertEqual(len(result), 3)
        self.mock_storage.load.assert_called_once()
    
    def test_add_pokemon(self):
        """Test adding a Pokemon to the collection."""
        # Arrange
        self.mock_storage.add_pokemon.return_value = True
        new_pokemon = Pokemon(
            name="Squirtle",
            pokemon_id=7,
            types=["water"]
        )
        
        # Act
        result = self.collection.add_pokemon(new_pokemon)
        
        # Assert
        self.assertTrue(result)
        self.mock_storage.add_pokemon.assert_called_once_with(new_pokemon)
        self.mock_storage.load.assert_called()
    
    def test_get_pokemon(self):
        """Test getting a Pokemon by ID."""
        # Arrange
        pokemon_id = "test-id"
        self.mock_storage.get_pokemon.return_value = self.pikachu
        
        # Act
        result = self.collection.get_pokemon(pokemon_id)
        
        # Assert
        self.assertEqual(result, self.pikachu)
        self.mock_storage.get_pokemon.assert_called_once_with(pokemon_id)
    
    def test_update_pokemon(self):
        """Test updating a Pokemon in the collection."""
        # Arrange
        self.mock_storage.update_pokemon.return_value = True
        
        # Modify the Pokemon
        self.pikachu.favorite = True
        
        # Act
        result = self.collection.update_pokemon(self.pikachu)
        
        # Assert
        self.assertTrue(result)
        self.mock_storage.update_pokemon.assert_called_once_with(self.pikachu)
        self.mock_storage.load.assert_called()
    
    def test_delete_pokemon(self):
        """Test deleting a Pokemon from the collection."""
        # Arrange
        pokemon_id = "test-id"
        self.mock_storage.delete_pokemon.return_value = True
        
        # Act
        result = self.collection.delete_pokemon(pokemon_id)
        
        # Assert
        self.assertTrue(result)
        self.mock_storage.delete_pokemon.assert_called_once_with(pokemon_id)
        self.mock_storage.load.assert_called()
    
    def test_search_pokemon(self):
        """Test searching for Pokemon by name."""
        # Act
        result = self.collection.search_pokemon("char")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Charizard")
    
    def test_search_pokemon_case_insensitive(self):
        """Test that search is case-insensitive."""
        # Act
        result = self.collection.search_pokemon("PIKA")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Pikachu")
    
    def test_search_pokemon_notes(self):
        """Test searching in notes field."""
        # Arrange
        self.pikachu.notes = "This is my starter Pokemon"
        
        # Act
        result = self.collection.search_pokemon("starter")
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Pikachu")
    
    def test_search_pokemon_empty_query(self):
        """Test searching with empty query returns all Pokemon."""
        # Act
        result = self.collection.search_pokemon("")
        
        # Assert
        self.assertEqual(len(result), 3)
    
    def test_filter_pokemon_by_type(self):
        """Test filtering Pokemon by type."""
        # Act
        result = self.collection.filter_pokemon(types=["fire"])
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Charizard")
    
    def test_filter_pokemon_by_favorite(self):
        """Test filtering Pokemon by favorite status."""
        # Act
        result = self.collection.filter_pokemon(favorite=True)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Charizard")
    
    def test_filter_pokemon_no_filters(self):
        """Test filtering with no filters returns all Pokemon."""
        # Act
        result = self.collection.filter_pokemon()
        
        # Assert
        self.assertEqual(len(result), 3)
    
    def test_sort_pokemon_by_name(self):
        """Test sorting Pokemon by name."""
        # Act
        result = self.collection.sort_pokemon("name")
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "Bulbasaur")
        self.assertEqual(result[1].name, "Charizard")
        self.assertEqual(result[2].name, "Pikachu")
    
    def test_sort_pokemon_by_id(self):
        """Test sorting Pokemon by Pokemon ID."""
        # Act
        result = self.collection.sort_pokemon("pokemon_id")
        
        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].pokemon_id, 1)  # Bulbasaur
        self.assertEqual(result[1].pokemon_id, 6)  # Charizard
        self.assertEqual(result[2].pokemon_id, 25)  # Pikachu
    
    def test_get_statistics(self):
        """Test getting collection statistics."""
        # Act
        stats = self.collection.get_statistics()
        
        # Assert
        self.assertEqual(stats['total_pokemon'], 3)
        self.assertEqual(stats['favorite_pokemon'], 1)
        
        # Check type counts
        self.assertEqual(stats['types']['electric'], 1)
        self.assertEqual(stats['types']['fire'], 1)
        self.assertEqual(stats['types']['flying'], 1)
        self.assertEqual(stats['types']['grass'], 1)
        self.assertEqual(stats['types']['poison'], 1)


if __name__ == "__main__":
    unittest.main()