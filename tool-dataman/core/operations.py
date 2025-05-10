#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
operations.py - Core operations for Dataman application

This module provides the core business logic and operations for 
the Dataman application, including problem management and validation.
"""
import random
from typing import Dict, List, Optional, Tuple, Union

from .models import Problem, ProblemSet
from .storage import StorageInterface


class DatamanOperations:
    """Core operations for the Dataman application."""
    
    def __init__(self, storage: StorageInterface):
        """
        Initialize operations with a storage backend.
        
        Args:
            storage (StorageInterface): Storage implementation for persistence
        """
        self.storage = storage
        self.current_problem_set = None
    
    def create_problem_set(self, name: str, description: Optional[str] = None) -> ProblemSet:
        """
        Create a new problem set.
        
        Args:
            name (str): Name of the problem set
            description (Optional[str]): Description of the problem set
            
        Returns:
            ProblemSet: The newly created problem set
        """
        problem_set = ProblemSet(name=name, description=description)
        self.current_problem_set = problem_set
        return problem_set
    
    def load_problem_set(self, name: str) -> Optional[ProblemSet]:
        """
        Load a problem set from storage.
        
        Args:
            name (str): Name of the problem set to load
            
        Returns:
            Optional[ProblemSet]: The loaded problem set or None if not found
        """
        problem_set = self.storage.load_problem_set(name)
        if problem_set:
            self.current_problem_set = problem_set
        return problem_set
    
    def save_current_problem_set(self) -> bool:
        """
        Save the current problem set to storage.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.current_problem_set:
            return False
        return self.storage.save_problem_set(self.current_problem_set)
    
    def list_problem_sets(self) -> List[str]:
        """
        List all available problem sets.
        
        Returns:
            List[str]: List of problem set names
        """
        return self.storage.list_problem_sets()
    
    def add_problem(self, problem: Problem) -> bool:
        """
        Add a problem to the current problem set.
        
        Args:
            problem (Problem): The problem to add
            
        Returns:
            bool: True if successful, False if no current problem set
        """
        if not self.current_problem_set:
            return False
        self.current_problem_set.add_problem(problem)
        return True
    
    def remove_problem(self, index: int) -> Optional[Problem]:
        """
        Remove a problem from the current problem set by index.
        
        Args:
            index (int): Index of the problem to remove
            
        Returns:
            Optional[Problem]: The removed problem or None if no current problem set
            
        Raises:
            IndexError: If the index is out of range
        """
        if not self.current_problem_set:
            return None
        return self.current_problem_set.remove_problem(index)
    
    def get_current_problems(self) -> List[Problem]:
        """
        Get all problems in the current problem set.
        
        Returns:
            List[Problem]: List of problems or empty list if no current problem set
        """
        if not self.current_problem_set:
            return []
        return self.current_problem_set.problems
    
    def check_answer(self, problem_index: int, answer: int) -> bool:
        """
        Check if an answer is correct for a specific problem.
        
        Args:
            problem_index (int): Index of the problem
            answer (int): The answer to check
            
        Returns:
            bool: True if the answer is correct, False otherwise
            
        Raises:
            IndexError: If the problem index is out of range
            ValueError: If no current problem set
        """
        if not self.current_problem_set:
            raise ValueError("No problem set loaded")
        
        if problem_index < 0 or problem_index >= len(self.current_problem_set.problems):
            raise IndexError(f"Problem index {problem_index} out of range")
        
        problem = self.current_problem_set.problems[problem_index]
        return problem.check_answer(answer)
    
    def generate_random_problem(self, 
                               difficulty: str = 'easy',
                               operators: Optional[List[str]] = None) -> Problem:
        """
        Generate a random math problem based on difficulty.
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
            operators (Optional[List[str]]): List of operators to use, defaults to all
            
        Returns:
            Problem: A randomly generated problem
            
        Raises:
            ValueError: If difficulty is invalid
        """
        if operators is None:
            operators = ['+', '-', '*', '/']
        
        # Define range of operands based on difficulty
        if difficulty == 'easy':
            range_first = (1, 10)
            range_second = (1, 10)
        elif difficulty == 'medium':
            range_first = (10, 50)
            range_second = (1, 20)
        elif difficulty == 'hard':
            range_first = (50, 100)
            range_second = (1, 50)
        else:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        
        # Generate random operands and operator
        first = random.randint(*range_first)
        operator = random.choice(operators)
        
        # For division, ensure we have a divisible number
        if operator == '/':
            # Generate a divisor that divides evenly into first
            divisors = [i for i in range(1, min(range_second[1] + 1, first + 1)) if first % i == 0]
            if not divisors:
                # If no divisors in range, use 1
                second = 1
            else:
                second = random.choice(divisors)
        else:
            second = random.randint(*range_second)
        
        # Create problem (answer will be calculated automatically)
        return Problem(first, operator, second)
    
    def generate_problem_set(self, 
                            name: str,
                            num_problems: int = 10,
                            difficulty: str = 'easy',
                            operators: Optional[List[str]] = None,
                            description: Optional[str] = None) -> ProblemSet:
        """
        Generate a problem set with random problems.
        
        Args:
            name (str): Name of the problem set
            num_problems (int): Number of problems to generate
            difficulty (str): Difficulty level
            operators (Optional[List[str]]): List of operators to use
            description (Optional[str]): Description of the problem set
            
        Returns:
            ProblemSet: The generated problem set
        """
        problem_set = self.create_problem_set(name, description)
        
        for _ in range(num_problems):
            problem = self.generate_random_problem(difficulty, operators)
            problem_set.add_problem(problem)
        
        self.current_problem_set = problem_set
        return problem_set
    
    def get_statistics(self) -> Dict[str, Union[int, float]]:
        """
        Get statistics for the current problem set.
        
        Returns:
            Dict[str, Union[int, float]]: Dictionary with statistics
        """
        if not self.current_problem_set or not self.current_problem_set.problems:
            return {
                "total_problems": 0,
                "attempted": 0,
                "correct": 0,
                "accuracy": 0.0,
                "by_operator": {}
            }
        
        total = len(self.current_problem_set.problems)
        attempted = sum(1 for p in self.current_problem_set.problems if p.user_answer is not None)
        correct = sum(1 for p in self.current_problem_set.problems 
                    if p.user_answer is not None and p.user_answer == p.solve())
        
        # Accuracy percentage
        accuracy = (correct / attempted * 100) if attempted > 0 else 0.0
        
        # Statistics by operator
        by_operator = {}
        for op in Problem.VALID_OPERATORS:
            op_problems = [p for p in self.current_problem_set.problems if p.operator == op]
            op_attempted = sum(1 for p in op_problems if p.user_answer is not None)
            op_correct = sum(1 for p in op_problems 
                           if p.user_answer is not None and p.user_answer == p.solve())
            op_accuracy = (op_correct / op_attempted * 100) if op_attempted > 0 else 0.0
            
            by_operator[op] = {
                "total": len(op_problems),
                "attempted": op_attempted,
                "correct": op_correct,
                "accuracy": op_accuracy
            }
        
        return {
            "total_problems": total,
            "attempted": attempted,
            "correct": correct,
            "accuracy": accuracy,
            "by_operator": by_operator
        }