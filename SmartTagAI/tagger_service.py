"""
TaggerService Module

This module provides the core tagging logic for analyzing messages
and assigning relevant tags based on keyword matching.
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class TaggerService:
    """
    Analyzes messages and assigns tags based on keyword frequency scoring.
    
    The service uses a simple keyword matching algorithm to score each tag
    and returns the top 2 most relevant tags.
    """
    
    def __init__(self, tags_config: Dict[str, List[str]]):
        """
        Initialize the TaggerService with tag configuration.
        
        Args:
            tags_config: Dictionary mapping tag names to their associated keywords
        """
        self.tags_config = tags_config
        
    def analyze_message(self, message_text: str) -> Tuple[str, str]:
        """
        Analyze a message and return the top 2 most relevant tags.
        
        The algorithm:
        1. Normalizes the message to lowercase
        2. Tokenizes the message into words
        3. For each tag, counts how many of its keywords appear in the message
        4. Ranks tags by their score (keyword match count)
        5. Returns the top 2 tags
        
        Args:
            message_text: The message to analyze
            
        Returns:
            Tuple of (primary_tag, secondary_tag)
        """
        if not message_text or not message_text.strip():
            return self._get_default_tags()
        
        normalized_message = message_text.lower()
        message_words = self._tokenize(normalized_message)
        
        tag_scores = self._calculate_tag_scores(message_words)
        
        ranked_tags = self._rank_tags(tag_scores)
        
        return self._get_top_two_tags(ranked_tags)
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words, removing punctuation.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of words
        """
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def _calculate_tag_scores(self, message_words: List[str]) -> Dict[str, int]:
        """
        Calculate scores for each tag based on keyword matches.
        
        Args:
            message_words: List of words from the message
            
        Returns:
            Dictionary mapping tag names to their scores
        """
        tag_scores = {}
        
        for tag_name, keywords in self.tags_config.items():
            score = 0
            for keyword in keywords:
                keyword_parts = keyword.split()
                
                if len(keyword_parts) == 1:
                    score += message_words.count(keyword)
                else:
                    message_text = ' '.join(message_words)
                    score += message_text.count(keyword)
            
            tag_scores[tag_name] = score
        
        return tag_scores
    
    def _rank_tags(self, tag_scores: Dict[str, int]) -> List[Tuple[str, int]]:
        """
        Rank tags by their scores in descending order.
        
        Args:
            tag_scores: Dictionary of tag names to scores
            
        Returns:
            List of (tag_name, score) tuples sorted by score
        """
        return sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
    
    def _get_top_two_tags(self, ranked_tags: List[Tuple[str, int]]) -> Tuple[str, str]:
        """
        Get the top 2 tags from the ranked list.
        
        If there are ties or insufficient tags, defaults to OTHER.
        
        Args:
            ranked_tags: List of (tag_name, score) tuples sorted by score
            
        Returns:
            Tuple of (primary_tag, secondary_tag)
        """
        if len(ranked_tags) < 2:
            return self._get_default_tags()
        
        primary_tag = ranked_tags[0][0]
        secondary_tag = ranked_tags[1][0]
        
        if ranked_tags[0][1] == 0:
            return self._get_default_tags()
        
        if ranked_tags[1][1] == 0 and 'OTHER' in self.tags_config:
            secondary_tag = 'OTHER'
        
        return primary_tag, secondary_tag
    
    def _get_default_tags(self) -> Tuple[str, str]:
        """
        Get default tags when analysis fails or message is empty.
        
        Returns:
            Tuple of default tags
        """
        tags = list(self.tags_config.keys())
        if 'OTHER' in tags:
            return 'OTHER', 'OTHER'
        elif len(tags) >= 2:
            return tags[0], tags[1]
        else:
            return 'UNKNOWN', 'UNKNOWN'
