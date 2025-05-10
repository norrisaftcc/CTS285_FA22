#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storage_factory.py - Factory for creating storage instances

This module provides a factory pattern implementation for creating
different storage backends for the Dataman application.
"""
from typing import Dict, Optional

from .storage import StorageInterface, JSONStorage
from .storage_sqlite import SQLiteStorage


class StorageFactory:
    """Factory for creating storage instances."""
    
    @staticmethod
    def create_storage(storage_type: str, **kwargs) -> Optional[StorageInterface]:
        """
        Create a storage instance of the specified type.
        
        Args:
            storage_type (str): Type of storage to create ('json', 'sqlite')
            **kwargs: Additional arguments to pass to the storage constructor
        
        Returns:
            Optional[StorageInterface]: Storage instance or None if type is invalid
            
        Example:
            >>> storage = StorageFactory.create_storage('json', file_path='data.json')
            >>> sqlite_storage = StorageFactory.create_storage('sqlite', db_path='data.db')
        """
        if storage_type == 'json':
            if 'file_path' not in kwargs:
                raise ValueError("file_path is required for JSON storage")
            return JSONStorage(kwargs['file_path'])
        elif storage_type == 'sqlite':
            if 'db_path' not in kwargs:
                raise ValueError("db_path is required for SQLite storage")
            return SQLiteStorage(kwargs['db_path'])
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
    
    @staticmethod
    def get_available_storage_types() -> Dict[str, str]:
        """
        Get a dictionary of available storage types.
        
        Returns:
            Dict[str, str]: Dictionary mapping storage type names to descriptions
        """
        return {
            'json': 'JSON file storage',
            'sqlite': 'SQLite database storage'
        }