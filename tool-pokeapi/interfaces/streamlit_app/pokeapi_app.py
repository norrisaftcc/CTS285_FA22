"""
Streamlit application with PokeAPI integration.

This application demonstrates how to use the PokeAPI in a Streamlit interface.
"""

import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.pokeapi_service import PokeApiService
from core.models import Pokemon
from core.storage import JsonStorage
from core.operations import PokemonCollection


# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'collection' not in st.session_state:
    # Create a storage for our Pokemon
    storage_file = os.path.join(os.path.dirname(__file__), 'streamlit_pokemon.json')
    storage = JsonStorage(storage_file)
    st.session_state.collection = PokemonCollection(storage)

# Initialize session state for the sample search functionality
if 'do_sample_search' not in st.session_state:
    st.session_state.do_sample_search = False
if 'sample_term' not in st.session_state:
    st.session_state.sample_term = ""


def search_pokemon():
    """Search for Pokemon based on user input."""
    search_query = st.session_state.search_query
    
    if search_query:
        with st.spinner(f'Searching for Pokemon matching "{search_query}"...'):
            results = PokeApiService.search_pokemon(search_query)
            st.session_state.search_results = results


def trigger_sample_search(sample_text):
    """Set up a sample search to be executed."""
    st.session_state.do_sample_search = True
    st.session_state.sample_term = sample_text


def add_pokemon_to_collection(pokemon_name):
    """Add a Pokemon to the collection."""
    with st.spinner(f'Fetching details for {pokemon_name}...'):
        pokemon_data = PokeApiService.get_pokemon_details(pokemon_name)
        if pokemon_data:
            pokemon = PokeApiService.create_pokemon_from_api_data(pokemon_data)
            success = st.session_state.collection.add_pokemon(pokemon)
            return success, pokemon
    return False, None


def get_pokemon_type_color(type_name):
    """Get a color for a Pokemon type."""
    type_colors = {
        'normal': '#A8A77A',
        'fire': '#EE8130',
        'water': '#6390F0',
        'electric': '#F7D02C',
        'grass': '#7AC74C',
        'ice': '#96D9D6',
        'fighting': '#C22E28',
        'poison': '#A33EA1',
        'ground': '#E2BF65',
        'flying': '#A98FF3',
        'psychic': '#F95587',
        'bug': '#A6B91A',
        'rock': '#B6A136',
        'ghost': '#735797',
        'dragon': '#6F35FC',
        'dark': '#705746',
        'steel': '#B7B7CE',
        'fairy': '#D685AD'
    }
    return type_colors.get(type_name.lower(), '#777777')


def display_type_badge(type_name):
    """Display a styled badge for a Pokemon type."""
    bg_color = get_pokemon_type_color(type_name)
    return f"""
    <span style="
        background-color: {bg_color}; 
        color: white; 
        padding: 3px 8px; 
        border-radius: 10px; 
        font-size: 0.8em; 
        margin-right: 5px;
        display: inline-block;
        text-shadow: 1px 1px 1px rgba(0,0,0,0.2);
    ">
        {type_name.upper()}
    </span>
    """


# Set page title and header
st.set_page_config(page_title="PokeSense - Pokemon Collection", layout="wide")
st.title('PokeSense - PokeAPI Integration')

st.write("""
This application demonstrates how to integrate the PokeAPI with PokeSense.
Search for Pokemon, view details, and add them to your collection.
""")

# Handle sample search if triggered
if st.session_state.do_sample_search:
    # Reset the flag
    st.session_state.do_sample_search = False
    
    # Set the search form values
    st.session_state.search_query = st.session_state.sample_term
    
    # Perform the search
    search_pokemon()
    

# Create sidebar
st.sidebar.title("Pokemon Search")

# Search form in sidebar
with st.sidebar.form("search_form"):
    st.write("### Search PokeAPI")
    st.text_input('Search Query', key='search_query', 
                  help="Enter a Pokemon name or partial name")
    st.form_submit_button("Search", on_click=search_pokemon)

# Display collection stats in sidebar
st.sidebar.write("---")
st.sidebar.write("### Your Collection")
pokemon_in_collection = st.session_state.collection.list_pokemon()
st.sidebar.write(f"Total Pokemon: {len(pokemon_in_collection)}")

if pokemon_in_collection:
    # Get stats
    stats = st.session_state.collection.get_statistics()
    st.sidebar.write(f"Favorite Pokemon: {stats['favorite_pokemon']}")
    
    # Display type breakdown if available
    if stats['types']:
        st.sidebar.write("#### Types in Collection:")
        for type_name, count in sorted(stats['types'].items(), key=lambda x: x[1], reverse=True)[:5]:
            st.sidebar.write(f"- {type_name.capitalize()}: {count}")

