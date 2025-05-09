"""
Streamlit application with Open Library integration and import/export functionality.

This application demonstrates how to use the Open Library API in a Streamlit interface
and allows users to import and export their book collections.
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import StringIO

# Add the parent directory to the path so we can import the core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import Book
from core.storage import JsonStorage
from core.storage_factory import StorageFactory
from core.operations import BookCollection
from core.openlibrary_service import OpenLibraryService
from core.utils import export_to_json, import_from_json, export_to_csv, import_from_csv


# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'collection' not in st.session_state:
    # Create a storage for our books
    storage_file = os.path.join(os.path.dirname(__file__), 'streamlit_books.json')
    storage = JsonStorage(storage_file)
    st.session_state.collection = BookCollection(storage)
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

# Initialize session state for the sample search functionality
if 'do_sample_search' not in st.session_state:
    st.session_state.do_sample_search = False
if 'sample_term' not in st.session_state:
    st.session_state.sample_term = ""
if 'sample_type' not in st.session_state:
    st.session_state.sample_type = "title"


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


def trigger_sample_search(sample_text, is_isbn=False):
    """Set up a sample search to be executed."""
    st.session_state.do_sample_search = True
    st.session_state.sample_term = sample_text
    st.session_state.sample_type = "isbn" if is_isbn else "title"


def add_book_to_collection(book_data):
    """Add a book to the collection."""
    book = OpenLibraryService.create_book_from_ol_data(book_data)
    success = st.session_state.collection.add_book(book)
    return success, book


def get_download_link(data, filename, text):
    """Generate a download link for data."""
    b64 = base64.b64encode(data.encode()).decode()
    href = f'data:file/txt;base64,{b64}'
    return f'<a href="{href}" download="{filename}">{text}</a>'


def import_books_from_file(file_data, file_format):
    """Import books from uploaded file data."""
    try:
        if file_format == 'json':
            books = import_from_json(file_data)
        else:  # csv
            books = import_from_csv(file_data)
        
        # Add each book to the collection
        added_count = 0
        for book in books:
            if st.session_state.collection.add_book(book):
                added_count += 1
        
        return added_count, len(books)
    except Exception as e:
        st.error(f"Error importing books: {e}")
        return 0, 0


# Set page title and header
st.set_page_config(page_title="BookSense - Book Manager", layout="wide")
st.title('BookSense - Book Management System')

st.write("""
This application allows you to search for books using the Open Library API,
manage your personal book collection, and import/export your data.
""")

# Handle sample search if triggered
if st.session_state.do_sample_search:
    # Reset the flag
    st.session_state.do_sample_search = False
    
    # Set the search form values
    st.session_state.search_query = st.session_state.sample_term
    st.session_state.search_type = st.session_state.sample_type
    
    # Perform the search
    search_books()
    

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

# Export functionality in sidebar
st.sidebar.write("---")
st.sidebar.write("### Import/Export")

export_format = st.sidebar.selectbox(
    "Export Format", 
    options=["JSON", "CSV"],
    index=0
)

if st.sidebar.button("Export Collection"):
    if books_in_collection:
        if export_format == "JSON":
            data = export_to_json(books_in_collection, pretty=True)
            download_link = get_download_link(data, 'booksense_collection.json', 'Download JSON')
        else:  # CSV
            data = export_to_csv(books_in_collection)
            download_link = get_download_link(data, 'booksense_collection.csv', 'Download CSV')
        
        st.sidebar.markdown(download_link, unsafe_allow_html=True)
    else:
        st.sidebar.warning("Your collection is empty. Add some books first!")

# Import functionality in sidebar
uploaded_file = st.sidebar.file_uploader("Import Collection", type=['json', 'csv'])
if uploaded_file is not None:
    file_format = uploaded_file.name.split('.')[-1].lower()
    file_data = uploaded_file.getvalue().decode('utf-8')
    
    if st.sidebar.button("Import Books"):
        added_count, total_count = import_books_from_file(file_data, file_format)
        if total_count > 0:
            st.sidebar.success(f"Imported {added_count} of {total_count} books!")
            st.rerun()  # Refresh the page to show new books
        else:
            st.sidebar.error("No valid books found in the file.")

# Main content area with tabs
search_tab, collection_tab, import_export_tab = st.tabs([
    "Search Books", "My Collection", "Import/Export"
])

# Display search results in Search tab
with search_tab:
    if st.session_state.search_results:
        results = st.session_state.search_results
        st.write(f"## Search Results")
        st.write(f"Found {results['total_found']} books. Showing first {len(results['books'])} results:")
        
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
    else:
        # Welcome message or no results
        st.write("## Search for Books")
        st.write("""
        Use the search form in the sidebar to find books in the Open Library database.
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
            is_isbn = sample.startswith("9")
            if st.button(f"Search for '{sample}'"):
                trigger_sample_search(sample, is_isbn)
                st.rerun()  # Refresh the page

