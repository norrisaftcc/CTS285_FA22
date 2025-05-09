"""
Storage factory for the BookSense application.

This module provides a factory for creating storage implementations.
"""

from typing import Dict, Type

from .storage import StorageInterface
from .storage import JsonStorage

# Import SQLite storage if available
try:
    from .storage_sqlite import SqliteStorage
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False


class StorageFactory:
    """Factory for creating storage implementations."""
    
    # Dictionary of storage types to their class implementations
    _storage_types: Dict[str, Type[StorageInterface]] = {
        'json': JsonStorage
    }
    
    # Add SQLite storage if available
    if HAS_SQLITE:
        _storage_types['sqlite'] = SqliteStorage
    
    @classmethod
    def get_available_storage_types(cls) -> Dict[str, str]:
        """Get a dictionary of available storage types and their descriptions.
        
        Returns:
            Dict[str, str]: Dictionary mapping storage type IDs to descriptions
        """
        descriptions = {
            'json': 'JSON file storage - simple, portable, human-readable',
        }
        
        if HAS_SQLITE:
            descriptions['sqlite'] = 'SQLite database - faster queries, better for large collections'
            
        return descriptions
    
    @classmethod
    def create_storage(cls, storage_type: str, path: str) -> StorageInterface:
        """Create a storage implementation of the specified type.
        
        Args:
            storage_type: The type of storage to create ('json', 'sqlite')
            path: The path to the storage file or database
            
        Returns:
            StorageInterface: A storage implementation
            
        Raises:
            ValueError: If the storage type is not supported
        """
        if storage_type not in cls._storage_types:
            available_types = ', '.join(cls._storage_types.keys())
            raise ValueError(f"Unsupported storage type: {storage_type}. " +
                             f"Available types: {available_types}")
        
        storage_class = cls._storage_types[storage_type]
        return storage_class(path)