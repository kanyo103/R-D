"""
Unit tests for ConfigurationLoader
"""

import unittest
import json
import tempfile
import os
from config_loader import ConfigurationLoader


class TestConfigurationLoader(unittest.TestCase):
    """Test cases for the ConfigurationLoader class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.valid_config = {
            "tags": {
                "TEST_TAG_1": {
                    "keywords": ["keyword1", "keyword2", "keyword3"]
                },
                "TEST_TAG_2": {
                    "keywords": ["keyword4", "keyword5"]
                }
            }
        }
        
    def tearDown(self):
        """Clean up after each test method"""
        pass
    
    def test_load_valid_configuration(self):
        """Test loading a valid configuration file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            loader.load_configuration()
            
            tags_config = loader.get_tags_config()
            self.assertIn("TEST_TAG_1", tags_config)
            self.assertIn("TEST_TAG_2", tags_config)
            self.assertEqual(tags_config["TEST_TAG_1"], ["keyword1", "keyword2", "keyword3"])
            self.assertEqual(tags_config["TEST_TAG_2"], ["keyword4", "keyword5"])
        finally:
            os.unlink(temp_file)
    
    def test_load_configuration_file_not_found(self):
        """Test that FileNotFoundError is raised when config file doesn't exist"""
        loader = ConfigurationLoader("nonexistent_file.json")
        
        with self.assertRaises(FileNotFoundError):
            loader.load_configuration()
    
    def test_load_invalid_json(self):
        """Test that JSONDecodeError is raised for invalid JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json content")
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            
            with self.assertRaises(json.JSONDecodeError):
                loader.load_configuration()
        finally:
            os.unlink(temp_file)
    
    def test_load_configuration_missing_tags_key(self):
        """Test that KeyError is raised when 'tags' key is missing"""
        invalid_config = {"not_tags": {}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_config, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            
            with self.assertRaises(KeyError):
                loader.load_configuration()
        finally:
            os.unlink(temp_file)
    
    def test_load_configuration_missing_keywords(self):
        """Test that KeyError is raised when a tag is missing 'keywords'"""
        invalid_config = {
            "tags": {
                "BAD_TAG": {
                    "not_keywords": ["word1"]
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_config, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            
            with self.assertRaises(KeyError):
                loader.load_configuration()
        finally:
            os.unlink(temp_file)
    
    def test_keywords_converted_to_lowercase(self):
        """Test that all keywords are converted to lowercase"""
        config_with_uppercase = {
            "tags": {
                "TEST": {
                    "keywords": ["UPPER", "MiXeD", "lower"]
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_with_uppercase, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            loader.load_configuration()
            
            tags_config = loader.get_tags_config()
            self.assertEqual(tags_config["TEST"], ["upper", "mixed", "lower"])
        finally:
            os.unlink(temp_file)
    
    def test_get_available_tags(self):
        """Test getting list of available tags"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.valid_config, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            loader.load_configuration()
            
            available_tags = loader.get_available_tags()
            self.assertIsInstance(available_tags, list)
            self.assertEqual(len(available_tags), 2)
            self.assertIn("TEST_TAG_1", available_tags)
            self.assertIn("TEST_TAG_2", available_tags)
        finally:
            os.unlink(temp_file)
    
    def test_empty_keywords_list(self):
        """Test handling of empty keywords list"""
        config_empty_keywords = {
            "tags": {
                "EMPTY_TAG": {
                    "keywords": []
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_empty_keywords, f)
            temp_file = f.name
        
        try:
            loader = ConfigurationLoader(temp_file)
            loader.load_configuration()
            
            tags_config = loader.get_tags_config()
            self.assertEqual(tags_config["EMPTY_TAG"], [])
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()
