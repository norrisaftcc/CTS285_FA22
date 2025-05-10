#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_storage.py - Tests for the storage module

This module contains unit tests for the storage module.
"""
import unittest
import os
import tempfile
import json
import sqlite3

from dataman.core.models import Problem, ProblemSet
from dataman.core.storage import JSONStorage
from dataman.core.storage_sqlite import SQLiteStorage


class TestJSONStorage(unittest.TestCase):
    """Tests for the JSONStorage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        
        # Create a storage instance
        self.storage = JSONStorage(self.file_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary file
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    
    def test_init_new_file(self):
        """Test initialization with a new file."""
        self.assertTrue(os.path.exists(self.file_path))
        
        # Check that the file has the correct structure
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        self.assertIn("problem_sets", data)
        self.assertEqual(data["problem_sets"], {})
    
    def test_init_existing_file(self):
        """Test initialization with an existing file."""
        # Create a file with some data
        data = {
            "problem_sets": {
                "Test Set": {
                    "name": "Test Set",
                    "description": "Test description",
                    "problems": []
                }
            }
        }
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f)
        
        # Create a new storage instance
        storage = JSONStorage(self.file_path)
        
        # Check that the data was loaded correctly
        self.assertIn("Test Set", storage.data["problem_sets"])
    
    def test_save_problem_set(self):
        """Test saving a problem set."""
        # Create a problem set
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)], "Test description")
        
        # Save the problem set
        result = self.storage.save_problem_set(problem_set)
        self.assertTrue(result)
        
        # Check that the problem set was saved correctly
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        self.assertIn("Test Set", data["problem_sets"])
        saved_set = data["problem_sets"]["Test Set"]
        self.assertEqual(saved_set["name"], "Test Set")
        self.assertEqual(saved_set["description"], "Test description")
        self.assertEqual(len(saved_set["problems"]), 1)
        
        saved_problem = saved_set["problems"][0]
        self.assertEqual(saved_problem["first"], 2)
        self.assertEqual(saved_problem["operator"], "+")
        self.assertEqual(saved_problem["second"], 2)
        self.assertEqual(saved_problem["answer"], 4)
    
    def test_load_problem_set(self):
        """Test loading a problem set."""
        # Create a problem set
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)], "Test description")
        
        # Save the problem set
        self.storage.save_problem_set(problem_set)
        
        # Load the problem set
        loaded_set = self.storage.load_problem_set("Test Set")
        
        # Check that the problem set was loaded correctly
        self.assertIsNotNone(loaded_set)
        self.assertEqual(loaded_set.name, "Test Set")
        self.assertEqual(loaded_set.description, "Test description")
        self.assertEqual(len(loaded_set.problems), 1)
        
        loaded_problem = loaded_set.problems[0]
        self.assertEqual(loaded_problem.first, 2)
        self.assertEqual(loaded_problem.operator, "+")
        self.assertEqual(loaded_problem.second, 2)
        self.assertEqual(loaded_problem.answer, 4)
    
    def test_load_problem_set_not_found(self):
        """Test loading a non-existent problem set."""
        loaded_set = self.storage.load_problem_set("Nonexistent Set")
        self.assertIsNone(loaded_set)
    
    def test_delete_problem_set(self):
        """Test deleting a problem set."""
        # Create some problem sets
        set1 = ProblemSet("Set 1", [Problem(2, "+", 2)])
        set2 = ProblemSet("Set 2", [Problem(3, "*", 4)])
        
        # Save the problem sets
        self.storage.save_problem_set(set1)
        self.storage.save_problem_set(set2)
        
        # Delete one problem set
        result = self.storage.delete_problem_set("Set 1")
        self.assertTrue(result)
        
        # Check that the problem set was deleted
        self.assertNotIn("Set 1", self.storage.list_problem_sets())
        self.assertIn("Set 2", self.storage.list_problem_sets())
    
    def test_delete_problem_set_not_found(self):
        """Test deleting a non-existent problem set."""
        result = self.storage.delete_problem_set("Nonexistent Set")
        self.assertFalse(result)
    
    def test_list_problem_sets(self):
        """Test listing problem sets."""
        # Create some problem sets
        sets = ["Set 1", "Set 2", "Set 3"]
        for name in sets:
            problem_set = ProblemSet(name)
            self.storage.save_problem_set(problem_set)
        
        # List the problem sets
        result = self.storage.list_problem_sets()
        
        # Check that all problem sets are listed
        self.assertCountEqual(result, sets)


