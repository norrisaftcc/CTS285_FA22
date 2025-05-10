#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_models.py - Tests for the models module

This module contains unit tests for the models module.
"""
import unittest
from dataman.core.models import Problem, ProblemSet


class TestProblem(unittest.TestCase):
    """Tests for the Problem class."""
    
    def test_init(self):
        """Test that a Problem object can be created."""
        problem = Problem(2, "+", 2)
        self.assertEqual(problem.first, 2)
        self.assertEqual(problem.operator, "+")
        self.assertEqual(problem.second, 2)
        self.assertEqual(problem.answer, 4)
        self.assertIsNone(problem.user_answer)
    
    def test_init_with_answer(self):
        """Test that a Problem object can be created with a specific answer."""
        problem = Problem(2, "+", 2, 4)
        self.assertEqual(problem.answer, 4)
    
    def test_str(self):
        """Test the string representation of a Problem."""
        problem = Problem(2, "+", 2)
        self.assertEqual(str(problem), "2 + 2 = 4")
    
    def test_show_problem_to_solve(self):
        """Test the problem representation for solving."""
        problem = Problem(2, "+", 2)
        self.assertEqual(problem.show_problem_to_solve(), "2 + 2 = ?")
    
    def test_solve_addition(self):
        """Test solving an addition problem."""
        problem = Problem(2, "+", 2)
        self.assertEqual(problem.solve(), 4)
    
    def test_solve_subtraction(self):
        """Test solving a subtraction problem."""
        problem = Problem(5, "-", 3)
        self.assertEqual(problem.solve(), 2)
    
    def test_solve_multiplication(self):
        """Test solving a multiplication problem."""
        problem = Problem(3, "*", 4)
        self.assertEqual(problem.solve(), 12)
    
    def test_solve_division(self):
        """Test solving a division problem."""
        problem = Problem(10, "/", 2)
        self.assertEqual(problem.solve(), 5)
    
    def test_solve_division_by_zero(self):
        """Test that dividing by zero raises a ZeroDivisionError."""
        problem = Problem(10, "/", 0)
        with self.assertRaises(ZeroDivisionError):
            problem.solve()
    
    def test_invalid_operator(self):
        """Test that an invalid operator raises a ValueError."""
        with self.assertRaises(ValueError):
            Problem(2, "^", 2)
    
    def test_check_answer(self):
        """Test checking an answer."""
        problem = Problem(2, "+", 2)
        self.assertTrue(problem.check_answer(4))
        self.assertFalse(problem.check_answer(5))
        self.assertEqual(problem.user_answer, 5)
    
    def test_to_dict(self):
        """Test converting a Problem to a dictionary."""
        problem = Problem(2, "+", 2)
        problem.user_answer = 4
        expected = {
            "first": 2,
            "operator": "+",
            "second": 2,
            "answer": 4,
            "user_answer": 4
        }
        self.assertEqual(problem.to_dict(), expected)
    
    def test_from_dict(self):
        """Test creating a Problem from a dictionary."""
        data = {
            "first": 2,
            "operator": "+",
            "second": 2,
            "answer": 4,
            "user_answer": 4
        }
        problem = Problem.from_dict(data)
        self.assertEqual(problem.first, 2)
        self.assertEqual(problem.operator, "+")
        self.assertEqual(problem.second, 2)
        self.assertEqual(problem.answer, 4)
        self.assertEqual(problem.user_answer, 4)
    
    def test_from_string(self):
        """Test creating a Problem from a string."""
        problem = Problem.from_string("2 + 2 = 4")
        self.assertEqual(problem.first, 2)
        self.assertEqual(problem.operator, "+")
        self.assertEqual(problem.second, 2)
        self.assertEqual(problem.answer, 4)
    
    def test_from_string_invalid(self):
        """Test that an invalid string raises a ValueError."""
        with self.assertRaises(ValueError):
            Problem.from_string("2 + 2")
        
        with self.assertRaises(ValueError):
            Problem.from_string("2 + 2 == 4")


class TestProblemSet(unittest.TestCase):
    """Tests for the ProblemSet class."""
    
    def test_init(self):
        """Test that a ProblemSet object can be created."""
        problem_set = ProblemSet("Test Set")
        self.assertEqual(problem_set.name, "Test Set")
        self.assertEqual(problem_set.problems, [])
        self.assertIsNone(problem_set.description)
    
    def test_init_with_problems_and_description(self):
        """Test that a ProblemSet object can be created with problems and description."""
        problems = [Problem(2, "+", 2), Problem(3, "*", 4)]
        problem_set = ProblemSet("Test Set", problems, "Test description")
        self.assertEqual(problem_set.name, "Test Set")
        self.assertEqual(problem_set.problems, problems)
        self.assertEqual(problem_set.description, "Test description")
    
    def test_add_problem(self):
        """Test adding a problem to a ProblemSet."""
        problem_set = ProblemSet("Test Set")
        problem = Problem(2, "+", 2)
        problem_set.add_problem(problem)
        self.assertEqual(problem_set.problems, [problem])
    
    def test_remove_problem(self):
        """Test removing a problem from a ProblemSet."""
        problem1 = Problem(2, "+", 2)
        problem2 = Problem(3, "*", 4)
        problem_set = ProblemSet("Test Set", [problem1, problem2])
        
        removed = problem_set.remove_problem(0)
        self.assertEqual(removed, problem1)
        self.assertEqual(problem_set.problems, [problem2])
    
    def test_remove_problem_invalid_index(self):
        """Test that removing a problem with an invalid index raises an IndexError."""
        problem_set = ProblemSet("Test Set", [Problem(2, "+", 2)])
        with self.assertRaises(IndexError):
            problem_set.remove_problem(1)
    
    def test_to_dict(self):
        """Test converting a ProblemSet to a dictionary."""
        problem1 = Problem(2, "+", 2)
        problem2 = Problem(3, "*", 4)
        problem_set = ProblemSet("Test Set", [problem1, problem2], "Test description")
        
        expected = {
            "name": "Test Set",
            "description": "Test description",
            "problems": [problem1.to_dict(), problem2.to_dict()]
        }
        self.assertEqual(problem_set.to_dict(), expected)
    
    def test_from_dict(self):
        """Test creating a ProblemSet from a dictionary."""
        data = {
            "name": "Test Set",
            "description": "Test description",
            "problems": [
                {
                    "first": 2,
                    "operator": "+",
                    "second": 2,
                    "answer": 4,
                    "user_answer": None
                },
                {
                    "first": 3,
                    "operator": "*",
                    "second": 4,
                    "answer": 12,
                    "user_answer": None
                }
            ]
        }
        
        problem_set = ProblemSet.from_dict(data)
        self.assertEqual(problem_set.name, "Test Set")
        self.assertEqual(problem_set.description, "Test description")
        self.assertEqual(len(problem_set.problems), 2)
        self.assertEqual(problem_set.problems[0].first, 2)
        self.assertEqual(problem_set.problems[0].operator, "+")
        self.assertEqual(problem_set.problems[0].second, 2)
        self.assertEqual(problem_set.problems[0].answer, 4)
        self.assertEqual(problem_set.problems[1].first, 3)
        self.assertEqual(problem_set.problems[1].operator, "*")
        self.assertEqual(problem_set.problems[1].second, 4)
        self.assertEqual(problem_set.problems[1].answer, 12)


if __name__ == "__main__":
    unittest.main()