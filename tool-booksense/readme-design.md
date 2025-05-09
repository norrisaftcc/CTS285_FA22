# readme-design.md

# overall design

BookSense is a simple tool designed to look up and recommend books in a modular fashion. Its design goals are:
- provide an easy to follow template for how to access a REST API resource
- provide an example of MCP level AI code generation

# components

the division of labor is according to the usual three level application design pattern.

user interface: two versions. A full featured Streamlit program, and a simple console based GUI that leverages the automated testing libraries

mid layer: business logic layer. does the thinking. organizes multiple objects together. probably consists mostly of a library with useful methods, which are used by both user interfaces and the test scaffold.

data layer: simple sqlite db is fine, unless you think something like json file storage is better for some things. use ORM so that the mid layer is working with object level abstractions, business logic layer should never have to refer to SQL commands directly.

# requirements

as a user, i'd like to be able to look up books on the open library REST API so that i can find books.

as a user, i'd like the system to be able to store my liked books in an internal database.

as a user, i'd like to be able to log in.

as a user, i'd like to be able to register.

as a user, i'd like the system to recommend me books based on other books I like. 

