#!/usr/bin/env python3
"""
Console-based Pokemon collection manager.

This script provides a command-line interface for managing Pokemon collections:
- Create new collections
- Add Pokemon from PokeAPI
- List Pokemon in a collection
- View Pokemon details
- Mark Pokemon as favorites
- Add notes to Pokemon
- Delete Pokemon from a collection
"""

import os
import sys
import argparse
from tabulate import tabulate

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pokeapi_service import PokeApiService
from core.models import Pokemon
from core.storage import JsonStorage
from core.operations import PokemonCollection


def create_collection(filename):
    """Create a new empty Pokemon collection."""
    if os.path.exists(filename):
        print(f"Collection file '{filename}' already exists.")
        return
    
    # Create the storage and save an empty collection
    storage = JsonStorage(filename)
    print(f"Created new empty collection: {filename}")


def add_pokemon(filename, pokemon_name):
    """Add a Pokemon to the collection."""
    if not os.path.exists(filename):
        print(f"Collection file '{filename}' does not exist.")
        return
    
    # Search for the Pokemon
    search_results = PokeApiService.search_pokemon(pokemon_name)
    if not search_results or search_results["count"] == 0:
        print(f"No Pokemon found matching '{pokemon_name}'")
        return
    
    # Display search results
    print(f"Found {search_results['count']} Pokemon matching '{pokemon_name}':")
    for i, pokemon in enumerate(search_results["pokemon"][:10]):
        print(f"{i+1}. {pokemon['name']}")
    
    # Ask user to choose which Pokemon to add
    if search_results["count"] > 1:
        choice = input("\nEnter the number of the Pokemon to add (or 0 to cancel): ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(search_results["pokemon"][:10]):
            print("Invalid choice. Operation cancelled.")
            return
        
        selected_name = search_results["pokemon"][int(choice)-1]["name"]
    else:
        selected_name = search_results["pokemon"][0]["name"]
    
    # Get detailed Pokemon data
    print(f"Fetching details for {selected_name}...")
    pokemon_data = PokeApiService.get_pokemon_details(selected_name)
    if not pokemon_data:
        print(f"Failed to retrieve details for {selected_name}")
        return
    
    # Create Pokemon object
    pokemon = PokeApiService.create_pokemon_from_api_data(pokemon_data)
    
    # Add to collection
    storage = JsonStorage(filename)
    collection = PokemonCollection(storage)
    
    if collection.add_pokemon(pokemon):
        print(f"Added {pokemon.name} to collection!")
    else:
        print(f"Failed to add {pokemon.name} to collection. It might already exist.")


def list_collection(filename):
    """List all Pokemon in a collection."""
    if not os.path.exists(filename):
        print(f"Collection file '{filename}' does not exist.")
        return
    
    # Load the collection
    storage = JsonStorage(filename)
    collection = PokemonCollection(storage)
    pokemon_list = collection.list_pokemon()
    
    if not pokemon_list:
        print("Collection is empty.")
        return
    
    # Get collection statistics
    stats = collection.get_statistics()
    
    # Print collection summary
    print(f"\nCollection: {filename}")
    print(f"Total Pokemon: {stats['total_pokemon']}")
    print(f"Favorite Pokemon: {stats['favorite_pokemon']}")
    
    # Print type distribution if any types exist
    if stats['types']:
        print("\nType Distribution:")
        for type_name, count in sorted(stats['types'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {type_name.capitalize()}: {count}")
    
    # Create a table of Pokemon
    table_data = []
    for pokemon in pokemon_list:
        # Prepare types as a comma-separated string
        types_str = ", ".join(t.capitalize() for t in pokemon.types)
        
        # Add star for favorites
        favorite = "★" if pokemon.favorite else ""
        
        # Add a row to the table
        table_data.append([
            pokemon.pokemon_id,
            pokemon.name.capitalize(),
            types_str,
            favorite,
            pokemon.notes[:30] + "..." if len(pokemon.notes) > 30 else pokemon.notes
        ])
    
    # Print the table
    print("\nPokemon in collection:")
    print(tabulate(
        table_data,
        headers=["ID", "Name", "Types", "Favorite", "Notes"],
        tablefmt="pretty"
    ))


def view_pokemon(filename, pokemon_name):
    """View detailed information about a Pokemon in the collection."""
    if not os.path.exists(filename):
        print(f"Collection file '{filename}' does not exist.")
        return
    
    # Load the collection
    storage = JsonStorage(filename)
    collection = PokemonCollection(storage)
    
    # Search for Pokemon by name
    results = collection.search_pokemon(pokemon_name)
    if not results:
        print(f"No Pokemon found with name '{pokemon_name}' in the collection.")
        return
    
    # If multiple matches, ask user to choose
    if len(results) > 1:
        print(f"Found {len(results)} Pokemon matching '{pokemon_name}':")
        for i, pokemon in enumerate(results):
            print(f"{i+1}. {pokemon.name.capitalize()}")
        
        choice = input("\nEnter the number of the Pokemon to view (or 0 to cancel): ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
            print("Invalid choice. Operation cancelled.")
            return
        
        pokemon = results[int(choice)-1]
    else:
        pokemon = results[0]
    
    # Display detailed information
    print(f"\n=== {pokemon.name.capitalize()} (#{pokemon.pokemon_id}) ===")
    print(f"Types: {', '.join(t.capitalize() for t in pokemon.types)}")
    print(f"Height: {pokemon.height/10:.1f} m")
    print(f"Weight: {pokemon.weight/10:.1f} kg")
    print(f"Favorite: {'Yes' if pokemon.favorite else 'No'}")
    
    if pokemon.abilities:
        print(f"\nAbilities: {', '.join(a.replace('-', ' ').title() for a in pokemon.abilities)}")
    
    if pokemon.stats:
        print("\nBase Stats:")
        for stat in pokemon.stats:
            print(f"  {stat['name'].replace('-', ' ').title()}: {stat['base_value']}")
    
    if pokemon.notes:
        print(f"\nNotes: {pokemon.notes}")
    
    if pokemon.sprites and pokemon.sprites.get('front_default'):
        print(f"\nSprite URL: {pokemon.sprites['front_default']}")


def update_pokemon(filename, pokemon_name):
    """Update a Pokemon's favorite status and notes."""
    if not os.path.exists(filename):
        print(f"Collection file '{filename}' does not exist.")
        return
    
    # Load the collection
    storage = JsonStorage(filename)
    collection = PokemonCollection(storage)
    
    # Search for Pokemon by name
    results = collection.search_pokemon(pokemon_name)
    if not results:
        print(f"No Pokemon found with name '{pokemon_name}' in the collection.")
        return
    
    # If multiple matches, ask user to choose
    if len(results) > 1:
        print(f"Found {len(results)} Pokemon matching '{pokemon_name}':")
        for i, pokemon in enumerate(results):
            print(f"{i+1}. {pokemon.name.capitalize()}")
        
        choice = input("\nEnter the number of the Pokemon to update (or 0 to cancel): ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
            print("Invalid choice. Operation cancelled.")
            return
        
        pokemon = results[int(choice)-1]
    else:
        pokemon = results[0]
    
    # Display current values
    print(f"\nUpdating {pokemon.name.capitalize()} (#{pokemon.pokemon_id})")
    print(f"Current favorite status: {'Yes' if pokemon.favorite else 'No'}")
    print(f"Current notes: {pokemon.notes}")
    
    # Update favorite status
    favorite_input = input("\nMark as favorite? (y/n): ").lower()
    if favorite_input in ['y', 'yes']:
        pokemon.favorite = True
    elif favorite_input in ['n', 'no']:
        pokemon.favorite = False
    
    # Update notes
    notes_input = input(f"Enter notes (leave empty to keep current): ")
    if notes_input:
        pokemon.notes = notes_input
    
    # Save the updated Pokemon
    if collection.update_pokemon(pokemon):
        print(f"Updated {pokemon.name} successfully!")
    else:
        print(f"Failed to update {pokemon.name}.")


def delete_pokemon(filename, pokemon_name):
    """Delete a Pokemon from the collection."""
    if not os.path.exists(filename):
        print(f"Collection file '{filename}' does not exist.")
        return
    
    # Load the collection
    storage = JsonStorage(filename)
    collection = PokemonCollection(storage)
    
    # Search for Pokemon by name
    results = collection.search_pokemon(pokemon_name)
    if not results:
        print(f"No Pokemon found with name '{pokemon_name}' in the collection.")
        return
    
    # If multiple matches, ask user to choose
    if len(results) > 1:
        print(f"Found {len(results)} Pokemon matching '{pokemon_name}':")
        for i, pokemon in enumerate(results):
            print(f"{i+1}. {pokemon.name.capitalize()}")
        
        choice = input("\nEnter the number of the Pokemon to delete (or 0 to cancel): ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(results):
            print("Invalid choice. Operation cancelled.")
            return
        
        pokemon = results[int(choice)-1]
    else:
        pokemon = results[0]
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {pokemon.name.capitalize()}? (y/n): ").lower()
    if confirm not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    # Delete the Pokemon
    if collection.delete_pokemon(pokemon.id):
        print(f"Deleted {pokemon.name} from collection!")
    else:
        print(f"Failed to delete {pokemon.name}.")


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Pokemon Collection Manager")
    parser.add_argument("--file", "-f", help="Collection file path", default="pokemon_collection.json")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create collection command
    create_parser = subparsers.add_parser("create", help="Create a new collection")
    
    # Add Pokemon command
    add_parser = subparsers.add_parser("add", help="Add a Pokemon to the collection")
    add_parser.add_argument("name", help="Name of the Pokemon to add")
    
    # List collection command
    list_parser = subparsers.add_parser("list", help="List all Pokemon in the collection")
    
    # View Pokemon command
    view_parser = subparsers.add_parser("view", help="View detailed information about a Pokemon")
    view_parser.add_argument("name", help="Name of the Pokemon to view")
    
    # Update Pokemon command
    update_parser = subparsers.add_parser("update", help="Update a Pokemon's favorite status and notes")
    update_parser.add_argument("name", help="Name of the Pokemon to update")
    
    # Delete Pokemon command
    delete_parser = subparsers.add_parser("delete", help="Delete a Pokemon from the collection")
    delete_parser.add_argument("name", help="Name of the Pokemon to delete")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "create":
        create_collection(args.file)
    elif args.command == "add":
        add_pokemon(args.file, args.name)
    elif args.command == "list":
        list_collection(args.file)
    elif args.command == "view":
        view_pokemon(args.file, args.name)
    elif args.command == "update":
        update_pokemon(args.file, args.name)
    elif args.command == "delete":
        delete_pokemon(args.file, args.name)
    else:
        # If no command is provided, show help
        parser.print_help()


if __name__ == "__main__":
    main()