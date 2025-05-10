#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
user_history.py - User history tracking for the Dataman application

This module provides functionality for tracking and persisting user history, 
including session information, completed problems, performance metrics, and achievements.
"""
import json
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

class UserHistory:
    """
    Tracks and persists user history for the Dataman application.
    
    Attributes:
        user_id (str): Unique identifier for the user
        history_file (str): Path to the history JSON file
        history (Dict): Dictionary containing user history data
    """
    
    def __init__(self, user_id: Optional[str] = None, history_file: Optional[str] = None):
        """
        Initialize user history tracking.
        
        Args:
            user_id (Optional[str]): Unique identifier for the user, generates one if not provided
            history_file (Optional[str]): Path to the history file, uses default if not provided
        """
        self.user_id = user_id or self._generate_user_id()
        self.history_file = history_file or self._get_default_history_file()
        self.history = self._load_history()
        
        # Initialize history if it's empty
        if not self.history:
            self.history = {
                "user_id": self.user_id,
                "created_at": datetime.now().isoformat(),
                "sessions": [],
                "problem_sets": {},
                "completed_problems": [],
                "statistics": {
                    "total_problems_attempted": 0,
                    "total_problems_correct": 0,
                    "by_operator": {},
                    "by_difficulty": {},
                    "average_time_per_problem": 0
                },
                "achievements": [],
                "last_login": None
            }
            self._initialize_operator_stats()
            self._initialize_difficulty_stats()
            self.save_history()
    
    def _generate_user_id(self) -> str:
        """
        Generate a unique user ID.
        
        Returns:
            str: A unique identifier
        """
        return str(uuid.uuid4())
    
    def _get_default_history_file(self) -> str:
        """
        Get the default path for the history file.
        
        Returns:
            str: Path to the default history file
        """
        home_dir = os.path.expanduser("~")
        dataman_dir = os.path.join(home_dir, ".dataman")
        
        # Create directory if it doesn't exist
        os.makedirs(dataman_dir, exist_ok=True)
        
        return os.path.join(dataman_dir, "user_history.json")
    
    def _load_history(self) -> Dict:
        """
        Load history from the history file.
        
        Returns:
            Dict: User history data
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_history(self) -> bool:
        """
        Save history to the history file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            return True
        except IOError:
            return False
    
    def _initialize_operator_stats(self) -> None:
        """Initialize statistics for each operator."""
        for operator in ["+", "-", "*", "/"]:
            self.history["statistics"]["by_operator"][operator] = {
                "attempted": 0,
                "correct": 0,
                "average_time": 0
            }
    
    def _initialize_difficulty_stats(self) -> None:
        """Initialize statistics for each difficulty level."""
        for difficulty in ["easy", "medium", "hard"]:
            self.history["statistics"]["by_difficulty"][difficulty] = {
                "attempted": 0,
                "correct": 0,
                "average_time": 0
            }
    
    def start_session(self) -> str:
        """
        Start a new user session.
        
        Returns:
            str: Session ID
        """
        session_id = str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "problems_attempted": 0,
            "problems_correct": 0,
            "problem_sets_used": []
        }
        
        self.history["sessions"].append(session)
        self.history["last_login"] = datetime.now().isoformat()
        self.save_history()
        
        return session_id
    
    def end_session(self, session_id: str) -> bool:
        """
        End a user session.
        
        Args:
            session_id (str): ID of the session to end
            
        Returns:
            bool: True if successful, False if session not found
        """
        for session in self.history["sessions"]:
            if session["session_id"] == session_id:
                session["end_time"] = datetime.now().isoformat()
                self.save_history()
                return True
        return False
    
    def track_problem_attempt(self, 
                             problem_dict: Dict, 
                             is_correct: bool, 
                             time_taken: float,
                             session_id: Optional[str] = None,
                             problem_set_name: Optional[str] = None,
                             difficulty: str = "easy") -> None:
        """
        Track a problem attempt in the user history.
        
        Args:
            problem_dict (Dict): Dictionary representation of the problem
            is_correct (bool): Whether the user's answer was correct
            time_taken (float): Time taken to solve the problem in seconds
            session_id (Optional[str]): Session ID, if tracking within a session
            problem_set_name (Optional[str]): Name of the problem set, if applicable
            difficulty (str): Difficulty level of the problem
        """
        # Record the problem attempt
        attempt = {
            "timestamp": datetime.now().isoformat(),
            "problem": problem_dict,
            "is_correct": is_correct,
            "time_taken": time_taken,
            "session_id": session_id,
            "problem_set_name": problem_set_name,
            "difficulty": difficulty
        }
        
        self.history["completed_problems"].append(attempt)
        
        # Update overall statistics
        self.history["statistics"]["total_problems_attempted"] += 1
        if is_correct:
            self.history["statistics"]["total_problems_correct"] += 1
        
        # Update operator statistics
        operator = problem_dict["operator"]
        self.history["statistics"]["by_operator"][operator]["attempted"] += 1
        if is_correct:
            self.history["statistics"]["by_operator"][operator]["correct"] += 1
        
        # Update time statistics
        current_avg = self.history["statistics"]["by_operator"][operator]["average_time"]
        attempted = self.history["statistics"]["by_operator"][operator]["attempted"]
        new_avg = ((current_avg * (attempted - 1)) + time_taken) / attempted
        self.history["statistics"]["by_operator"][operator]["average_time"] = new_avg
        
        # Update difficulty statistics
        self.history["statistics"]["by_difficulty"][difficulty]["attempted"] += 1
        if is_correct:
            self.history["statistics"]["by_difficulty"][difficulty]["correct"] += 1
        
        current_avg = self.history["statistics"]["by_difficulty"][difficulty]["average_time"]
        attempted = self.history["statistics"]["by_difficulty"][difficulty]["attempted"]
        new_avg = ((current_avg * (attempted - 1)) + time_taken) / attempted
        self.history["statistics"]["by_difficulty"][difficulty]["average_time"] = new_avg
        
        # Update overall average time
        total_attempted = self.history["statistics"]["total_problems_attempted"]
        current_overall_avg = self.history["statistics"]["average_time_per_problem"]
        new_overall_avg = ((current_overall_avg * (total_attempted - 1)) + time_taken) / total_attempted
        self.history["statistics"]["average_time_per_problem"] = new_overall_avg
        
        # Update session statistics if provided
        if session_id:
            for session in self.history["sessions"]:
                if session["session_id"] == session_id:
                    session["problems_attempted"] += 1
                    if is_correct:
                        session["problems_correct"] += 1
                    if problem_set_name and problem_set_name not in session["problem_sets_used"]:
                        session["problem_sets_used"].append(problem_set_name)
                    break
        
        # Update problem set statistics if provided
        if problem_set_name:
            if problem_set_name not in self.history["problem_sets"]:
                self.history["problem_sets"][problem_set_name] = {
                    "attempts": 0,
                    "correct": 0,
                    "last_used": None
                }
            
            self.history["problem_sets"][problem_set_name]["attempts"] += 1
            if is_correct:
                self.history["problem_sets"][problem_set_name]["correct"] += 1
            self.history["problem_sets"][problem_set_name]["last_used"] = datetime.now().isoformat()
        
        # Check for achievements
        self._check_achievements()
        
        # Save the updated history
        self.save_history()
    
    def _check_achievements(self) -> None:
        """Check and update user achievements based on history."""
        achievements = []
        
        # First problem attempted
        if self.history["statistics"]["total_problems_attempted"] == 1:
            achievements.append({
                "id": "first_problem",
                "name": "First Steps",
                "description": "Attempted your first problem",
                "earned_at": datetime.now().isoformat()
            })
        
        # First problem correct
        if self.history["statistics"]["total_problems_correct"] == 1:
            achievements.append({
                "id": "first_correct",
                "name": "Math Novice",
                "description": "Solved your first problem correctly",
                "earned_at": datetime.now().isoformat()
            })
        
        # 10 problems correct
        if self.history["statistics"]["total_problems_correct"] == 10:
            achievements.append({
                "id": "ten_correct",
                "name": "Math Apprentice",
                "description": "Solved 10 problems correctly",
                "earned_at": datetime.now().isoformat()
            })
        
        # 50 problems correct
        if self.history["statistics"]["total_problems_correct"] == 50:
            achievements.append({
                "id": "fifty_correct",
                "name": "Math Expert",
                "description": "Solved 50 problems correctly",
                "earned_at": datetime.now().isoformat()
            })
        
        # 100 problems correct
        if self.history["statistics"]["total_problems_correct"] == 100:
            achievements.append({
                "id": "hundred_correct",
                "name": "Math Master",
                "description": "Solved 100 problems correctly",
                "earned_at": datetime.now().isoformat()
            })
        
        # Perfect score in a drill (check last 20 problems)
        if len(self.history["completed_problems"]) >= 10:
            last_ten = self.history["completed_problems"][-10:]
            if all(p["is_correct"] for p in last_ten):
                # Check if this achievement already exists
                if not any(a["id"] == "perfect_ten" for a in self.history["achievements"]):
                    achievements.append({
                        "id": "perfect_ten",
                        "name": "Perfect Ten",
                        "description": "Solved 10 problems in a row correctly",
                        "earned_at": datetime.now().isoformat()
                    })
        
        # Add new achievements to history
        for achievement in achievements:
            if not any(a["id"] == achievement["id"] for a in self.history["achievements"]):
                self.history["achievements"].append(achievement)
    
    def get_user_stats(self) -> Dict:
        """
        Get user statistics.
        
        Returns:
            Dict: Dictionary with user statistics
        """
        return self.history["statistics"]
    
    def get_recent_problems(self, limit: int = 10) -> List[Dict]:
        """
        Get the most recently completed problems.
        
        Args:
            limit (int): Maximum number of problems to return
            
        Returns:
            List[Dict]: List of recent problem attempts
        """
        return self.history["completed_problems"][-limit:]
    
    def get_achievements(self) -> List[Dict]:
        """
        Get user achievements.
        
        Returns:
            List[Dict]: List of earned achievements
        """
        return self.history["achievements"]
    
    def get_problem_set_stats(self, name: str) -> Optional[Dict]:
        """
        Get statistics for a specific problem set.
        
        Args:
            name (str): Name of the problem set
            
        Returns:
            Optional[Dict]: Statistics for the problem set, or None if not found
        """
        return self.history["problem_sets"].get(name)
    
    def get_learning_suggestions(self) -> Dict[str, List[str]]:
        """
        Get learning suggestions based on user performance.
        
        Returns:
            Dict[str, List[str]]: Dictionary with suggestions by category
        """
        suggestions = {
            "operators": [],
            "difficulty": [],
            "general": []
        }
        
        # Check operator performance
        for operator, stats in self.history["statistics"]["by_operator"].items():
            if stats["attempted"] > 0:
                accuracy = stats["correct"] / stats["attempted"] * 100
                if accuracy < 60:
                    op_name = {"+": "addition", "-": "subtraction", "*": "multiplication", "/": "division"}[operator]
                    suggestions["operators"].append(f"Practice more {op_name} problems")
        
        # Check difficulty performance
        for difficulty, stats in self.history["statistics"]["by_difficulty"].items():
            if stats["attempted"] > 0:
                accuracy = stats["correct"] / stats["attempted"] * 100
                if difficulty == "easy" and accuracy > 90 and stats["attempted"] >= 20:
                    suggestions["difficulty"].append("Try some medium difficulty problems")
                elif difficulty == "medium" and accuracy > 90 and stats["attempted"] >= 20:
                    suggestions["difficulty"].append("Try some hard difficulty problems")
                elif difficulty == "hard" and accuracy < 50 and stats["attempted"] >= 5:
                    suggestions["difficulty"].append("Practice more medium difficulty problems before hard ones")
        
        # General suggestions
        total_problems = self.history["statistics"]["total_problems_attempted"]
        if total_problems < 10:
            suggestions["general"].append("Complete more problems to get personalized suggestions")
        else:
            # Check for inactivity
            if self.history["sessions"] and len(self.history["sessions"]) > 1:
                last_session = self.history["sessions"][-1]
                if last_session["end_time"]:
                    last_active = datetime.fromisoformat(last_session["end_time"])
                    now = datetime.now()
                    days_since_active = (now - last_active).days
                    if days_since_active > 7:
                        suggestions["general"].append(f"It's been {days_since_active} days since your last session. Regular practice helps build math skills!")
        
        return suggestions


class UserHistorySingleton:
    """
    Singleton class to ensure only one instance of UserHistory exists.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls, user_id: Optional[str] = None, history_file: Optional[str] = None) -> UserHistory:
        """
        Get the singleton instance of UserHistory.
        
        Args:
            user_id (Optional[str]): User ID to use if creating a new instance
            history_file (Optional[str]): History file path to use if creating a new instance
            
        Returns:
            UserHistory: The singleton instance
        """
        if cls._instance is None:
            cls._instance = UserHistory(user_id, history_file)
        return cls._instance


def track_problem_with_timer(problem_dict: Dict, 
                            session_id: Optional[str] = None, 
                            problem_set_name: Optional[str] = None,
                            difficulty: str = "easy") -> Dict:
    """
    Helper function to track a problem attempt with timing.
    
    Args:
        problem_dict (Dict): Dictionary representation of the problem
        session_id (Optional[str]): Session ID, if tracking within a session
        problem_set_name (Optional[str]): Name of the problem set, if applicable
        difficulty (str): Difficulty level of the problem
        
    Returns:
        Dict: Dictionary with timer functions
    """
    start_time = None
    user_history = UserHistorySingleton.get_instance()
    
    def start():
        nonlocal start_time
        start_time = time.time()
    
    def stop(is_correct: bool):
        if start_time is None:
            raise ValueError("Timer was not started")
        
        time_taken = time.time() - start_time
        user_history.track_problem_attempt(
            problem_dict=problem_dict,
            is_correct=is_correct,
            time_taken=time_taken,
            session_id=session_id,
            problem_set_name=problem_set_name,
            difficulty=difficulty
        )
        return time_taken
    
    return {
        "start": start,
        "stop": stop
    }