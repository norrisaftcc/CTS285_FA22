#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
models.py - Data models for Dataman application

This module defines the core data models used throughout the Dataman application,
including the Problem class which represents a math problem.
"""
from typing import Dict, List, Union, Optional
import json

class Problem:
    """
    Represents a mathematical problem with operands, operator, and answer.
    
    Attributes:
        first (int): First operand in the math problem
        operator (str): Mathematical operator ('+', '-', '*', '/')
        second (int): Second operand in the math problem
        answer (int): The answer to the math problem
        user_answer (Optional[int]): User-provided answer, if any
    """
    
    VALID_OPERATORS = ['+', '-', '*', '/']
    
    def __init__(self, first: int, operator: str, second: int, answer: Optional[int] = None):
        """
        Initialize a Problem with operands and operator.
        
        Args:
            first (int): First operand in the math problem
            operator (str): Mathematical operator ('+', '-', '*', '/')
            second (int): Second operand in the math problem
            answer (Optional[int]): The answer to the problem, if known
        
        Raises:
            ValueError: If the operator is not valid
        """
        self.first = first
        if operator not in self.VALID_OPERATORS:
            raise ValueError(f"Invalid operator: {operator}. Must be one of {self.VALID_OPERATORS}")
        self.operator = operator
        self.second = second
        self.answer = answer if answer is not None else self.solve()
        self.user_answer = None
    
    def __str__(self) -> str:
        """
        Return a string representation of the problem.
        
        Returns:
            str: String representation in the format "a op b = c"
        """
        return f"{self.first} {self.operator} {self.second} = {self.answer}"
    
    def show_problem_to_solve(self) -> str:
        """
        Return a string with the problem to be solved (without answer).
        
        Returns:
            str: String representation in the format "a op b = ?"
        """
        return f"{self.first} {self.operator} {self.second} = ?"
    
    def solve(self) -> int:
        """
        Calculate the correct answer to the problem.
        
        Returns:
            int: The calculated answer
            
        Raises:
            ZeroDivisionError: If attempting to divide by zero
        """
        if self.operator == "+":
            return self.first + self.second
        elif self.operator == "-":
            return self.first - self.second
        elif self.operator == "*":
            return self.first * self.second
        elif self.operator == "/":
            if self.second == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return self.first // self.second
    
    def check_answer(self, provided_answer: int) -> bool:
        """
        Check if a provided answer is correct.
        
        Args:
            provided_answer (int): The answer to check
            
        Returns:
            bool: True if the provided answer is correct, False otherwise
        """
        self.user_answer = provided_answer
        return self.solve() == provided_answer
    
    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Convert the problem to a dictionary for storage.
        
        Returns:
            Dict[str, Union[int, str]]: Dictionary representation of the problem
        """
        return {
            "first": self.first,
            "operator": self.operator,
            "second": self.second,
            "answer": self.answer,
            "user_answer": self.user_answer
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Union[int, str]]) -> 'Problem':
        """
        Create a Problem instance from a dictionary.
        
        Args:
            data (Dict[str, Union[int, str]]): Dictionary representation of a problem
            
        Returns:
            Problem: New Problem instance
        """
        problem = cls(
            first=data["first"],
            operator=data["operator"],
            second=data["second"],
            answer=data["answer"]
        )
        problem.user_answer = data.get("user_answer")
        return problem

    @classmethod
    def from_string(cls, problem_string: str) -> 'Problem':
        """
        Parse a problem string in the format "a op b = c".
        
        Args:
            problem_string (str): String representation of a problem
            
        Returns:
            Problem: New Problem instance
            
        Raises:
            ValueError: If the problem string is not in the expected format
        """
        try:
            parts = problem_string.split()
            if len(parts) != 5 or parts[3] != "=":
                raise ValueError()
            
            first = int(parts[0])
            operator = parts[1]
            second = int(parts[2])
            answer = int(parts[4])
            
            return cls(first, operator, second, answer)
        except (ValueError, IndexError):
            raise ValueError(f"Invalid problem format: {problem_string}. Expected format: 'a op b = c'")


class ProblemSet:
    """
    Represents a collection of related math problems.
    
    Attributes:
        name (str): Name of the problem set
        problems (List[Problem]): List of problems in the set
        description (Optional[str]): Optional description of the problem set
    """
    
    def __init__(self, name: str, problems: Optional[List[Problem]] = None, description: Optional[str] = None):
        """
        Initialize a problem set with a name and optional list of problems.
        
        Args:
            name (str): Name of the problem set
            problems (Optional[List[Problem]]): Initial list of problems
            description (Optional[str]): Description of the problem set
        """
        self.name = name
        self.problems = problems or []
        self.description = description
    
    def add_problem(self, problem: Problem) -> None:
        """
        Add a problem to the set.
        
        Args:
            problem (Problem): Problem to add
        """
        self.problems.append(problem)
    
    def remove_problem(self, index: int) -> Problem:
        """
        Remove a problem from the set by index.
        
        Args:
            index (int): Index of the problem to remove
            
        Returns:
            Problem: The removed problem
            
        Raises:
            IndexError: If index is out of range
        """
        return self.problems.pop(index)
    
    def to_dict(self) -> Dict:
        """
        Convert the problem set to a dictionary for storage.
        
        Returns:
            Dict: Dictionary representation of the problem set
        """
        return {
            "name": self.name,
            "description": self.description,
            "problems": [p.to_dict() for p in self.problems]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProblemSet':
        """
        Create a ProblemSet instance from a dictionary.
        
        Args:
            data (Dict): Dictionary representation of a problem set
            
        Returns:
            ProblemSet: New ProblemSet instance
        """
        problems = [Problem.from_dict(p) for p in data.get("problems", [])]
        return cls(
            name=data["name"],
            problems=problems,
            description=data.get("description")
        )