#!/usr/bin/env python3
"""
Simple script to test the PokeAPI integration.

This script validates that we can successfully fetch data from the PokeAPI,
parse it correctly, and create Pokemon objects.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pokeapi_service import PokeApiService
from core.models import Pokemon


def test_search_pokemon(query):
    """Test searching for Pokemon by name."""
    print(f"\n=== Testing Pokemon Search: '{query}' ===")
    
    results = PokeApiService.search_pokemon(query)
    
    if not results or results["count"] == 0:
        print(f"No Pokemon found matching '{query}'")
        return None
    
    print(f"Found {results['count']} Pokemon. First few results:")
    for i, pokemon in enumerate(results["pokemon"][:5]):
        print(f"  {i+1}. {pokemon['name']}")
    
    # Return the first result for further testing
    if results["pokemon"]:
        return results["pokemon"][0]["name"]
    return None


def test_get_pokemon_details(pokemon_name):
    """Test getting detailed information about a Pokemon."""
    print(f"\n=== Testing Pokemon Details: {pokemon_name} ===")
    
    pokemon_data = PokeApiService.get_pokemon_details(pokemon_name)
    
    if not pokemon_data:
        print(f"Failed to retrieve details for {pokemon_name}")
        return None
    
    # Extract and display key information
    info = PokeApiService.extract_pokemon_info(pokemon_data)
    
    print(f"Pokemon: #{info['id']} {info['name'].capitalize()}")
    print(f"Types: {', '.join(info['types'])}")
    print(f"Height: {info['height']/10} m")
    print(f"Weight: {info['weight']/10} kg")
    
    if info.get('abilities'):
        print(f"Abilities: {', '.join(info['abilities'])}")
    
    if info.get('stats'):
        print("Base Stats:")
        for stat in info['stats']:
            print(f"  {stat['name'].capitalize()}: {stat['base_value']}")
    
    # Check for sprites
    if info.get('sprites'):
        print("Sprite URLs available:")
        for sprite_name, url in info['sprites'].items():
            if url:
                print(f"  {sprite_name}: {url}")
    
    return pokemon_data


def test_create_pokemon_object(pokemon_data):
    """Test creating a Pokemon object from API data."""
    print("\n=== Testing Pokemon Object Creation ===")
    
    pokemon = PokeApiService.create_pokemon_from_api_data(pokemon_data)
    
    print(f"Created Pokemon object for {pokemon.name}:")
    print(f"  ID: {pokemon.id}")
    print(f"  Pokemon ID: {pokemon.pokemon_id}")
    print(f"  Types: {', '.join(pokemon.types)}")
    print(f"  Height: {pokemon.height/10} m")
    print(f"  Weight: {pokemon.weight/10} kg")
    print(f"  Number of abilities: {len(pokemon.abilities)}")
    print(f"  Number of stats: {len(pokemon.stats)}")
    print(f"  Number of moves: {len(pokemon.moves)}")
    
    # Test serialization
    print("\nTesting serialization to dictionary...")
    pokemon_dict = pokemon.to_dict()
    print(f"  Dictionary has {len(pokemon_dict)} keys")
    
    # Test that we can serialize to JSON
    try:
        json_str = json.dumps(pokemon_dict)
        print(f"  Successfully serialized to JSON ({len(json_str)} characters)")
        
        # Optionally write to a temporary file to inspect
        with open("temp_pokemon.json", "w") as f:
            json.dump(pokemon_dict, f, indent=2)
        print("  Wrote serialized data to temp_pokemon.json for inspection")
    except Exception as e:
        print(f"  Error serializing to JSON: {e}")
    
    return pokemon


def main():
    """Run all API tests."""
    print("=== PokeAPI Integration Test ===")
    print("This script tests fetching data from the PokeAPI and creating Pokemon objects.")
    
    # Test with a few different Pokemon
    test_cases = ["pikachu", "charizard", "eevee"]
    
    for query in test_cases:
        # Test search
        pokemon_name = test_search_pokemon(query)
        if not pokemon_name:
            continue
        
        # Test getting details
        pokemon_data = test_get_pokemon_details(pokemon_name)
        if not pokemon_data:
            continue
        
        # Test creating a Pokemon object
        pokemon = test_create_pokemon_object(pokemon_data)
        
        # Only need to test one successfully
        if pokemon:
            print("\n✅ API integration test completed successfully!")
            break
    else:
        print("\n❌ All test cases failed")


if __name__ == "__main__":
    main()