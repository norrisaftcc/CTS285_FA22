"""
Unit tests for the storage factory module.
"""

import unittest
from unittest.mock import patch, MagicMock

from core.storage import JsonStorage
from core.storage_factory import StorageFactory


class TestStorageFactory(unittest.TestCase):
    """Tests for the StorageFactory class."""

    def test_get_available_storage_types(self):
        """Test getting available storage types."""
        storage_types = StorageFactory.get_available_storage_types()
        
        # JSON storage should always be available
        self.assertIn("json", storage_types)
        self.assertIn("JSON file storage", storage_types["json"])
        
        # SQLite storage may or may not be available depending on the environment
        if "sqlite" in storage_types:
            self.assertIn("SQLite database", storage_types["sqlite"])

    def test_create_json_storage(self):
        """Test creating a JSON storage instance."""
        storage = StorageFactory.create_storage("json", "test_path.json")
        
        self.assertIsInstance(storage, JsonStorage)
        self.assertEqual(storage.file_path, "test_path.json")

    @patch("core.storage_factory.HAS_SQLITE", True)
    @patch("core.storage_factory.SqliteStorage")
    def test_create_sqlite_storage_if_available(self, mock_sqlite_storage):
        """Test creating a SQLite storage instance if available."""
        # Configure the mock to return a new mock instance
        mock_instance = MagicMock()
        mock_sqlite_storage.return_value = mock_instance
        
        # Add the mock to the storage types
        original_storage_types = StorageFactory._storage_types.copy()
        try:
            StorageFactory._storage_types["sqlite"] = mock_sqlite_storage
            
            # Try to create a SQLite storage
            storage = StorageFactory.create_storage("sqlite", "test_path.db")
            
            # Check that the SqliteStorage constructor was called
            mock_sqlite_storage.assert_called_once_with("test_path.db")
            
            # Check that we got the mock instance back
            self.assertEqual(storage, mock_instance)
        finally:
            # Restore the original storage types
            StorageFactory._storage_types = original_storage_types

    def test_create_invalid_storage_type(self):
        """Test creating an invalid storage type raises an error."""
        with self.assertRaises(ValueError):
            StorageFactory.create_storage("invalid_type", "test_path")


if __name__ == "__main__":
    unittest.main()