# Display collection in Collection tab
with collection_tab:
    if books_in_collection:
        st.write("## Your Book Collection")
        
        # Add filtering options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            filter_status = st.selectbox(
                "Filter by Status",
                options=["All", "Read", "Reading", "To Read"],
                index=0
            )
        
        with filter_col2:
            min_rating = st.slider(
                "Minimum Rating",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=0.5
            )
        
        with filter_col3:
            sort_by = st.selectbox(
                "Sort By",
                options=["Title", "Author", "Year", "Rating"],
                index=0
            )
            sort_asc = st.checkbox("Ascending", value=True)
        
        # Apply filters and sorting
        filtered_books = books_in_collection
        
        # Filter by status
        if filter_status != "All":
            filtered_books = [b for b in filtered_books if b.read_status == filter_status]
        
        # Filter by rating
        filtered_books = [b for b in filtered_books if b.rating >= min_rating]
        
        # Sort the books
        if sort_by == "Title":
            filtered_books = sorted(filtered_books, key=lambda b: b.title.lower(), reverse=not sort_asc)
        elif sort_by == "Author":
            filtered_books = sorted(filtered_books, key=lambda b: b.author.lower(), reverse=not sort_asc)
        elif sort_by == "Year":
            filtered_books = sorted(filtered_books, key=lambda b: b.year, reverse=not sort_asc)
        elif sort_by == "Rating":
            filtered_books = sorted(filtered_books, key=lambda b: b.rating, reverse=not sort_asc)
        
        # Show filter results
        st.write(f"Showing {len(filtered_books)} of {len(books_in_collection)} books")
        
        # Convert filtered books to a DataFrame for display
        if filtered_books:
            books_data = []
            for book in filtered_books:
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
            if filtered_books:
                selected_book_index = st.selectbox(
                    "Select a book to view details:",
                    options=range(len(filtered_books)),
                    format_func=lambda x: filtered_books[x].title
                )
                
                selected_book = filtered_books[selected_book_index]
                
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
            st.info("No books match your filters.")
    else:
        st.info("Your collection is empty. Search for books and add them to your collection!")

# Import/Export tab content
with import_export_tab:
    st.write("## Import and Export Your Collection")
    
    # Export section
    st.write("### Export Your Collection")
    st.write("Export your book collection to a file for backup or sharing.")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        export_format_tab = st.selectbox(
            "Select Format", 
            options=["JSON", "CSV"],
            index=0,
            key="export_format_tab"
        )
    
    with export_col2:
        if books_in_collection:
            if export_format_tab == "JSON":
                data = export_to_json(books_in_collection, pretty=True)
                download_link = get_download_link(data, 'booksense_collection.json', 'Download JSON')
                st.markdown(download_link, unsafe_allow_html=True)
                
                # Preview
                with st.expander("Preview JSON"):
                    st.code(data[:1000] + "..." if len(data) > 1000 else data, language="json")
            else:  # CSV
                data = export_to_csv(books_in_collection)
                download_link = get_download_link(data, 'booksense_collection.csv', 'Download CSV')
                st.markdown(download_link, unsafe_allow_html=True)
                
                # Preview
                with st.expander("Preview CSV"):
                    st.code(data[:1000] + "..." if len(data) > 1000 else data)
        else:
            st.warning("Your collection is empty. Add some books first!")
    
    # Import section
    st.write("---")
    st.write("### Import Books")
    st.write("Import books from a JSON or CSV file.")
    
    upload_col1, upload_col2 = st.columns(2)
    
    with upload_col1:
        uploaded_file_tab = st.file_uploader("Choose a file", type=['json', 'csv'], key="file_uploader_tab")
    
    with upload_col2:
        if uploaded_file_tab is not None:
            file_format = uploaded_file_tab.name.split('.')[-1].lower()
            file_data = uploaded_file_tab.getvalue().decode('utf-8')
            
            if file_format == 'json':
                st.info("Importing from JSON file...")
            else:
                st.info("Importing from CSV file...")
            
            if st.button("Import Books", key="import_button_tab"):
                added_count, total_count = import_books_from_file(file_data, file_format)
                if total_count > 0:
                    st.success(f"Imported {added_count} of {total_count} books!")
                    st.rerun()  # Refresh the page to show new books
                else:
                    st.error("No valid books found in the file.")
    
    # Sample data section
    st.write("---")
    st.write("### Sample Data")
    st.write("Don't have any data to import? Try these sample files:")
    
    sample_col1, sample_col2 = st.columns(2)
    
    with sample_col1:
        if st.button("Generate Sample JSON"):
            from core.utils import generate_sample_books
            sample_books = generate_sample_books()
            sample_json = export_to_json(sample_books, pretty=True)
            st.session_state.sample_data = sample_json
            st.session_state.sample_format = "json"
            st.rerun()
    
    with sample_col2:
        if st.button("Generate Sample CSV"):
            from core.utils import generate_sample_books
            sample_books = generate_sample_books()
            sample_csv = export_to_csv(sample_books)
            st.session_state.sample_data = sample_csv
            st.session_state.sample_format = "csv"
            st.rerun()
    
    # Display and allow download of sample data
    if hasattr(st.session_state, 'sample_data') and st.session_state.sample_data:
        st.write("### Sample Data Generated")
        
        # Show preview
        with st.expander("Preview"):
            if st.session_state.sample_format == "json":
                st.code(st.session_state.sample_data[:1000] + "..." 
                       if len(st.session_state.sample_data) > 1000 
                       else st.session_state.sample_data, 
                       language="json")
            else:
                st.code(st.session_state.sample_data[:1000] + "..." 
                       if len(st.session_state.sample_data) > 1000 
                       else st.session_state.sample_data)
        
        # Download link
        filename = f"sample_books.{st.session_state.sample_format}"
        download_link = get_download_link(
            st.session_state.sample_data, 
            filename, 
            f"Download Sample {st.session_state.sample_format.upper()}"
        )
        st.markdown(download_link, unsafe_allow_html=True)
        
        # Import button
        if st.button("Import Sample Data"):
            added_count, total_count = import_books_from_file(
                st.session_state.sample_data, 
                st.session_state.sample_format
            )
            if total_count > 0:
                st.success(f"Imported {added_count} of {total_count} sample books!")
                st.rerun()  # Refresh the page to show new books