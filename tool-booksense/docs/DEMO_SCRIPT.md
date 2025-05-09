# BookSense Demo Script

This script provides a step-by-step demonstration of the BookSense application for the presentation.

## Setup (Before Presentation)

1. Ensure the environment is activated:
   ```bash
   cd /Users/norrisa/Documents/dev/github/CTS285_FA22/tool-booksense
   source toolvenv/bin/activate
   ```

2. Start the application:
   ```bash
   cd streamlit_example
   streamlit run openlibrary_app_with_export.py
   ```

3. Clear any existing books from the collection (for a clean demo)

## Introduction (User - Project Lead)

"Today we're presenting BookSense, a comprehensive book management application developed by our team. BookSense allows users to search for books, build personal collections, and manage their reading habits."

"Let me introduce our team members and their contributions:
- I served as the Project Lead, guiding the vision and requirements
- Claude was our Technical Architect, implementing the core functionality
- Goofus focused on rapid feature development
- Gallant ensured code quality and testing

Now, let's walk through the main features of the application."

## Demo Section 1: Search & Discovery (Claude - Technical Architect)

"The first major feature of BookSense is the ability to search for books using the Open Library API."

1. Show the search form in the sidebar
2. Explain the different search types (title, author, subject, ISBN)
3. Perform a search for "The Great Gatsby"
4. Point out the search results showing book covers and information
5. Expand the "More Details" section to show additional book information
6. Click "Add to Collection" for a book to demonstrate adding to the collection

"This search functionality showcases our Open Library API integration. The service handles API requests, caching responses for performance, and processing the results into a user-friendly format."

## Demo Section 2: Collection Management (Goofus - Pragmatic Developer)

"Now that we've added some books to our collection, let's see how BookSense helps users manage their books."

1. Navigate to the "My Collection" tab
2. Show the list of books in the collection
3. Demonstrate the filtering options:
   - Filter by reading status
   - Filter by minimum rating
   - Sort by different fields
4. Select a book to show the detailed view
5. Change the reading status and rating
6. Click "Update Book" to save changes
7. Show the updated book in the collection

"I focused on making these features practical and user-friendly, ensuring users can quickly manage their reading habits. The interface gives immediate feedback and provides intuitive controls for collection management."

## Demo Section 3: Import & Export (Gallant - Quality Specialist)

"One of the most important aspects of any collection app is the ability to back up and restore your data. Let's look at our import and export functionality."

1. Navigate to the "Import/Export" tab
2. Show the export options:
   - Select JSON format
   - Show the preview
   - Point out the download link
   - Switch to CSV format and repeat
3. Demonstrate the import functionality:
   - Click "Generate Sample JSON" to create sample data
   - Show the preview of the generated data
   - Click "Import Sample Data"
4. Return to the "My Collection" tab to show the imported books

"These features were implemented with careful attention to detail and robust error handling. We ensure data integrity throughout the export and import process, and provide clear feedback to the user."

## Technical Overview (Claude - Technical Architect)

"Let me briefly explain the architecture behind BookSense:"

1. Show a diagram of the modular architecture
2. Highlight the separation of concerns:
   - Core functionality (models, storage, operations)
   - User interfaces (Streamlit)
   - API integration (Open Library)
3. Explain the storage factory pattern:
   - Abstract interface for storage
   - Multiple backend implementations (JSON, SQLite)
   - Seamless switching between backends

"This architecture allows for flexibility and future expansion. We can add new interfaces or storage backends without changing the core functionality."

## Testing Philosophy (User - Project Lead)

"Our team took an interesting approach to testing, showcasing two different philosophies:"

1. Explain Goofus's practical testing approach:
   - Focus on functionality
   - Quick feedback loop
   - Testing what users actually use

2. Explain Gallant's comprehensive testing approach:
   - Mock external dependencies
   - Test edge cases
   - High code coverage
   - Documentation as tests

"By combining these approaches, we achieved both rapid development and high quality."

## Conclusion and Future Plans (User - Project Lead)

"BookSense has successfully achieved all our MVP requirements, but we have exciting plans for the future:"

1. Outline future interfaces:
   - Command-line interface
   - RESTful API
   - Desktop GUI

2. Describe planned features:
   - Book recommendations
   - Reading progress tracking
   - Social sharing

"Thank you for watching our presentation. We're now happy to answer any questions about BookSense or our development process."

## Q&A Preparation

Be prepared to answer questions about:
- The technical implementation
- The team collaboration process
- Challenges faced during development
- How specific features work
- Future development plans