# Display search results
if st.session_state.search_results:
    results = st.session_state.search_results
    st.write(f"## Search Results")
    st.write(f"Found {results['count']} Pokemon. Showing first {len(results['pokemon'])} results:")
    
    # Create tabs
    search_tab, collection_tab = st.tabs(["Search Results", "Your Collection"])
    
    with search_tab:
        # Display results in a grid layout
        cols = st.columns(3)  # Create 3 columns
        
        for i, pokemon_item in enumerate(results['pokemon']):
            col_idx = i % 3  # Distribute across 3 columns
            with cols[col_idx]:
                pokemon_name = pokemon_item["name"]
                
                # Fetch details for this Pokemon
                with st.spinner(f"Loading {pokemon_name}..."):
                    pokemon_data = PokeApiService.get_pokemon_details(pokemon_name)
                    if pokemon_data:
                        info = PokeApiService.extract_pokemon_info(pokemon_data)
                        
                        # Create a card-like container
                        with st.container():
                            st.write("---")
                            
                            # Create a row for sprite and details
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                sprite_url = info.get('sprites', {}).get('official_artwork') or info.get('sprites', {}).get('front_default')
                                if sprite_url:
                                    st.image(sprite_url, width=120)
                                else:
                                    st.write("No sprite available")
                            
                            with col2:
                                st.write(f"**#{info['id']} {info['name'].capitalize()}**")
                                
                                # Display types
                                types_html = ""
                                for type_name in info['types']:
                                    types_html += display_type_badge(type_name)
                                st.markdown(types_html, unsafe_allow_html=True)
                                
                                st.write(f"Height: {info['height']/10:.1f} m")
                                st.write(f"Weight: {info['weight']/10:.1f} kg")
                                
                                # Add to collection button
                                if st.button(f"Add to Collection", key=f"add_{i}"):
                                    success, pokemon = add_pokemon_to_collection(pokemon_name)
                                    if success:
                                        st.success(f"Added '{info['name'].capitalize()}' to your collection!")
                                    else:
                                        st.error("This Pokemon is already in your collection.")
                            
                            # Expandable section for more details
                            with st.expander("More Details"):
                                # Show abilities
                                if info['abilities']:
                                    st.write("**Abilities:**")
                                    for ability in info['abilities']:
                                        st.write(f"- {ability.replace('-', ' ').title()}")
                                
                                # Show stats
                                if info['stats']:
                                    st.write("**Base Stats:**")
                                    for stat in info['stats']:
                                        stat_name = stat['name'].replace('-', ' ').title()
                                        stat_value = stat['base_value']
                                        # Create a progress bar for the stat
                                        max_stat = 255  # Maximum possible stat value
                                        st.write(f"{stat_name}: {stat_value}")
                                        st.progress(min(stat_value / max_stat, 1.0))
    
    with collection_tab:
        # Display the Pokemon collection
        if not pokemon_in_collection:
            st.write("Your collection is empty. Add Pokemon from the search results!")
        else:
            # Convert Pokemon to a DataFrame for easy display
            pokemon_data = []
            for pokemon in pokemon_in_collection:
                pokemon_data.append({
                    'Name': pokemon.name.capitalize(),
                    'ID': f"#{pokemon.pokemon_id}",
                    'Types': ", ".join(t.capitalize() for t in pokemon.types),
                    'Favorite': "★" if pokemon.favorite else "",
                    'Notes': pokemon.notes,
                    'Collection ID': pokemon.id
                })
            
            df = pd.DataFrame(pokemon_data)
            
            # Display sortable table
            st.dataframe(
                df.drop(columns=['Collection ID']),
                hide_index=True
            )
            
            # Detail view for a selected Pokemon
            st.write("## Pokemon Details")
            if pokemon_in_collection:
                selected_pokemon_index = st.selectbox(
                    "Select a Pokemon to view details:",
                    options=range(len(pokemon_in_collection)),
                    format_func=lambda x: f"{pokemon_in_collection[x].name.capitalize()} (#{pokemon_in_collection[x].pokemon_id})"
                )
                
                selected_pokemon = pokemon_in_collection[selected_pokemon_index]
                
                # Display the selected Pokemon details
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    sprite_url = selected_pokemon.sprites.get('official_artwork') or selected_pokemon.sprites.get('front_default')
                    if sprite_url:
                        st.image(sprite_url, width=200)
                    else:
                        st.write("No sprite available")
                
                with col2:
                    st.write(f"### #{selected_pokemon.pokemon_id} {selected_pokemon.name.capitalize()}")
                    
                    # Display types
                    types_html = ""
                    for type_name in selected_pokemon.types:
                        types_html += display_type_badge(type_name)
                    st.markdown(types_html, unsafe_allow_html=True)
                    
                    st.write(f"**Height:** {selected_pokemon.height/10:.1f} m")
                    st.write(f"**Weight:** {selected_pokemon.weight/10:.1f} kg")
                    
                    # Abilities
                    if selected_pokemon.abilities:
                        st.write("**Abilities:**")
                        abilities_text = ", ".join(ability.replace('-', ' ').title() 
                                                for ability in selected_pokemon.abilities)
                        st.write(abilities_text)
                    
                    # Update favorite status
                    new_favorite = st.checkbox(
                        "Mark as Favorite",
                        value=selected_pokemon.favorite
                    )
                    
                    # Notes input
                    new_notes = st.text_area(
                        "Notes:",
                        value=selected_pokemon.notes,
                        height=100
                    )
                    
                    if st.button("Update Pokemon"):
                        selected_pokemon.favorite = new_favorite
                        selected_pokemon.notes = new_notes
                        st.session_state.collection.update_pokemon(selected_pokemon)
                        st.success("Pokemon updated successfully!")
                    
                    if st.button("Remove from Collection", type="secondary"):
                        if st.session_state.collection.delete_pokemon(selected_pokemon.id):
                            st.warning(f"'{selected_pokemon.name.capitalize()}' has been removed from your collection.")
                            st.rerun()  # Refresh the page
                        else:
                            st.error("Failed to remove the Pokemon.")
                
                # Additional details in expandable sections
                with st.expander("Stats"):
                    if selected_pokemon.stats:
                        for stat in selected_pokemon.stats:
                            stat_name = stat['name'].replace('-', ' ').title()
                            stat_value = stat['base_value']
                            # Create a progress bar for the stat
                            max_stat = 255  # Maximum possible stat value
                            st.write(f"{stat_name}: {stat_value}")
                            st.progress(min(stat_value / max_stat, 1.0))
                
                with st.expander("Moves"):
                    if selected_pokemon.moves:
                        moves_list = [move.replace('-', ' ').title() for move in selected_pokemon.moves]
                        st.write(", ".join(moves_list))
                    else:
                        st.write("No moves information available")
                        
                with st.expander("Alternative Sprites"):
                    sprite_cols = st.columns(4)
                    
                    sprites = selected_pokemon.sprites
                    sprites_to_display = {
                        'Default': sprites.get('front_default'),
                        'Back': sprites.get('back_default'),
                        'Shiny': sprites.get('front_shiny'),
                        'Shiny Back': sprites.get('back_shiny')
                    }
                    
                    for i, (label, url) in enumerate(sprites_to_display.items()):
                        with sprite_cols[i]:
                            st.write(f"**{label}**")
                            if url:
                                st.image(url, width=100)
                            else:
                                st.write("N/A")

