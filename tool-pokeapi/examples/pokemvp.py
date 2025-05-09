#!/usr/bin/env python3
"""
Minimal Viable Pokemon (MVP) Demo

This is a simple script that:
1. Retrieves Pikachu from the PokeAPI
2. Prints its information
3. Saves it to a JSON file
4. Exits

No user input required - just a basic demonstration of core functionality.
"""

import os
import sys
import json

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pokeapi_service import PokeApiService
from core.models import Pokemon
from core.storage import JsonStorage
from core.operations import PokemonCollection


def main():
    """Run the MVP demo."""
    print("=== PokeSense MVP Demo ===\n")
    
    # Step 1: Retrieve Pikachu from the API
    print("1. Fetching Pikachu from PokeAPI...")
    pokemon_data = PokeApiService.get_pokemon_details("pikachu")
    
    if not pokemon_data:
        print("Failed to fetch Pikachu. Please check your internet connection.")
        return
    
    # Step 2: Create a Pokemon object
    print("2. Creating Pokemon object...")
    pikachu = PokeApiService.create_pokemon_from_api_data(pokemon_data)
    
    # Step 3: Print Pokemon information
    print("\n=== Pikachu Information ===")
    print(f"Name: {pikachu.name.capitalize()}")
    print(f"Pokedex ID: #{pikachu.pokemon_id}")
    print(f"Types: {', '.join(t.capitalize() for t in pikachu.types)}")
    print(f"Height: {pikachu.height/10:.1f} m")
    print(f"Weight: {pikachu.weight/10:.1f} kg")
    
    print("\nAbilities:")
    for ability in pikachu.abilities:
        print(f"- {ability.replace('-', ' ').title()}")
    
    print("\nBase Stats:")
    for stat in pikachu.stats:
        print(f"- {stat['name'].replace('-', ' ').title()}: {stat['base_value']}")
    
    # Step 4: Save to JSON file
    collection_file = "mvp_collection.json"
    print(f"\n3. Saving Pikachu to {collection_file}...")
    
    storage = JsonStorage(collection_file)
    collection = PokemonCollection(storage)
    
    # Add Pikachu to the collection
    if collection.add_pokemon(pikachu):
        print(f"Successfully saved Pikachu to {collection_file}")
    else:
        print(f"Pikachu already exists in {collection_file}")
    
    # Step 5: Verify we can read the Pokemon back
    print("\n4. Reading Pokemon from storage...")
    
    # Reload the collection to verify
    fresh_collection = PokemonCollection(storage)
    pokemon_list = fresh_collection.list_pokemon()
    
    print(f"Found {len(pokemon_list)} Pokemon in collection")
    if pokemon_list:
        saved_pokemon = pokemon_list[0]
        print(f"Retrieved: {saved_pokemon.name.capitalize()} (#{saved_pokemon.pokemon_id})")
    
    print("\n=== Demo Completed Successfully ===")


if __name__ == "__main__":
    main()