#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py - Utility functions for the Dataman application

This module provides utility functions used throughout the Dataman application.
"""
import os
import random
from typing import List, Optional, Tuple

from .models import Problem


def parse_problem_string(problem_string: str) -> Tuple[int, str, int, Optional[int]]:
    """
    Parse a problem string in the format "a op b = c" or "a op b = ?".
    
    Args:
        problem_string (str): String representation of a problem
        
    Returns:
        Tuple[int, str, int, Optional[int]]: Tuple of (first, operator, second, answer)
        
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
        
        # Parse answer if provided, otherwise None
        answer = None
        if parts[4] != "?":
            answer = int(parts[4])
        
        return first, operator, second, answer
    except (ValueError, IndexError):
        raise ValueError(f"Invalid problem format: {problem_string}. Expected format: 'a op b = c' or 'a op b = ?'")


def generate_timed_drill(num_problems: int = 20, 
                         difficulty: str = 'easy', 
                         operators: Optional[List[str]] = None) -> List[Problem]:
    """
    Generate a timed drill with the specified number of problems.
    
    Args:
        num_problems (int): Number of problems to generate
        difficulty (str): Difficulty level ('easy', 'medium', 'hard')
        operators (Optional[List[str]]): List of operators to use
        
    Returns:
        List[Problem]: List of generated problems
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
    
    problems = []
    
    for _ in range(num_problems):
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
        problem = Problem(first, operator, second)
        problems.append(problem)
    
    return problems


def format_time(seconds: int) -> str:
    """
    Format time in seconds as MM:SS.
    
    Args:
        seconds (int): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def get_default_storage_path(storage_type: str) -> str:
    """
    Get the default storage path for the given storage type.
    
    Args:
        storage_type (str): Type of storage ('json', 'sqlite')
        
    Returns:
        str: Default path for the storage type
        
    Raises:
        ValueError: If storage_type is not valid
    """
    home_dir = os.path.expanduser("~")
    dataman_dir = os.path.join(home_dir, ".dataman")
    
    # Create directory if it doesn't exist
    os.makedirs(dataman_dir, exist_ok=True)
    
    if storage_type == 'json':
        return os.path.join(dataman_dir, "dataman.json")
    elif storage_type == 'sqlite':
        return os.path.join(dataman_dir, "dataman.db")
    else:
        raise ValueError(f"Invalid storage type: {storage_type}")