else:
    # No search results yet, show collection or welcome message
    if pokemon_in_collection:
        st.write("## Your Pokemon Collection")
        
        # Display Pokemon in a grid
        cols = st.columns(4)  # Create 4 columns
        
        for i, pokemon in enumerate(pokemon_in_collection):
            col_idx = i % 4  # Distribute across 4 columns
            with cols[col_idx]:
                sprite_url = pokemon.sprites.get('official_artwork') or pokemon.sprites.get('front_default')
                if sprite_url:
                    st.image(sprite_url, width=120)
                
                st.write(f"**{pokemon.name.capitalize()}**")
                
                # Display types inline
                types_html = ""
                for type_name in pokemon.types:
                    types_html += display_type_badge(type_name)
                st.markdown(types_html, unsafe_allow_html=True)
                
                if pokemon.favorite:
                    st.write("⭐ Favorite")
        
    else:
        st.write("## Welcome to PokeSense!")
        st.write("""
        Search for Pokemon using the form in the sidebar to get started.
        You can search by Pokemon name or partial name.
        """)
        
        # Sample searches to help users get started
        st.write("### Try these sample searches:")
        sample_searches = [
            "Pikachu",
            "Char",  # Will match Charmander, Charmeleon, etc.
            "Eevee",
            "Mew"  # Will match Mewtwo and Mew
        ]
        
        for sample in sample_searches:
            if st.button(f"Search for '{sample}'"):
                trigger_sample_search(sample)
                st.rerun()  # Refresh the page