#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_operations.py - Tests for the operations module

This module contains unit tests for the operations module.
"""
import unittest
import os
import tempfile
from unittest.mock import MagicMock

from dataman.core.models import Problem, ProblemSet
from dataman.core.operations import DatamanOperations
from dataman.core.storage import JSONStorage


class TestDatamanOperations(unittest.TestCase):
    """Tests for the DatamanOperations class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for storage
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        
        # Create a storage instance
        self.storage = JSONStorage(self.file_path)
        
        # Create operations instance
        self.operations = DatamanOperations(self.storage)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary file
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
    
    def test_create_problem_set(self):
        """Test creating a problem set."""
        problem_set = self.operations.create_problem_set("Test Set", "Test description")
        self.assertEqual(problem_set.name, "Test Set")
        self.assertEqual(problem_set.description, "Test description")
        self.assertEqual(problem_set.problems, [])
        self.assertEqual(self.operations.current_problem_set, problem_set)
    
    def test_load_problem_set(self):
        """Test loading a problem set."""
        # Create a problem set
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)], "Test description")
        self.storage.save_problem_set(problem_set)
        
        # Load the problem set
        loaded_set = self.operations.load_problem_set("Test Set")
        self.assertEqual(loaded_set.name, "Test Set")
        self.assertEqual(loaded_set.description, "Test description")
        self.assertEqual(len(loaded_set.problems), 1)
        self.assertEqual(loaded_set.problems[0].first, 2)
        self.assertEqual(loaded_set.problems[0].operator, "+")
        self.assertEqual(loaded_set.problems[0].second, 2)
        self.assertEqual(loaded_set.problems[0].answer, 4)
        self.assertEqual(self.operations.current_problem_set, loaded_set)
    
    def test_load_problem_set_not_found(self):
        """Test loading a non-existent problem set."""
        loaded_set = self.operations.load_problem_set("Nonexistent Set")
        self.assertIsNone(loaded_set)
    
    def test_save_current_problem_set(self):
        """Test saving the current problem set."""
        # Create a problem set
        problem_set = self.operations.create_problem_set("Test Set", "Test description")
        problem_set.add_problem(Problem(2, "+", 2))
        
        # Save the problem set
        result = self.operations.save_current_problem_set()
        self.assertTrue(result)
        
        # Verify the problem set was saved
        self.assertIn("Test Set", self.storage.list_problem_sets())
    
    def test_save_current_problem_set_no_set(self):
        """Test saving when there is no current problem set."""
        self.operations.current_problem_set = None
        result = self.operations.save_current_problem_set()
        self.assertFalse(result)
    
    def test_list_problem_sets(self):
        """Test listing problem sets."""
        # Create some problem sets
        sets = ["Set 1", "Set 2", "Set 3"]
        for name in sets:
            problem_set = ProblemSet(name)
            self.storage.save_problem_set(problem_set)
        
        # List the problem sets
        result = self.operations.list_problem_sets()
        for name in sets:
            self.assertIn(name, result)
    
    def test_add_problem(self):
        """Test adding a problem to the current problem set."""
        # Create a problem set
        self.operations.create_problem_set("Test Set")
        
        # Add a problem
        problem = Problem(2, "+", 2)
        result = self.operations.add_problem(problem)
        self.assertTrue(result)
        self.assertEqual(self.operations.current_problem_set.problems, [problem])
    
    def test_add_problem_no_set(self):
        """Test adding a problem when there is no current problem set."""
        self.operations.current_problem_set = None
        problem = Problem(2, "+", 2)
        result = self.operations.add_problem(problem)
        self.assertFalse(result)
    
    def test_remove_problem(self):
        """Test removing a problem from the current problem set."""
        # Create a problem set with problems
        self.operations.create_problem_set("Test Set")
        problem1 = Problem(2, "+", 2)
        problem2 = Problem(3, "*", 4)
        self.operations.add_problem(problem1)
        self.operations.add_problem(problem2)
        
        # Remove a problem
        removed = self.operations.remove_problem(0)
        self.assertEqual(removed, problem1)
        self.assertEqual(self.operations.current_problem_set.problems, [problem2])
    
    def test_remove_problem_no_set(self):
        """Test removing a problem when there is no current problem set."""
        self.operations.current_problem_set = None
        result = self.operations.remove_problem(0)
        self.assertIsNone(result)
    
    def test_get_current_problems(self):
        """Test getting problems from the current problem set."""
        # Create a problem set with problems
        self.operations.create_problem_set("Test Set")
        problem1 = Problem(2, "+", 2)
        problem2 = Problem(3, "*", 4)
        self.operations.add_problem(problem1)
        self.operations.add_problem(problem2)
        
        # Get the problems
        problems = self.operations.get_current_problems()
        self.assertEqual(problems, [problem1, problem2])
    
    def test_get_current_problems_no_set(self):
        """Test getting problems when there is no current problem set."""
        self.operations.current_problem_set = None
        problems = self.operations.get_current_problems()
        self.assertEqual(problems, [])
    
    def test_check_answer(self):
        """Test checking an answer for a problem."""
        # Create a problem set with a problem
        self.operations.create_problem_set("Test Set")
        self.operations.add_problem(Problem(2, "+", 2))
        
        # Check a correct answer
        result = self.operations.check_answer(0, 4)
        self.assertTrue(result)
        
        # Check an incorrect answer
        result = self.operations.check_answer(0, 5)
        self.assertFalse(result)
    
    def test_check_answer_no_set(self):
        """Test checking an answer when there is no current problem set."""
        self.operations.current_problem_set = None
        with self.assertRaises(ValueError):
            self.operations.check_answer(0, 4)
    
    def test_check_answer_invalid_index(self):
        """Test checking an answer with an invalid problem index."""
        self.operations.create_problem_set("Test Set")
        self.operations.add_problem(Problem(2, "+", 2))
        
        with self.assertRaises(IndexError):
            self.operations.check_answer(1, 4)
    
    def test_generate_random_problem(self):
        """Test generating a random problem."""
        problem = self.operations.generate_random_problem()
        self.assertIsInstance(problem, Problem)
        self.assertIn(problem.operator, ["+", "-", "*", "/"])
    
    def test_generate_random_problem_with_options(self):
        """Test generating a random problem with specific options."""
        problem = self.operations.generate_random_problem("medium", ["+", "-"])
        self.assertIsInstance(problem, Problem)
        self.assertIn(problem.operator, ["+", "-"])
    
    def test_generate_random_problem_invalid_difficulty(self):
        """Test generating a random problem with an invalid difficulty."""
        with self.assertRaises(ValueError):
            self.operations.generate_random_problem("invalid")
    
    def test_generate_problem_set(self):
        """Test generating a problem set with random problems."""
        problem_set = self.operations.generate_problem_set(
            "Random Set", 5, "easy", ["+"], "Random problems"
        )
        
        self.assertEqual(problem_set.name, "Random Set")
        self.assertEqual(problem_set.description, "Random problems")
        self.assertEqual(len(problem_set.problems), 5)
        
        for problem in problem_set.problems:
            self.assertEqual(problem.operator, "+")
    
    def test_get_statistics_no_set(self):
        """Test getting statistics when there is no current problem set."""
        self.operations.current_problem_set = None
        stats = self.operations.get_statistics()
        self.assertEqual(stats["total_problems"], 0)
        self.assertEqual(stats["attempted"], 0)
        self.assertEqual(stats["correct"], 0)
        self.assertEqual(stats["accuracy"], 0.0)
        self.assertEqual(stats["by_operator"], {})
    
    def test_get_statistics(self):
        """Test getting statistics for a problem set."""
        # Create a problem set with problems
        self.operations.create_problem_set("Test Set")
        
        # Add some problems with user answers
        problem1 = Problem(2, "+", 2)
        problem1.check_answer(4)  # Correct
        
        problem2 = Problem(3, "-", 2)
        problem2.check_answer(0)  # Incorrect
        
        problem3 = Problem(3, "*", 4)
        problem3.check_answer(12)  # Correct
        
        problem4 = Problem(10, "/", 2)
        # No answer
        
        self.operations.add_problem(problem1)
        self.operations.add_problem(problem2)
        self.operations.add_problem(problem3)
        self.operations.add_problem(problem4)
        
        # Get statistics
        stats = self.operations.get_statistics()
        
        self.assertEqual(stats["total_problems"], 4)
        self.assertEqual(stats["attempted"], 3)
        self.assertEqual(stats["correct"], 2)
        self.assertEqual(stats["accuracy"], 2/3 * 100)
        
        # Check operator stats
        self.assertEqual(len(stats["by_operator"]), 4)  # All operators should be included
        
        # Addition
        self.assertEqual(stats["by_operator"]["+"]["total"], 1)
        self.assertEqual(stats["by_operator"]["+"]["attempted"], 1)
        self.assertEqual(stats["by_operator"]["+"]["correct"], 1)
        self.assertEqual(stats["by_operator"]["+"]["accuracy"], 100.0)
        
        # Subtraction
        self.assertEqual(stats["by_operator"]["-"]["total"], 1)
        self.assertEqual(stats["by_operator"]["-"]["attempted"], 1)
        self.assertEqual(stats["by_operator"]["-"]["correct"], 0)
        self.assertEqual(stats["by_operator"]["-"]["accuracy"], 0.0)
        
        # Multiplication
        self.assertEqual(stats["by_operator"]["*"]["total"], 1)
        self.assertEqual(stats["by_operator"]["*"]["attempted"], 1)
        self.assertEqual(stats["by_operator"]["*"]["correct"], 1)
        self.assertEqual(stats["by_operator"]["*"]["accuracy"], 100.0)
        
        # Division
        self.assertEqual(stats["by_operator"]["/"]["total"], 1)
        self.assertEqual(stats["by_operator"]["/"]["attempted"], 0)
        self.assertEqual(stats["by_operator"]["/"]["correct"], 0)
        self.assertEqual(stats["by_operator"]["/"]["accuracy"], 0.0)


if __name__ == "__main__":
    unittest.main()