"""
Tests for the Pokemon data model.
"""

import unittest
from datetime import datetime
from core.models import Pokemon


class TestPokemonModel(unittest.TestCase):
    """Test cases for the Pokemon model class."""

    def test_pokemon_creation(self):
        """Test creating a valid Pokemon instance."""
        # Arrange
        name = "Pikachu"
        pokemon_id = 25
        types = ["electric"]
        
        # Act
        pokemon = Pokemon(name=name, pokemon_id=pokemon_id, types=types)
        
        # Assert
        self.assertEqual(pokemon.name, name)
        self.assertEqual(pokemon.pokemon_id, pokemon_id)
        self.assertEqual(pokemon.types, types)
        self.assertFalse(pokemon.favorite)
        self.assertEqual(pokemon.notes, "")
        self.assertIsNotNone(pokemon.id)
        self.assertIsInstance(pokemon.date_added, datetime)

    def test_string_pokemon_id_conversion(self):
        """Test that string pokemon_id is converted to integer."""
        # Arrange & Act
        pokemon = Pokemon(name="Bulbasaur", pokemon_id="1")
        
        # Assert
        self.assertEqual(pokemon.pokemon_id, 1)
        self.assertIsInstance(pokemon.pokemon_id, int)

    def test_invalid_name(self):
        """Test that empty name raises ValueError."""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            Pokemon(name="", pokemon_id=25)

    def test_invalid_pokemon_id(self):
        """Test that non-convertible pokemon_id raises ValueError."""
        # Arrange & Act & Assert
        with self.assertRaises(ValueError):
            Pokemon(name="Pikachu", pokemon_id="not_a_number")

    def test_to_dict(self):
        """Test conversion to dictionary."""
        # Arrange
        pokemon = Pokemon(
            name="Charizard",
            pokemon_id=6,
            types=["fire", "flying"],
            height=17,
            weight=905,
            favorite=True,
            notes="My starter Pokemon"
        )
        
        # Act
        pokemon_dict = pokemon.to_dict()
        
        # Assert
        self.assertEqual(pokemon_dict["name"], "Charizard")
        self.assertEqual(pokemon_dict["pokemon_id"], 6)
        self.assertEqual(pokemon_dict["types"], ["fire", "flying"])
        self.assertEqual(pokemon_dict["height"], 17)
        self.assertEqual(pokemon_dict["weight"], 905)
        self.assertTrue(pokemon_dict["favorite"])
        self.assertEqual(pokemon_dict["notes"], "My starter Pokemon")
        self.assertEqual(pokemon_dict["id"], pokemon.id)

    def test_from_dict(self):
        """Test creation from dictionary."""
        # Arrange
        data = {
            "name": "Squirtle",
            "pokemon_id": 7,
            "types": ["water"],
            "height": 5,
            "weight": 90,
            "favorite": True,
            "notes": "Water starter",
            "id": "test-id-123",
            "date_added": "2022-09-15T14:30:45"
        }
        
        # Act
        pokemon = Pokemon.from_dict(data)
        
        # Assert
        self.assertEqual(pokemon.name, "Squirtle")
        self.assertEqual(pokemon.pokemon_id, 7)
        self.assertEqual(pokemon.types, ["water"])
        self.assertEqual(pokemon.height, 5)
        self.assertEqual(pokemon.weight, 90)
        self.assertTrue(pokemon.favorite)
        self.assertEqual(pokemon.notes, "Water starter")
        self.assertEqual(pokemon.id, "test-id-123")
        self.assertEqual(pokemon.date_added.year, 2022)
        self.assertEqual(pokemon.date_added.month, 9)
        self.assertEqual(pokemon.date_added.day, 15)


if __name__ == "__main__":
    unittest.main()