"""
Streamlit application with Open Library integration.

This application demonstrates how to use the Open Library API in a Streamlit interface.
"""

import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.openlibrary_service import OpenLibraryService
from core.models import Book
from core.storage import JsonStorage
from core.operations import BookCollection


# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'collection' not in st.session_state:
    # Create a storage for our books
    storage_file = os.path.join(os.path.dirname(__file__), 'streamlit_books.json')
    storage = JsonStorage(storage_file)
    st.session_state.collection = BookCollection(storage)


def search_books():
    """Search for books based on user input."""
    search_query = st.session_state.search_query
    search_type = st.session_state.search_type
    
    if search_query:
        with st.spinner(f'Searching for {search_type}s matching "{search_query}"...'):
            results = OpenLibraryService.search_books(
                search_query, 
                search_type=search_type, 
                limit=10
            )
            st.session_state.search_results = results


def add_book_to_collection(book_data):
    """Add a book to the collection."""
    book = OpenLibraryService.create_book_from_ol_data(book_data)
    success = st.session_state.collection.add_book(book)
    return success, book


# Set page title and header
st.set_page_config(page_title="BookSense - Open Library Search", layout="wide")
st.title('BookSense - Open Library Integration')

st.write("""
This application demonstrates how to integrate the Open Library API with BookSense.
Search for books, view details, and add them to your collection.
""")

# Create sidebar
st.sidebar.title("Book Search")

# Search form in sidebar
with st.sidebar.form("search_form"):
    st.write("### Search Open Library")
    st.selectbox(
        'Search Type',
        options=['title', 'author', 'subject', 'isbn', 'all'],
        index=0,
        key='search_type'
    )
    st.text_input('Search Query', key='search_query')
    st.form_submit_button("Search", on_click=search_books)

# Display collection stats in sidebar
st.sidebar.write("---")
st.sidebar.write("### Your Collection")
books_in_collection = st.session_state.collection.list_books()
st.sidebar.write(f"Total Books: {len(books_in_collection)}")

if books_in_collection:
    # Get stats
    stats = st.session_state.collection.get_statistics()
    st.sidebar.write(f"Read: {stats['read_books']}")
    st.sidebar.write(f"Reading: {stats['reading_books']}")
    st.sidebar.write(f"To Read: {stats['to_read_books']}")
    st.sidebar.write(f"Average Rating: {stats['average_rating']:.2f}")

