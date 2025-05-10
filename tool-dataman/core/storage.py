#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storage.py - Base storage interface and JSON implementation

This module defines the storage interface and JSON implementation 
for the Dataman application's data persistence.
"""
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from .models import Problem, ProblemSet


class StorageInterface(ABC):
    """Abstract base class that defines the storage interface."""
    
    @abstractmethod
    def save_problem_set(self, problem_set: ProblemSet) -> bool:
        """
        Save a problem set to storage.
        
        Args:
            problem_set (ProblemSet): The problem set to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def load_problem_set(self, name: str) -> Optional[ProblemSet]:
        """
        Load a problem set from storage by name.
        
        Args:
            name (str): Name of the problem set to load
            
        Returns:
            Optional[ProblemSet]: The loaded problem set, or None if not found
        """
        pass
    
    @abstractmethod
    def delete_problem_set(self, name: str) -> bool:
        """
        Delete a problem set from storage.
        
        Args:
            name (str): Name of the problem set to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_problem_sets(self) -> List[str]:
        """
        List all available problem sets.
        
        Returns:
            List[str]: List of problem set names
        """
        pass


class JSONStorage(StorageInterface):
    """Implementation of StorageInterface using JSON files."""
    
    def __init__(self, file_path: str):
        """
        Initialize JSON storage with a file path.
        
        Args:
            file_path (str): Path to the JSON file
        """
        self.file_path = file_path
        self.data = self._load_or_create_storage()
    
    def _load_or_create_storage(self) -> Dict:
        """
        Load existing data or create new storage.
        
        Returns:
            Dict: The loaded or newly created data
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is invalid or can't be read, create new storage
                return {"problem_sets": {}}
        else:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            # Return empty data structure
            return {"problem_sets": {}}
    
    def _save_storage(self) -> bool:
        """
        Save the current data to the JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except IOError:
            return False
    
    def save_problem_set(self, problem_set: ProblemSet) -> bool:
        """
        Save a problem set to JSON storage.
        
        Args:
            problem_set (ProblemSet): The problem set to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.data["problem_sets"][problem_set.name] = problem_set.to_dict()
        return self._save_storage()
    
    def load_problem_set(self, name: str) -> Optional[ProblemSet]:
        """
        Load a problem set from JSON storage by name.
        
        Args:
            name (str): Name of the problem set to load
            
        Returns:
            Optional[ProblemSet]: The loaded problem set, or None if not found
        """
        if name in self.data["problem_sets"]:
            return ProblemSet.from_dict(self.data["problem_sets"][name])
        return None
    
    def delete_problem_set(self, name: str) -> bool:
        """
        Delete a problem set from JSON storage.
        
        Args:
            name (str): Name of the problem set to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if name in self.data["problem_sets"]:
            del self.data["problem_sets"][name]
            return self._save_storage()
        return False
    
    def list_problem_sets(self) -> List[str]:
        """
        List all available problem sets in JSON storage.
        
        Returns:
            List[str]: List of problem set names
        """
        return list(self.data["problem_sets"].keys())