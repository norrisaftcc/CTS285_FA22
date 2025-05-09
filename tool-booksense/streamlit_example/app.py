import streamlit as st
import pandas as pd
import numpy as np

st.title('BookSense Example App')

st.write("""
# BookSense Simple Demo
This is a simple example Streamlit application for the BookSense tool project.
""")

# Create a sample book database
books_data = {
    'Title': ['To Kill a Mockingbird', '1984', 'The Great Gatsby', 
              'Pride and Prejudice', 'The Catcher in the Rye'],
    'Author': ['Harper Lee', 'George Orwell', 'F. Scott Fitzgerald', 
               'Jane Austen', 'J.D. Salinger'],
    'Year': [1960, 1949, 1925, 1813, 1951],
    'Rating': [4.27, 4.19, 3.93, 4.25, 3.81]
}

df = pd.DataFrame(books_data)

# Display the book database
st.subheader('Book Database')
st.dataframe(df)

# Add a filter for books
st.sidebar.header('Filters')
min_year = st.sidebar.slider('Minimum Publication Year', 
                             min_value=int(df['Year'].min()),
                             max_value=int(df['Year'].max()),
                             value=int(df['Year'].min()))

filtered_df = df[df['Year'] >= min_year]
st.subheader(f'Books published since {min_year}')
st.dataframe(filtered_df)

# Add a chart
st.subheader('Book Ratings')
fig = st.bar_chart(df.set_index('Title')['Rating'])

# Add a form to add a new book
st.subheader('Add a New Book')
with st.form("new_book_form"):
    new_title = st.text_input('Title')
    new_author = st.text_input('Author')
    new_year = st.number_input('Publication Year', min_value=1000, max_value=2023, step=1)
    new_rating = st.slider('Rating', min_value=1.0, max_value=5.0, step=0.1)
    
    submitted = st.form_submit_button("Add Book")
    if submitted:
        st.success(f"Added '{new_title}' by {new_author} (Note: In this demo, books aren't actually saved)")

# Extra information section
st.subheader('About this Demo')
st.info("""
This is a simple Streamlit demo for the BookSense tool project. 
Streamlit makes it easy to create data-focused web applications with Python.
To run this app, use: `streamlit run app.py`
""")