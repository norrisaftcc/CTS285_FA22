"""
Tests for the PokeAPI service integration.
"""

import unittest
from unittest.mock import patch, Mock
import json
import os
import requests
from core.pokeapi_service import PokeApiService
from core.models import Pokemon


class TestPokeApiService(unittest.TestCase):
    """Test cases for the PokeApiService class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Clear the cache before each test
        PokeApiService._cache = {}
        PokeApiService._cache_expiry = {}
        
        # Load mock response data
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        # Create fixtures directory if it doesn't exist
        if not os.path.exists(self.fixtures_dir):
            os.makedirs(self.fixtures_dir)
    
    def test_search_pokemon(self):
        """Test searching for Pokemon by name."""
        # Arrange
        mock_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
                {"name": "pikachu-gmax", "url": "https://pokeapi.co/api/v2/pokemon/10080/"}
            ]
        }
        
        # Mock the list_pokemon method
        with patch.object(PokeApiService, 'list_pokemon', return_value={
            "count": 1000,
            "pokemon": [
                {"name": "pikachu", "url": "https://pokeapi.co/api/v2/pokemon/25/"},
                {"name": "pikachu-gmax", "url": "https://pokeapi.co/api/v2/pokemon/10080/"},
                {"name": "charizard", "url": "https://pokeapi.co/api/v2/pokemon/6/"}
            ]
        }) as mock_method:
            # Act
            result = PokeApiService.search_pokemon("pika")
            
            # Assert
            self.assertEqual(result["count"], 2)
            self.assertEqual(len(result["pokemon"]), 2)
            self.assertEqual(result["pokemon"][0]["name"], "pikachu")
            self.assertEqual(result["pokemon"][1]["name"], "pikachu-gmax")
    
    @patch('requests.get')
    def test_get_pokemon_details(self, mock_get):
        """Test getting detailed information about a Pokemon."""
        # Arrange
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "types": [
                {"slot": 1, "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}}
            ],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png",
                "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png",
                "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/25.png",
                "other": {
                    "official-artwork": {
                        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
                    }
                }
            },
            "abilities": [
                {"ability": {"name": "static", "url": "https://pokeapi.co/api/v2/ability/9/"}},
                {"ability": {"name": "lightning-rod", "url": "https://pokeapi.co/api/v2/ability/31/"}}
            ],
            "stats": [
                {"base_stat": 35, "stat": {"name": "hp"}},
                {"base_stat": 55, "stat": {"name": "attack"}}
            ],
            "moves": [
                {"move": {"name": "mega-punch", "url": "https://pokeapi.co/api/v2/move/5/"}}
            ]
        }
        mock_get.return_value = mock_response
        
        # Act
        result = PokeApiService.get_pokemon_details("pikachu")
        
        # Assert
        mock_get.assert_called_once()
        self.assertEqual(result["id"], 25)
        self.assertEqual(result["name"], "pikachu")
        self.assertEqual(result["types"][0]["type"]["name"], "electric")
    
    def test_extract_pokemon_info(self):
        """Test extracting Pokemon information from API data."""
        # Arrange
        pokemon_data = {
            "id": 6,
            "name": "charizard",
            "height": 17,
            "weight": 905,
            "types": [
                {"slot": 1, "type": {"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"}},
                {"slot": 2, "type": {"name": "flying", "url": "https://pokeapi.co/api/v2/type/3/"}}
            ],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
                "other": {
                    "official-artwork": {
                        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png"
                    }
                }
            },
            "abilities": [
                {"ability": {"name": "blaze", "url": "https://pokeapi.co/api/v2/ability/66/"}},
                {"ability": {"name": "solar-power", "url": "https://pokeapi.co/api/v2/ability/94/"}}
            ],
            "stats": [
                {"base_stat": 78, "stat": {"name": "hp"}},
                {"base_stat": 84, "stat": {"name": "attack"}}
            ],
            "moves": [
                {"move": {"name": "mega-punch", "url": "https://pokeapi.co/api/v2/move/5/"}},
                {"move": {"name": "fire-punch", "url": "https://pokeapi.co/api/v2/move/7/"}}
            ],
            "base_experience": 240
        }
        
        # Act
        info = PokeApiService.extract_pokemon_info(pokemon_data)
        
        # Assert
        self.assertEqual(info["id"], 6)
        self.assertEqual(info["name"], "charizard")
        self.assertEqual(info["height"], 17)
        self.assertEqual(info["weight"], 905)
        self.assertEqual(info["types"], ["fire", "flying"])
        self.assertEqual(info["abilities"], ["blaze", "solar-power"])
        self.assertEqual(len(info["stats"]), 2)
        self.assertEqual(info["stats"][0]["name"], "hp")
        self.assertEqual(info["stats"][0]["base_value"], 78)
        self.assertEqual(info["moves"], ["mega-punch", "fire-punch"])
        self.assertEqual(info["sprites"]["front_default"], "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png")
        self.assertEqual(info["sprites"]["official_artwork"], "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png")
    
    def test_extract_pokemon_info_empty(self):
        """Test extracting information from empty data returns empty dict."""
        # Act
        info = PokeApiService.extract_pokemon_info({})
        
        # Assert
        self.assertEqual(info, {})
    
    def test_create_pokemon_from_api_data(self):
        """Test creating a Pokemon object from API data."""
        # Arrange
        pokemon_data = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "types": [
                {"slot": 1, "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}}
            ],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                "other": {
                    "official-artwork": {
                        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
                    }
                }
            },
            "abilities": [
                {"ability": {"name": "static", "url": "https://pokeapi.co/api/v2/ability/9/"}},
                {"ability": {"name": "lightning-rod", "url": "https://pokeapi.co/api/v2/ability/31/"}}
            ],
            "stats": [
                {"base_stat": 35, "stat": {"name": "hp"}},
                {"base_stat": 55, "stat": {"name": "attack"}}
            ],
            "moves": [
                {"move": {"name": "mega-punch", "url": "https://pokeapi.co/api/v2/move/5/"}}
            ]
        }
        
        # Act
        pokemon = PokeApiService.create_pokemon_from_api_data(pokemon_data)
        
        # Assert
        self.assertIsInstance(pokemon, Pokemon)
        self.assertEqual(pokemon.name, "pikachu")
        self.assertEqual(pokemon.pokemon_id, 25)
        self.assertEqual(pokemon.types, ["electric"])
        self.assertEqual(pokemon.height, 4)
        self.assertEqual(pokemon.weight, 60)
        self.assertEqual(pokemon.abilities, ["static", "lightning-rod"])
        self.assertEqual(len(pokemon.stats), 2)
        self.assertEqual(pokemon.stats[0]["name"], "hp")
        self.assertEqual(pokemon.moves, ["mega-punch"])
        self.assertFalse(pokemon.favorite)
        self.assertEqual(pokemon.notes, "")
        self.assertIsNotNone(pokemon.id)


if __name__ == "__main__":
    unittest.main()