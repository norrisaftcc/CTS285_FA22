#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core_usage.py - Example demonstrating core functionality of the Dataman package

This script demonstrates how to use the core functionality of the Dataman package,
including creating problems, problem sets, and using different storage backends.
"""
import os
import tempfile

from dataman.core.models import Problem, ProblemSet
from dataman.core.storage import JSONStorage
from dataman.core.storage_sqlite import SQLiteStorage
from dataman.core.storage_factory import StorageFactory
from dataman.core.operations import DatamanOperations


def create_problems_example():
    """Example of creating and working with Problem objects."""
    print("\n=== Creating and Working with Problems ===")
    
    # Create problems with different operators
    addition = Problem(2, "+", 2)
    subtraction = Problem(5, "-", 3)
    multiplication = Problem(3, "*", 4)
    division = Problem(10, "/", 2)
    
    # Print the problems
    print(f"Addition: {addition}")
    print(f"Subtraction: {subtraction}")
    print(f"Multiplication: {multiplication}")
    print(f"Division: {division}")
    
    # Show problems to solve
    print(f"\nAddition to solve: {addition.show_problem_to_solve()}")
    
    # Check answers
    print(f"\nChecking answers:")
    print(f"Is 4 the correct answer to {addition.show_problem_to_solve()}? {addition.check_answer(4)}")
    print(f"Is 5 the correct answer to {addition.show_problem_to_solve()}? {addition.check_answer(5)}")
    
    # Create a problem from a string
    problem_string = "7 + 3 = 10"
    problem = Problem.from_string(problem_string)
    print(f"\nProblem from string '{problem_string}': {problem}")
    
    return addition, subtraction, multiplication, division


def create_problem_set_example(problems):
    """Example of creating and working with ProblemSet objects."""
    print("\n=== Creating and Working with Problem Sets ===")
    
    # Create a problem set
    problem_set = ProblemSet("Math Practice", problems, "A set of practice problems")
    
    # Print information about the problem set
    print(f"Problem set name: {problem_set.name}")
    print(f"Problem set description: {problem_set.description}")
    print(f"Number of problems: {len(problem_set.problems)}")
    
    # Add a new problem
    new_problem = Problem(6, "+", 7)
    problem_set.add_problem(new_problem)
    print(f"\nAdded a new problem: {new_problem}")
    print(f"Number of problems now: {len(problem_set.problems)}")
    
    # Remove a problem
    removed = problem_set.remove_problem(0)
    print(f"\nRemoved problem: {removed}")
    print(f"Number of problems now: {len(problem_set.problems)}")
    
    return problem_set


def json_storage_example(problem_set):
    """Example of using JSONStorage."""
    print("\n=== Using JSON Storage ===")
    
    # Create a temporary file for storage
    fd, file_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        # Create a JSON storage instance
        storage = JSONStorage(file_path)
        
        # Save the problem set
        storage.save_problem_set(problem_set)
        print(f"Saved problem set '{problem_set.name}' to {file_path}")
        
        # List problem sets
        problem_sets = storage.list_problem_sets()
        print(f"Available problem sets: {problem_sets}")
        
        # Load the problem set
        loaded_set = storage.load_problem_set(problem_set.name)
        print(f"Loaded problem set: {loaded_set.name}")
        print(f"Number of problems: {len(loaded_set.problems)}")
        
        # Delete the problem set
        storage.delete_problem_set(problem_set.name)
        print(f"Deleted problem set '{problem_set.name}'")
        problem_sets = storage.list_problem_sets()
        print(f"Available problem sets now: {problem_sets}")
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)


def sqlite_storage_example(problem_set):
    """Example of using SQLiteStorage."""
    print("\n=== Using SQLite Storage ===")
    
    # Create a temporary file for storage
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(db_path)  # SQLite will create the file
    
    try:
        # Create a SQLite storage instance
        storage = SQLiteStorage(db_path)
        
        # Save the problem set
        storage.save_problem_set(problem_set)
        print(f"Saved problem set '{problem_set.name}' to {db_path}")
        
        # List problem sets
        problem_sets = storage.list_problem_sets()
        print(f"Available problem sets: {problem_sets}")
        
        # Load the problem set
        loaded_set = storage.load_problem_set(problem_set.name)
        print(f"Loaded problem set: {loaded_set.name}")
        print(f"Number of problems: {len(loaded_set.problems)}")
        
        # Delete the problem set
        storage.delete_problem_set(problem_set.name)
        print(f"Deleted problem set '{problem_set.name}'")
        problem_sets = storage.list_problem_sets()
        print(f"Available problem sets now: {problem_sets}")
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.remove(db_path)


def storage_factory_example():
    """Example of using StorageFactory."""
    print("\n=== Using Storage Factory ===")
    
    # Get available storage types
    storage_types = StorageFactory.get_available_storage_types()
    print(f"Available storage types: {storage_types}")
    
    # Create temporary files for storage
    fd_json, json_path = tempfile.mkstemp(suffix=".json")
    os.close(fd_json)
    
    fd_sqlite, sqlite_path = tempfile.mkstemp(suffix=".db")
    os.close(fd_sqlite)
    os.remove(sqlite_path)  # SQLite will create the file
    
    try:
        # Create storage instances using the factory
        json_storage = StorageFactory.create_storage("json", file_path=json_path)
        print(f"Created JSON storage at {json_path}")
        
        sqlite_storage = StorageFactory.create_storage("sqlite", db_path=sqlite_path)
        print(f"Created SQLite storage at {sqlite_path}")
        
        # Try to create an invalid storage type
        try:
            StorageFactory.create_storage("invalid")
        except ValueError as e:
            print(f"Expected error: {e}")
    finally:
        # Clean up
        if os.path.exists(json_path):
            os.remove(json_path)
        if os.path.exists(sqlite_path):
            os.remove(sqlite_path)


def operations_example():
    """Example of using DatamanOperations."""
    print("\n=== Using DatamanOperations ===")
    
    # Create a temporary file for storage
    fd, file_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    try:
        # Create a storage instance and operations
        storage = JSONStorage(file_path)
        operations = DatamanOperations(storage)
        
        # Create a problem set
        problem_set = operations.create_problem_set("Practice Set", "A set for practice")
        print(f"Created problem set: {problem_set.name}")
        
        # Add some problems
        problem1 = Problem(2, "+", 2)
        problem2 = Problem(3, "*", 4)
        operations.add_problem(problem1)
        operations.add_problem(problem2)
        print(f"Added problems to the problem set")
        
        # Save the problem set
        operations.save_current_problem_set()
        print(f"Saved problem set to storage")
        
        # Generate a random problem
        random_problem = operations.generate_random_problem("easy", ["+", "-"])
        print(f"Generated random problem: {random_problem}")
        
        # Generate a random problem set
        random_set = operations.generate_problem_set(
            "Random Set", 5, "medium", ["+", "-", "*"], "Randomly generated problems"
        )
        operations.save_current_problem_set()
        print(f"Generated random problem set '{random_set.name}' with {len(random_set.problems)} problems")
        
        # Check an answer
        result = operations.check_answer(0, 4)
        print(f"Is 4 the correct answer to problem 1? {result}")
        
        # Get statistics
        stats = operations.get_statistics()
        print(f"\nStatistics:")
        print(f"Total problems: {stats['total_problems']}")
        print(f"Attempted: {stats['attempted']}")
        print(f"Correct: {stats['correct']}")
        print(f"Accuracy: {stats['accuracy']:.1f}%")
        
        # List all problem sets
        problem_sets = operations.list_problem_sets()
        print(f"\nAvailable problem sets: {problem_sets}")
        
        # Load another problem set
        operations.load_problem_set("Random Set")
        print(f"Loaded problem set: {operations.current_problem_set.name}")
        print(f"Number of problems: {len(operations.current_problem_set.problems)}")
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)


def main():
    """Main function to run all examples."""
    print("=== Dataman Core Usage Examples ===")
    
    # Run examples
    problems = create_problems_example()
    problem_set = create_problem_set_example(problems)
    json_storage_example(problem_set)
    sqlite_storage_example(problem_set)
    storage_factory_example()
    operations_example()
    
    print("\n=== All Examples Completed ===")


if __name__ == "__main__":
    main()