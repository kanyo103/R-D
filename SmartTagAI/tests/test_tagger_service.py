"""
Unit tests for TaggerService
"""

import unittest
from tagger_service import TaggerService


class TestTaggerService(unittest.TestCase):
    """Test cases for the TaggerService class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.tags_config = {
            "SALES": ["buy", "purchase", "price", "demo", "upgrade"],
            "SUPPORT": ["help", "issue", "problem", "error", "bug", "fix"],
            "BILLING": ["invoice", "payment", "charge", "refund", "bill"],
            "OTHER": ["question", "inquiry", "general"]
        }
        self.tagger = TaggerService(self.tags_config)
    
    def test_analyze_sales_message(self):
        """Test analyzing a message with strong sales keywords"""
        message = "I want to buy your product and see a demo"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "SALES")
    
    def test_analyze_support_message(self):
        """Test analyzing a message with strong support keywords"""
        message = "I have an issue and need help to fix this bug"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "SUPPORT")
    
    def test_analyze_billing_message(self):
        """Test analyzing a message with strong billing keywords"""
        message = "I need a refund for the invoice charge on my bill"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "BILLING")
    
    def test_analyze_mixed_message(self):
        """Test analyzing a message with keywords from multiple categories"""
        message = "I want to buy the product but I have a billing issue"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertIn(primary, ["SALES", "BILLING", "SUPPORT"])
        self.assertIn(secondary, ["SALES", "BILLING", "SUPPORT"])
        self.assertNotEqual(primary, secondary)
    
    def test_analyze_empty_message(self):
        """Test analyzing an empty message"""
        primary, secondary = self.tagger.analyze_message("")
        
        self.assertEqual(primary, "OTHER")
        self.assertEqual(secondary, "OTHER")
    
    def test_analyze_whitespace_message(self):
        """Test analyzing a message with only whitespace"""
        primary, secondary = self.tagger.analyze_message("   \t\n   ")
        
        self.assertEqual(primary, "OTHER")
        self.assertEqual(secondary, "OTHER")
    
    def test_analyze_no_matching_keywords(self):
        """Test analyzing a message with no matching keywords"""
        message = "zebra elephant giraffe"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "OTHER")
        self.assertEqual(secondary, "OTHER")
    
    def test_case_insensitive_matching(self):
        """Test that keyword matching is case-insensitive"""
        message = "I WANT TO BUY YOUR PRODUCT"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "SALES")
    
    def test_multi_word_keywords(self):
        """Test handling of multi-word keywords"""
        tags_config = {
            "TAG1": ["multi word keyword", "single"],
            "TAG2": ["other", "test"]
        }
        tagger = TaggerService(tags_config)
        
        message = "This has a multi word keyword in it"
        primary, secondary = tagger.analyze_message(message)
        
        self.assertEqual(primary, "TAG1")
    
    def test_keyword_frequency_scoring(self):
        """Test that tags are scored by keyword frequency"""
        message = "buy buy buy help"
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "SALES")
    
    def test_returns_tuple(self):
        """Test that analyze_message returns a tuple"""
        message = "test message"
        result = self.tagger.analyze_message(message)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    def test_tokenize_method(self):
        """Test the tokenization method"""
        text = "Hello, world! This is a test."
        tokens = self.tagger._tokenize(text)
        
        self.assertIsInstance(tokens, list)
        self.assertIn("Hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("test", tokens)
        self.assertNotIn(",", tokens)
        self.assertNotIn("!", tokens)
    
    def test_calculate_tag_scores(self):
        """Test the tag scoring calculation"""
        message_words = ["buy", "purchase", "help"]
        scores = self.tagger._calculate_tag_scores(message_words)
        
        self.assertIsInstance(scores, dict)
        self.assertGreater(scores["SALES"], 0)
        self.assertGreater(scores["SUPPORT"], 0)
        self.assertEqual(scores["SALES"], 2)
        self.assertEqual(scores["SUPPORT"], 1)
    
    def test_rank_tags(self):
        """Test tag ranking by score"""
        scores = {"TAG1": 5, "TAG2": 10, "TAG3": 3}
        ranked = self.tagger._rank_tags(scores)
        
        self.assertIsInstance(ranked, list)
        self.assertEqual(ranked[0][0], "TAG2")
        self.assertEqual(ranked[0][1], 10)
        self.assertEqual(ranked[1][0], "TAG1")
        self.assertEqual(ranked[2][0], "TAG3")
    
    def test_punctuation_handling(self):
        """Test that punctuation is properly handled"""
        message = "buy! purchase? price, demo."
        primary, secondary = self.tagger.analyze_message(message)
        
        self.assertEqual(primary, "SALES")
    
    def test_single_tag_config(self):
        """Test behavior with only one tag configured"""
        single_tag_config = {"ONLY_TAG": ["keyword1", "keyword2"]}
        tagger = TaggerService(single_tag_config)
        
        message = "keyword1"
        primary, secondary = tagger.analyze_message(message)
        
        self.assertIsInstance(primary, str)
        self.assertIsInstance(secondary, str)


if __name__ == '__main__':
    unittest.main()
