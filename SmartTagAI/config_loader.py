"""
ConfigurationLoader Module

This module handles loading and parsing the tag configuration from a JSON file.
"""

import json
from typing import Dict, List


class ConfigurationLoader:
    """
    Loads and manages tag configuration from a JSON file.
    
    The configuration file should contain a 'tags' object where each key is a tag name
    and the value is an object with a 'keywords' array.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the ConfigurationLoader.
        
        Args:
            config_path: Path to the configuration JSON file
        """
        # If not provided, resolve path relative to this file so the
        # configuration can be loaded regardless of the current working directory.
        if config_path:
            self.config_path = config_path
        else:
            import os
            base_dir = os.path.dirname(__file__)
            self.config_path = os.path.join(base_dir, 'tag_config.json')
        self.tags_config: Dict[str, List[str]] = {}
        
    def load_configuration(self) -> None:
        """
        Load and parse the configuration file.
        
        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            json.JSONDecodeError: If the configuration file is not valid JSON
            KeyError: If the configuration structure is invalid
        """
        try:
            with open(self.config_path, 'r') as file:
                config_data = json.load(file)
                
            if 'tags' not in config_data:
                raise KeyError("Configuration must contain a 'tags' object")
            
            for tag_name, tag_data in config_data['tags'].items():
                if 'keywords' not in tag_data:
                    raise KeyError(f"Tag '{tag_name}' must contain a 'keywords' array")
                
                self.tags_config[tag_name] = [
                    keyword.lower() for keyword in tag_data['keywords']
                ]
                
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in configuration file: {str(e)}",
                e.doc,
                e.pos
            )
    
    def get_tags_config(self) -> Dict[str, List[str]]:
        """
        Get the loaded tags configuration.
        
        Returns:
            Dictionary mapping tag names to their associated keywords
        """
        return self.tags_config
    
    def get_available_tags(self) -> List[str]:
        """
        Get a list of all available tag names.
        
        Returns:
            List of tag names
        """
        return list(self.tags_config.keys())
