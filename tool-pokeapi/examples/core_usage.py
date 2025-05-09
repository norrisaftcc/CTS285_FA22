"""
Example script demonstrating the core functionality of the PokeSense application.

This script shows how to:
1. Search for Pokemon using the PokeAPI
2. Get detailed information about a Pokemon
3. Add Pokemon to a collection
4. Save and load Pokemon from storage
"""

import os
import sys

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pokeapi_service import PokeApiService
from core.models import Pokemon
from core.storage import JsonStorage
from core.operations import PokemonCollection


def main():
    """Demonstrate the core functionality of PokeSense."""
    print("PokeSense Core Functionality Demo")
    print("=================================")
    
    # Create a temporary storage file for this demo
    storage_file = os.path.join(os.path.dirname(__file__), 'demo_pokemon.json')
    storage = JsonStorage(storage_file)
    
    # Create a Pokemon collection
    collection = PokemonCollection(storage)
    
    # Search for Pokemon
    print("\nSearching for Pokemon with 'char' in their name...")
    search_results = PokeApiService.search_pokemon('char')
    
    if search_results and search_results['pokemon']:
        print(f"Found {search_results['count']} Pokemon. Here are the first few:")
        for i, pokemon in enumerate(search_results['pokemon'][:5]):
            print(f"{i+1}. {pokemon['name']}")
    
        # Get details for Charizard
        print("\nGetting details for Charizard...")
        charizard_data = PokeApiService.get_pokemon_details('charizard')
        
        if charizard_data:
            charizard_info = PokeApiService.extract_pokemon_info(charizard_data)
            print(f"Pokemon: #{charizard_info['id']} {charizard_info['name'].capitalize()}")
            print(f"Types: {', '.join(charizard_info['types'])}")
            print(f"Height: {charizard_info['height']/10} m")
            print(f"Weight: {charizard_info['weight']/10} kg")
            print(f"Base Experience: {charizard_info['base_experience']}")
            print(f"Abilities: {', '.join(charizard_info['abilities'])}")
            
            # Create a Pokemon object and add to collection
            print("\nAdding Charizard to collection...")
            charizard = PokeApiService.create_pokemon_from_api_data(charizard_data)
            collection.add_pokemon(charizard)
            
            # Add another Pokemon - Pikachu
            print("Adding Pikachu to collection...")
            pikachu_data = PokeApiService.get_pokemon_details('pikachu')
            if pikachu_data:
                pikachu = PokeApiService.create_pokemon_from_api_data(pikachu_data)
                collection.add_pokemon(pikachu)
            
            # List all Pokemon in the collection
            print("\nPokemon in collection:")
            for pokemon in collection.list_pokemon():
                print(f"- {pokemon.name.capitalize()} (#{pokemon.pokemon_id})")
            
            # Filter Pokemon by type
            fire_pokemon = collection.filter_pokemon(types=['fire'])
            print(f"\nFire-type Pokemon: {len(fire_pokemon)}")
            for pokemon in fire_pokemon:
                print(f"- {pokemon.name.capitalize()}")
            
            # Update a Pokemon
            print("\nMarking Charizard as favorite...")
            charizard.favorite = True
            charizard.notes = "My first Pokemon!"
            collection.update_pokemon(charizard)
            
            # Get and display the updated Pokemon
            updated_charizard = collection.get_pokemon(charizard.id)
            print(f"Updated {updated_charizard.name}:")
            print(f"- Favorite: {updated_charizard.favorite}")
            print(f"- Notes: {updated_charizard.notes}")
            
            # Get collection statistics
            stats = collection.get_statistics()
            print("\nCollection Statistics:")
            print(f"- Total Pokemon: {stats['total_pokemon']}")
            print(f"- Favorite Pokemon: {stats['favorite_pokemon']}")
            print("- Types:")
            for type_name, count in stats['types'].items():
                print(f"  - {type_name.capitalize()}: {count}")
    else:
        print("No Pokemon found in the search.")
    
    # Clean up the demo file
    print("\nCleaning up demo files...")
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main()