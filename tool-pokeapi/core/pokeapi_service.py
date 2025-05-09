"""
PokeAPI integration service for the PokeSense application.

This module provides functions to interact with the PokeAPI
for searching Pokemon, retrieving Pokemon details, and fetching sprites.
"""

import requests
import urllib.parse
from typing import Dict, List, Optional, Any, Union
import time
from datetime import datetime

from .models import Pokemon


class PokeApiService:
    """Service for interacting with the PokeAPI."""
    
    # Base URLs for the PokeAPI
    BASE_URL = "https://pokeapi.co/api/v2"
    POKEMON_URL = f"{BASE_URL}/pokemon"
    TYPE_URL = f"{BASE_URL}/type"
    ABILITY_URL = f"{BASE_URL}/ability"
    
    # Default headers for API requests
    DEFAULT_HEADERS = {
        "User-Agent": "PokeSense/1.0 (github.com/CTS285_FA22/tool-pokeapi)"
    }
    
    # Cache for API responses to avoid duplicate requests
    _cache = {}
    _cache_expiry = {}
    CACHE_DURATION = 3600  # Cache duration in seconds (1 hour)
    
    @classmethod
    def _get_cached_or_request(cls, url: str, headers: Optional[Dict] = None, 
                              params: Optional[Dict] = None) -> Dict:
        """Get data from cache or make a new request.
        
        Args:
            url: The URL to request
            headers: Request headers (optional)
            params: Query parameters (optional)
            
        Returns:
            Dict: JSON response or empty dict if error
        """
        # Create a cache key from the URL and params
        cache_key = f"{url}:{str(params)}"
        
        # Check if we have a cached response
        current_time = time.time()
        if cache_key in cls._cache and cls._cache_expiry.get(cache_key, 0) > current_time:
            return cls._cache[cache_key]
        
        # No cache or expired, make a new request
        try:
            # Merge default headers with provided headers
            request_headers = cls.DEFAULT_HEADERS.copy()
            if headers:
                request_headers.update(headers)
            
            # Make the request
            response = requests.get(url, headers=request_headers, params=params, timeout=10)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            
            # Parse JSON response
            data = response.json()
            
            # Cache the response
            cls._cache[cache_key] = data
            cls._cache_expiry[cache_key] = current_time + cls.CACHE_DURATION
            
            return data
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to the PokeAPI")
        except requests.exceptions.Timeout:
            print("Timeout Error: The request to PokeAPI timed out")
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        except ValueError:  # Includes JSONDecodeError
            print("Error: Could not decode the JSON response from PokeAPI")
        
        return {}
    
    @classmethod
    def list_pokemon(cls, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get a list of Pokemon.
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            
        Returns:
            Dict: Dictionary containing list results and metadata
        """
        # Construct the URL with parameters
        params = {
            "limit": limit,
            "offset": offset
        }
        
        # Make the request
        data = cls._get_cached_or_request(cls.POKEMON_URL, params=params)
        
        # Process the results
        if not data:
            return {"count": 0, "pokemon": []}
        
        return {
            "count": data.get("count", 0),
            "next": data.get("next"),
            "previous": data.get("previous"),
            "pokemon": data.get("results", [])
        }
    
    @classmethod
    def search_pokemon(cls, query: str) -> Dict[str, Any]:
        """Search for Pokemon by name.
        
        Args:
            query: The search query (Pokemon name)
            
        Returns:
            Dict: Dictionary containing search results
        """
        # Get list of all Pokemon (this is cached so it's efficient)
        all_pokemon = cls.list_pokemon(limit=2000)
        
        if not all_pokemon or not all_pokemon["pokemon"]:
            return {"count": 0, "pokemon": []}
        
        # Filter Pokemon by name
        query_lower = query.lower()
        filtered_pokemon = [p for p in all_pokemon["pokemon"] if query_lower in p["name"].lower()]
        
        # Sort results by relevance (exact matches first, then startswith, then contains)
        exact_matches = [p for p in filtered_pokemon if p["name"].lower() == query_lower]
        starts_with = [p for p in filtered_pokemon if p["name"].lower().startswith(query_lower) and p not in exact_matches]
        contains = [p for p in filtered_pokemon if p not in exact_matches and p not in starts_with]
        
        sorted_results = exact_matches + starts_with + contains
        
        return {
            "count": len(sorted_results),
            "pokemon": sorted_results[:20]  # Limit to 20 results
        }
    
    @classmethod
    def get_pokemon_details(cls, identifier: Union[str, int]) -> Dict[str, Any]:
        """Get detailed information about a Pokemon by its name or ID.
        
        Args:
            identifier: Pokemon name or ID
            
        Returns:
            Dict: Detailed Pokemon information
        """
        # Construct the URL
        url = f"{cls.POKEMON_URL}/{str(identifier).lower()}"
        
        # Make the request
        return cls._get_cached_or_request(url)
    
    @classmethod
    def get_pokemon_types(cls) -> List[Dict[str, Any]]:
        """Get a list of all Pokemon types.
        
        Returns:
            List: List of Pokemon types
        """
        # Make the request
        data = cls._get_cached_or_request(cls.TYPE_URL, params={"limit": 30})
        
        # Return types
        return data.get("results", [])
    
    @classmethod
    def get_pokemon_by_type(cls, type_name: str) -> List[Dict[str, Any]]:
        """Get a list of Pokemon of a specific type.
        
        Args:
            type_name: The name of the type
            
        Returns:
            List: List of Pokemon of the specified type
        """
        # Construct the URL
        url = f"{cls.TYPE_URL}/{type_name.lower()}"
        
        # Make the request
        data = cls._get_cached_or_request(url)
        
        # Return Pokemon of this type
        return data.get("pokemon", [])
    
    @classmethod
    def extract_pokemon_info(cls, pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the most useful information from a PokeAPI Pokemon result.
        
        Args:
            pokemon_data: Pokemon data from PokeAPI
            
        Returns:
            Dict: Formatted Pokemon information
        """
        if not pokemon_data:
            return {}
            
        # Extract types
        types = []
        if "types" in pokemon_data:
            types = [t["type"]["name"] for t in pokemon_data["types"]]
            
        # Extract abilities
        abilities = []
        if "abilities" in pokemon_data:
            abilities = [a["ability"]["name"] for a in pokemon_data["abilities"]]
            
        # Extract stats
        stats = []
        if "stats" in pokemon_data:
            stats = [{
                "name": s["stat"]["name"],
                "base_value": s["base_stat"]
            } for s in pokemon_data["stats"]]
            
        # Extract moves (limiting to first 10 for brevity)
        moves = []
        if "moves" in pokemon_data:
            moves = [m["move"]["name"] for m in pokemon_data["moves"][:10]]
            
        # Extract sprites
        sprites = {}
        if "sprites" in pokemon_data:
            sprite_data = pokemon_data["sprites"]
            sprites = {
                "front_default": sprite_data.get("front_default"),
                "back_default": sprite_data.get("back_default"),
                "front_shiny": sprite_data.get("front_shiny"),
                "back_shiny": sprite_data.get("back_shiny")
            }
            
            # Add official artwork if available
            if "other" in sprite_data and "official-artwork" in sprite_data["other"]:
                sprites["official_artwork"] = sprite_data["other"]["official-artwork"].get("front_default")
                
        return {
            "id": pokemon_data.get("id"),
            "name": pokemon_data.get("name"),
            "height": pokemon_data.get("height"),
            "weight": pokemon_data.get("weight"),
            "types": types,
            "abilities": abilities,
            "stats": stats,
            "moves": moves,
            "sprites": sprites,
            "base_experience": pokemon_data.get("base_experience")
        }
    
    @classmethod
    def create_pokemon_from_api_data(cls, pokemon_data: Dict[str, Any]) -> Pokemon:
        """Create a Pokemon object from PokeAPI data.
        
        Args:
            pokemon_data: Pokemon data from PokeAPI
            
        Returns:
            Pokemon: A Pokemon object
        """
        # Extract key information
        info = cls.extract_pokemon_info(pokemon_data)
        
        # Create and return a Pokemon object
        return Pokemon(
            name=info["name"],
            pokemon_id=info["id"],
            types=info["types"],
            sprites=info["sprites"],
            height=info["height"],
            weight=info["weight"],
            stats=info["stats"],
            abilities=info["abilities"],
            moves=info["moves"]
        )