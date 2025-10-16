"""
Configuration Loader Module
Handles loading and validation of tag configuration from JSON file.
"""

import json
from typing import Dict, List
from pathlib import Path


class ConfigurationLoader:
    """
    Responsible for loading and validating tag configuration data.
    Follows Single Responsibility Principle - only handles config operations.
    """

    def __init__(self, config_path: str = "tag_config.json"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration JSON file
        """
        self.config_path = config_path
        self.config_data = None

    def load_config(self) -> Dict[str, List[str]]:
        """
        Load and parse the configuration file.
        
        Returns:
            Dictionary mapping tag names to keyword lists
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config format is invalid
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate and extract tags
            if 'tags' not in data:
                raise ValueError("Configuration must contain 'tags' key")
            
            self.config_data = {}
            for tag_name, tag_info in data['tags'].items():
                if 'keywords' not in tag_info:
                    raise ValueError(f"Tag '{tag_name}' missing 'keywords' field")
                
                # Normalize keywords to lowercase for case-insensitive matching
                keywords = [kw.lower() for kw in tag_info['keywords']]
                self.config_data[tag_name] = keywords
            
            if not self.config_data:
                raise ValueError("Configuration must contain at least one tag")
            
            return self.config_data
            
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please ensure tag_config.json exists in the current directory."
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in config file: {str(e)}")

    def get_tags(self) -> List[str]:
        """
        Get list of all available tags.
        
        Returns:
            List of tag names
        """
        if self.config_data is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")
        return list(self.config_data.keys())

    def get_keywords(self, tag: str) -> List[str]:
        """
        Get keywords for a specific tag.
        
        Args:
            tag: Tag name
            
        Returns:
            List of keywords for the tag
        """
        if self.config_data is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")
        
        if tag not in self.config_data:
            raise KeyError(f"Tag '{tag}' not found in configuration")
        
        return self.config_data[tag]

    def validate_config(self) -> bool:
        """
        Validate the loaded configuration.
        
        Returns:
            True if configuration is valid
        """
        if self.config_data is None:
            return False
        
        # Check for at least one tag
        if len(self.config_data) == 0:
            return False
        
        # Check each tag has at least one keyword
        for tag, keywords in self.config_data.items():
            if not keywords or len(keywords) == 0:
                return False
        
        return True