# Display search results
if st.session_state.search_results:
    results = st.session_state.search_results
    st.write(f"## Search Results")
    st.write(f"Found {results['total_found']} books. Showing first {len(results['books'])} results:")
    
    # Create tabs
    search_tab, collection_tab = st.tabs(["Search Results", "Your Collection"])
    
    with search_tab:
        # Display results in a grid layout
        cols = st.columns(2)  # Create 2 columns
        
        for i, book_data in enumerate(results['books']):
            col_idx = i % 2  # Alternate between columns
            with cols[col_idx]:
                info = OpenLibraryService.extract_book_info(book_data)
                
                # Create a card-like container
                with st.container():
                    st.write("---")
                    
                    # Create a row for cover and details
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if info['cover_url']:
                            st.image(info['cover_url'], width=100)
                        else:
                            st.write("No cover available")
                    
                    with col2:
                        st.write(f"**{info['title']}**")
                        st.write(f"By: {', '.join(info['authors'])}")
                        st.write(f"Published: {info['first_published']}")
                        if info['isbn']:
                            st.write(f"ISBN: {info['isbn']}")
                        
                        # Add to collection button
                        if st.button(f"Add to Collection", key=f"add_{i}"):
                            success, book = add_book_to_collection(book_data)
                            if success:
                                st.success(f"Added '{info['title']}' to your collection!")
                            else:
                                st.error("This book is already in your collection.")
                    
                    # Expandable section for more details
                    with st.expander("More Details"):
                        if info['subjects']:
                            st.write(f"**Subjects:** {', '.join(info['subjects'])}")
                        
                        st.write(f"**Editions:** {info['editions_count']}")
                        
                        if info['open_library_url']:
                            st.write(f"[View on Open Library]({info['open_library_url']})")
    
    with collection_tab:
        # Display the book collection
        if not books_in_collection:
            st.write("Your collection is empty. Add books from the search results!")
        else:
            # Convert books to a DataFrame for easy display
            books_data = []
            for book in books_in_collection:
                books_data.append({
                    'Title': book.title,
                    'Author': book.author,
                    'Year': book.year,
                    'Rating': book.rating,
                    'Status': book.read_status,
                    'ID': book.id
                })
            
            df = pd.DataFrame(books_data)
            
            # Display sortable table
            st.dataframe(
                df.drop(columns=['ID']),
                hide_index=True,
                column_config={
                    "Title": st.column_config.TextColumn("Title"),
                    "Author": st.column_config.TextColumn("Author"),
                    "Year": st.column_config.NumberColumn("Year"),
                    "Rating": st.column_config.NumberColumn("Rating", format="%.1f ⭐"),
                    "Status": st.column_config.SelectboxColumn(
                        "Status", 
                        options=["Read", "Reading", "To Read"]
                    )
                }
            )
            
            # Detail view for a selected book
            st.write("## Book Details")
            selected_book_index = st.selectbox(
                "Select a book to view details:",
                options=range(len(books_in_collection)),
                format_func=lambda x: books_in_collection[x].title
            )
            
            selected_book = books_in_collection[selected_book_index]
            
            # Display the selected book details
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if selected_book.cover_url:
                    st.image(selected_book.cover_url, width=150)
                else:
                    st.write("No cover available")
            
            with col2:
                st.write(f"### {selected_book.title}")
                st.write(f"**Author:** {selected_book.author}")
                st.write(f"**Year:** {selected_book.year}")
                st.write(f"**Rating:** {selected_book.rating} / 5.0")
                st.write(f"**Status:** {selected_book.read_status}")
                
                if selected_book.isbn:
                    st.write(f"**ISBN:** {selected_book.isbn}")
                
                if selected_book.genre:
                    st.write(f"**Genres:** {', '.join(selected_book.genre)}")
                
                if selected_book.description:
                    st.write(f"**Description:** {selected_book.description}")
                
                # Update book status
                new_status = st.selectbox(
                    "Update reading status:",
                    options=["Read", "Reading", "To Read"],
                    index=["Read", "Reading", "To Read"].index(selected_book.read_status)
                )
                
                new_rating = st.slider(
                    "Update rating:",
                    min_value=0.0,
                    max_value=5.0,
                    value=selected_book.rating,
                    step=0.5
                )
                
                if st.button("Update Book"):
                    selected_book.read_status = new_status
                    selected_book.rating = new_rating
                    st.session_state.collection.update_book(selected_book)
                    st.success("Book updated successfully!")
                
                if st.button("Remove from Collection", type="secondary"):
                    if st.session_state.collection.delete_book(selected_book.id):
                        st.warning(f"'{selected_book.title}' has been removed from your collection.")
                        st.rerun()  # Refresh the page
                    else:
                        st.error("Failed to remove the book.")

else:
    # No search results yet, show collection or welcome message
    if books_in_collection:
        st.write("## Your Book Collection")
        
        # Convert books to a DataFrame for easy display
        books_data = []
        for book in books_in_collection:
            books_data.append({
                'Title': book.title,
                'Author': book.author,
                'Year': book.year,
                'Rating': book.rating,
                'Status': book.read_status
            })
        
        df = pd.DataFrame(books_data)
        st.dataframe(df)
        
    else:
        st.write("## Welcome to BookSense!")
        st.write("""
        Search for books using the form in the sidebar to get started.
        You can search by title, author, subject, or ISBN.
        """)
        
        # Sample searches to help users get started
        st.write("### Try these sample searches:")
        sample_searches = [
            "The Great Gatsby",
            "J.K. Rowling",
            "Science Fiction",
            "9780743273565"  # ISBN for The Great Gatsby
        ]
        
        for sample in sample_searches:
            if st.button(f"Search for '{sample}'"):
                st.session_state.search_query = sample
                st.session_state.search_type = "title" if not sample.startswith("9") else "isbn"
                search_books()
                st.rerun()  # Refresh the page with search results