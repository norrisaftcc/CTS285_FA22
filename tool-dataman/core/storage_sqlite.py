#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storage_sqlite.py - SQLite storage implementation

This module provides a SQLite implementation of the storage interface
for the Dataman application.
"""
import os
import sqlite3
from typing import Dict, List, Optional, Union

from .models import Problem, ProblemSet
from .storage import StorageInterface


class SQLiteStorage(StorageInterface):
    """Implementation of StorageInterface using SQLite database."""
    
    def __init__(self, db_path: str):
        """
        Initialize SQLite storage with a database path.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_db()
    
    def _get_connection(self):
        """
        Get a connection to the SQLite database.
        
        Returns:
            sqlite3.Connection: Database connection
        """
        return sqlite3.connect(self.db_path)
    
    def _initialize_db(self):
        """Create the necessary tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create problem sets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS problem_sets (
            name TEXT PRIMARY KEY,
            description TEXT
        )
        ''')
        
        # Create problems table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_set_name TEXT,
            first INTEGER,
            operator TEXT,
            second INTEGER,
            answer INTEGER,
            user_answer INTEGER,
            FOREIGN KEY (problem_set_name) REFERENCES problem_sets (name) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_problem_set(self, problem_set: ProblemSet) -> bool:
        """
        Save a problem set to SQLite storage.
        
        Args:
            problem_set (ProblemSet): The problem set to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if problem set already exists
            cursor.execute("SELECT name FROM problem_sets WHERE name=?", (problem_set.name,))
            exists = cursor.fetchone()
            
            if exists:
                # Update problem set
                cursor.execute(
                    "UPDATE problem_sets SET description=? WHERE name=?",
                    (problem_set.description, problem_set.name)
                )
                # Delete existing problems for this set
                cursor.execute("DELETE FROM problems WHERE problem_set_name=?", (problem_set.name,))
            else:
                # Insert new problem set
                cursor.execute(
                    "INSERT INTO problem_sets (name, description) VALUES (?, ?)",
                    (problem_set.name, problem_set.description)
                )
            
            # Insert problems
            for problem in problem_set.problems:
                cursor.execute(
                    "INSERT INTO problems (problem_set_name, first, operator, second, answer, user_answer) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        problem_set.name,
                        problem.first,
                        problem.operator,
                        problem.second,
                        problem.answer,
                        problem.user_answer
                    )
                )
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def load_problem_set(self, name: str) -> Optional[ProblemSet]:
        """
        Load a problem set from SQLite storage by name.
        
        Args:
            name (str): Name of the problem set to load
            
        Returns:
            Optional[ProblemSet]: The loaded problem set, or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get problem set
            cursor.execute("SELECT name, description FROM problem_sets WHERE name=?", (name,))
            problem_set_data = cursor.fetchone()
            
            if not problem_set_data:
                conn.close()
                return None
            
            # Get problems for this set
            cursor.execute(
                "SELECT first, operator, second, answer, user_answer FROM problems WHERE problem_set_name=?",
                (name,)
            )
            problem_rows = cursor.fetchall()
            
            # Create problem set
            problem_set = ProblemSet(
                name=problem_set_data[0],
                description=problem_set_data[1]
            )
            
            # Add problems
            for row in problem_rows:
                problem = Problem(
                    first=row[0],
                    operator=row[1],
                    second=row[2],
                    answer=row[3]
                )
                problem.user_answer = row[4]
                problem_set.add_problem(problem)
            
            conn.close()
            return problem_set
        except sqlite3.Error:
            return None
    
    def delete_problem_set(self, name: str) -> bool:
        """
        Delete a problem set from SQLite storage.
        
        Args:
            name (str): Name of the problem set to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if problem set exists
            cursor.execute("SELECT name FROM problem_sets WHERE name=?", (name,))
            exists = cursor.fetchone()
            
            if not exists:
                conn.close()
                return False
            
            # Delete problem set and its problems (cascade delete will handle the problems)
            cursor.execute("DELETE FROM problem_sets WHERE name=?", (name,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    
    def list_problem_sets(self) -> List[str]:
        """
        List all available problem sets in SQLite storage.
        
        Returns:
            List[str]: List of problem set names
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM problem_sets")
            problem_sets = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            return problem_sets
        except sqlite3.Error:
            return []