"""
Tests for the storage implementations.
"""

import unittest
import os
import json
from datetime import datetime
from core.models import Pokemon
from core.storage import JsonStorage


class TestJsonStorage(unittest.TestCase):
    """Test cases for the JsonStorage class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary test file
        self.test_file = "test_storage.json"
        
        # Create a JsonStorage instance
        self.storage = JsonStorage(self.test_file)
        
        # Create some test Pokemon
        self.pikachu = Pokemon(
            name="Pikachu",
            pokemon_id=25,
            types=["electric"],
            height=4,
            weight=60
        )
        
        self.charizard = Pokemon(
            name="Charizard",
            pokemon_id=6,
            types=["fire", "flying"],
            height=17,
            weight=905,
            favorite=True
        )
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Remove the test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_init_creates_file(self):
        """Test that initialization creates the storage file if it doesn't exist."""
        # Assert
        self.assertTrue(os.path.exists(self.test_file))
        
        # Verify the file contains an empty array
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data, [])
    
    def test_add_pokemon(self):
        """Test adding a Pokemon to storage."""
        # Act
        result = self.storage.add_pokemon(self.pikachu)
        
        # Assert
        self.assertTrue(result)
        
        # Verify Pokemon was saved to file
        pokemon_list = self.storage.load()
        self.assertEqual(len(pokemon_list), 1)
        self.assertEqual(pokemon_list[0].name, "Pikachu")
    
    def test_add_duplicate_pokemon(self):
        """Test adding a duplicate Pokemon returns False."""
        # Arrange
        self.storage.add_pokemon(self.pikachu)
        duplicate = Pokemon(
            name="Pikachu Clone",
            pokemon_id=25,
            id=self.pikachu.id  # Same ID as pikachu
        )
        
        # Act
        result = self.storage.add_pokemon(duplicate)
        
        # Assert
        self.assertFalse(result)
        
        # Verify no duplicate was added
        pokemon_list = self.storage.load()
        self.assertEqual(len(pokemon_list), 1)
    
    def test_get_pokemon(self):
        """Test getting a Pokemon by ID."""
        # Arrange
        self.storage.add_pokemon(self.pikachu)
        self.storage.add_pokemon(self.charizard)
        
        # Act
        result = self.storage.get_pokemon(self.charizard.id)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Charizard")
        self.assertEqual(result.pokemon_id, 6)
    
    def test_get_nonexistent_pokemon(self):
        """Test getting a Pokemon with non-existent ID returns None."""
        # Arrange
        self.storage.add_pokemon(self.pikachu)
        
        # Act
        result = self.storage.get_pokemon("non-existent-id")
        
        # Assert
        self.assertIsNone(result)
    
    def test_update_pokemon(self):
        """Test updating an existing Pokemon."""
        # Arrange
        self.storage.add_pokemon(self.pikachu)
        
        # Modify the Pokemon
        self.pikachu.favorite = True
        self.pikachu.notes = "My first Pokemon"
        
        # Act
        result = self.storage.update_pokemon(self.pikachu)
        
        # Assert
        self.assertTrue(result)
        
        # Verify Pokemon was updated
        updated = self.storage.get_pokemon(self.pikachu.id)
        self.assertTrue(updated.favorite)
        self.assertEqual(updated.notes, "My first Pokemon")
    
    def test_update_nonexistent_pokemon(self):
        """Test updating a Pokemon with non-existent ID returns False."""
        # Act
        result = self.storage.update_pokemon(self.pikachu)
        
        # Assert
        self.assertFalse(result)
    
    def test_delete_pokemon(self):
        """Test deleting a Pokemon by ID."""
        # Arrange
        self.storage.add_pokemon(self.pikachu)
        self.storage.add_pokemon(self.charizard)
        
        # Act
        result = self.storage.delete_pokemon(self.pikachu.id)
        
        # Assert
        self.assertTrue(result)
        
        # Verify Pokemon was deleted
        pokemon_list = self.storage.load()
        self.assertEqual(len(pokemon_list), 1)
        self.assertEqual(pokemon_list[0].name, "Charizard")
    
    def test_delete_nonexistent_pokemon(self):
        """Test deleting a Pokemon with non-existent ID returns False."""
        # Act
        result = self.storage.delete_pokemon("non-existent-id")
        
        # Assert
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()