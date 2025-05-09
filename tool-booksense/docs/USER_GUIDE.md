# BookSense User Guide

This guide provides detailed instructions for using the BookSense application.

## Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd tool-booksense
   ```

2. **Set up the environment**
   ```bash
   # Activate the virtual environment
   source toolvenv/bin/activate  # On Unix/Mac
   toolvenv\Scripts\activate     # On Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   cd streamlit_example
   streamlit run openlibrary_app_with_export.py
   ```

The application will open in your default web browser, typically at `http://localhost:8501`.

## User Interface Overview

BookSense has a clean, intuitive interface organized into three main sections:

1. **Sidebar** - Contains search functionality, collection statistics, and quick import/export options
2. **Main Area** - Features tabs for different functions (search, collection, import/export)
3. **Detail Views** - Shows detailed information about selected books

## Searching for Books

BookSense allows you to search for books using the Open Library API.

1. In the sidebar, select a **Search Type**:
   - Title - Search by book title
   - Author - Search by author name
   - Subject - Search by book subject/genre
   - ISBN - Search by ISBN number
   - All - Search across all fields

2. Enter your **Search Query** in the text field

3. Click the **Search** button to find matching books

4. View results in the **Search Books** tab:
   - Book cover images (when available)
   - Basic information (title, author, year)
   - "Add to Collection" button for each book
   - "More Details" section for additional information

5. Click **Add to Collection** to add a book to your personal collection

## Managing Your Collection

The **My Collection** tab allows you to view and manage your personal book collection.

### Filtering and Sorting

1. Use the dropdown to filter books by **Reading Status** (All, Read, Reading, To Read)
2. Adjust the slider to filter by **Minimum Rating**
3. Select a field to **Sort By** (Title, Author, Year, Rating)
4. Toggle the **Ascending** checkbox to change sort direction

### Book Details and Updates

1. Select a book from your collection to view its details
2. View the full book information, including:
   - Cover image
   - Title and author
   - Publication year
   - Rating and reading status
   - ISBN and genres
   - Description (when available)

3. Update book information:
   - Change the **Reading Status** using the dropdown
   - Adjust the **Rating** using the slider
   - Click **Update Book** to save changes

4. Remove books:
   - Click **Remove from Collection** to delete a book

## Importing and Exporting

The **Import/Export** tab provides tools for backing up and restoring your collection.

### Exporting Your Collection

1. Select your preferred format (**JSON** or **CSV**)
2. Click the **Download** link to save the file to your computer
3. Use the **Preview** section to see what the exported data looks like

### Importing Books

1. Click **Choose a file** to select a JSON or CSV file from your computer
2. Click **Import Books** to add the books to your collection
3. A success message will show how many books were imported

### Sample Data

If you don't have any data to import, you can:

1. Click **Generate Sample JSON** or **Generate Sample CSV** to create sample data
2. View the sample data in the preview section
3. Click **Download Sample** to save it to your computer
4. Click **Import Sample Data** to add the sample books to your collection

## Tips and Tricks

1. **Quick Searches**: Use the sample search buttons on the welcome screen to quickly try common searches

2. **Efficient Filtering**: Combine status filtering and rating filtering to quickly find specific books

3. **Backup Strategy**: Regularly export your collection to JSON for backup purposes

4. **Collection Sharing**: Export your collection and share the file with friends who also use BookSense

5. **Alternative Views**: Use the sidebar's collection statistics for a quick overview of your reading habits

## Troubleshooting

1. **Search Not Working**
   - Check your internet connection
   - Verify that your search term is spelled correctly
   - Try different search types (title, author, etc.)

2. **Import Errors**
   - Ensure your import file is properly formatted JSON or CSV
   - Check that the file contains the required book fields
   - Try using the sample data feature to see correct formatting

3. **Books Not Displaying Correctly**
   - Check if the book has a cover URL available
   - Some books from Open Library may have limited information
   - Try adding more detailed information manually through the update feature

4. **Application Not Loading**
   - Verify that all dependencies are installed
   - Check that you're running the correct application file
   - Restart the application if necessary

---

For further assistance or to report issues, please contact the development team or submit an issue on GitHub.