class TestSQLiteStorage(unittest.TestCase):
    """Tests for the SQLiteStorage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        os.remove(self.db_path)  # SQLite will create the file
        
        # Create a storage instance
        self.storage = SQLiteStorage(self.db_path)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary file
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_init(self):
        """Test initialization."""
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check that the tables were created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check problem_sets table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='problem_sets'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Check problems table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='problems'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
    
    def test_save_problem_set(self):
        """Test saving a problem set."""
        # Create a problem set
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)], "Test description")
        
        # Save the problem set
        result = self.storage.save_problem_set(problem_set)
        self.assertTrue(result)
        
        # Check that the problem set was saved correctly
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check problem set
        cursor.execute("SELECT name, description FROM problem_sets WHERE name=?", ("Test Set",))
        problem_set_data = cursor.fetchone()
        self.assertIsNotNone(problem_set_data)
        self.assertEqual(problem_set_data[0], "Test Set")
        self.assertEqual(problem_set_data[1], "Test description")
        
        # Check problem
        cursor.execute(
            "SELECT first, operator, second, answer FROM problems WHERE problem_set_name=?",
            ("Test Set",)
        )
        problem_data = cursor.fetchone()
        self.assertIsNotNone(problem_data)
        self.assertEqual(problem_data[0], 2)
        self.assertEqual(problem_data[1], "+")
        self.assertEqual(problem_data[2], 2)
        self.assertEqual(problem_data[3], 4)
        
        conn.close()
    
    def test_load_problem_set(self):
        """Test loading a problem set."""
        # Create a problem set
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)], "Test description")
        
        # Save the problem set
        self.storage.save_problem_set(problem_set)
        
        # Load the problem set
        loaded_set = self.storage.load_problem_set("Test Set")
        
        # Check that the problem set was loaded correctly
        self.assertIsNotNone(loaded_set)
        self.assertEqual(loaded_set.name, "Test Set")
        self.assertEqual(loaded_set.description, "Test description")
        self.assertEqual(len(loaded_set.problems), 1)
        
        loaded_problem = loaded_set.problems[0]
        self.assertEqual(loaded_problem.first, 2)
        self.assertEqual(loaded_problem.operator, "+")
        self.assertEqual(loaded_problem.second, 2)
        self.assertEqual(loaded_problem.answer, 4)
    
    def test_load_problem_set_not_found(self):
        """Test loading a non-existent problem set."""
        loaded_set = self.storage.load_problem_set("Nonexistent Set")
        self.assertIsNone(loaded_set)
    
    def test_delete_problem_set(self):
        """Test deleting a problem set."""
        # Create some problem sets
        set1 = ProblemSet("Set 1", [Problem(2, "+", 2)])
        set2 = ProblemSet("Set 2", [Problem(3, "*", 4)])
        
        # Save the problem sets
        self.storage.save_problem_set(set1)
        self.storage.save_problem_set(set2)
        
        # Delete one problem set
        result = self.storage.delete_problem_set("Set 1")
        self.assertTrue(result)
        
        # Check that the problem set was deleted
        self.assertNotIn("Set 1", self.storage.list_problem_sets())
        self.assertIn("Set 2", self.storage.list_problem_sets())
        
        # Check that the problems were also deleted
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM problems WHERE problem_set_name=?", ("Set 1",))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)
        conn.close()
    
    def test_delete_problem_set_not_found(self):
        """Test deleting a non-existent problem set."""
        result = self.storage.delete_problem_set("Nonexistent Set")
        self.assertFalse(result)
    
    def test_list_problem_sets(self):
        """Test listing problem sets."""
        # Create some problem sets
        sets = ["Set 1", "Set 2", "Set 3"]
        for name in sets:
            problem_set = ProblemSet(name)
            self.storage.save_problem_set(problem_set)
        
        # List the problem sets
        result = self.storage.list_problem_sets()
        
        # Check that all problem sets are listed
        self.assertCountEqual(result, sets)


if __name__ == "__main__":
    unittest.main()