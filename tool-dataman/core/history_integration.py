#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
history_integration.py - Integration of user history with Dataman operations

This module provides decorators and helper functions to integrate user history
tracking with the Dataman application's operations.
"""
import time
import functools
from typing import Callable, Any, Dict, Optional, Union

from .models import Problem, ProblemSet
from .user_history import UserHistorySingleton, track_problem_with_timer


def with_history_tracking(session_id: Optional[str] = None):
    """
    Decorator to add history tracking to problem checking operations.
    
    Args:
        session_id (Optional[str]): Active session ID, if any
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract problem and other relevant info
            self = args[0]  # 'self' from the method
            
            # Get problem and expected answer
            problem_index = kwargs.get('problem_index', args[1] if len(args) > 1 else None)
            answer = kwargs.get('answer', args[2] if len(args) > 2 else None)
            
            if problem_index is None or answer is None:
                # If we can't determine the arguments, just call the original function
                return func(*args, **kwargs)
            
            # Get the problem from the current problem set
            if not self.current_problem_set or problem_index >= len(self.current_problem_set.problems):
                return func(*args, **kwargs)
            
            problem = self.current_problem_set.problems[problem_index]
            problem_set_name = self.current_problem_set.name
            
            # Call the original function with timing
            start_time = time.time()
            result = func(*args, **kwargs)
            time_taken = time.time() - start_time
            
            # Track the attempt
            user_history = UserHistorySingleton.get_instance()
            user_history.track_problem_attempt(
                problem_dict=problem.to_dict(),
                is_correct=result,
                time_taken=time_taken,
                session_id=session_id,
                problem_set_name=problem_set_name
            )
            
            return result
        return wrapper
    return decorator


def with_timed_drill(func: Callable):
    """
    Decorator to track timed drill performance.
    
    Args:
        func (Callable): The function to decorate
        
    Returns:
        Callable: Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_history = UserHistorySingleton.get_instance()
        session_id = user_history.start_session()
        
        # Call the original function
        result = func(*args, **kwargs)
        
        # End the session
        user_history.end_session(session_id)
        
        return result
    return wrapper


class HistoryAwareOperations:
    """
    Mixin class to add history tracking to operations.
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the mixin.
        
        Args:
            session_id (Optional[str]): Active session ID, if any
        """
        self.user_history = UserHistorySingleton.get_instance()
        self.session_id = session_id or self.user_history.start_session()
    
    def end_session(self):
        """End the current session."""
        if self.session_id:
            self.user_history.end_session(self.session_id)
            self.session_id = None
    
    def track_problem(self, problem: Problem, is_correct: bool, time_taken: float):
        """
        Track a problem attempt.
        
        Args:
            problem (Problem): The problem that was attempted
            is_correct (bool): Whether the answer was correct
            time_taken (float): Time taken to solve the problem in seconds
        """
        problem_set_name = getattr(self, 'current_problem_set', None)
        problem_set_name = problem_set_name.name if problem_set_name else None
        
        self.user_history.track_problem_attempt(
            problem_dict=problem.to_dict(),
            is_correct=is_correct,
            time_taken=time_taken,
            session_id=self.session_id,
            problem_set_name=problem_set_name
        )
    
    def get_user_stats(self):
        """
        Get user statistics.
        
        Returns:
            Dict: User statistics
        """
        return self.user_history.get_user_stats()
    
    def get_recent_problems(self, limit: int = 10):
        """
        Get the most recently completed problems.
        
        Args:
            limit (int): Maximum number of problems to return
            
        Returns:
            List[Dict]: List of recent problem attempts
        """
        return self.user_history.get_recent_problems(limit)
    
    def get_achievements(self):
        """
        Get user achievements.
        
        Returns:
            List[Dict]: List of earned achievements
        """
        return self.user_history.get_achievements()
    
    def get_learning_suggestions(self):
        """
        Get learning suggestions based on user performance.
        
        Returns:
            Dict[str, List[str]]: Dictionary with suggestions by category
        """
        return self.user_history.get_learning_suggestions()
    
    def get_problem_set_stats(self, name: str):
        """
        Get statistics for a specific problem set.
        
        Args:
            name (str): Name of the problem set
            
        Returns:
            Optional[Dict]: Statistics for the problem set, or None if not found
        """
        return self.user_history.get_problem_set_stats(name)