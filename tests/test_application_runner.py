"""
Unit tests for ApplicationRunner
"""

import unittest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from main import ApplicationRunner


class TestApplicationRunner(unittest.TestCase):
    """Test cases for the ApplicationRunner class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.app = ApplicationRunner()
    
    def test_initialization(self):
        """Test that ApplicationRunner initializes with None values"""
        self.assertIsNone(self.app.config_loader)
        self.assertIsNone(self.app.tagger_service)
    
    @patch('main.ConfigurationLoader')
    @patch('main.TaggerService')
    def test_initialize_success(self, mock_tagger, mock_loader):
        """Test successful initialization"""
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_tags_config.return_value = {"TEST": ["word"]}
        mock_loader_instance.get_available_tags.return_value = ["TEST"]
        mock_loader.return_value = mock_loader_instance
        
        result = self.app.initialize()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.app.config_loader)
        self.assertIsNotNone(self.app.tagger_service)
        mock_loader_instance.load_configuration.assert_called_once()
    
    @patch('main.ConfigurationLoader')
    def test_initialize_file_not_found(self, mock_loader):
        """Test initialization failure when config file not found"""
        mock_loader_instance = MagicMock()
        mock_loader_instance.load_configuration.side_effect = FileNotFoundError("Config not found")
        mock_loader.return_value = mock_loader_instance
        
        with patch('sys.stdout', new=StringIO()):
            result = self.app.initialize()
        
        self.assertFalse(result)
    
    @patch('main.ConfigurationLoader')
    def test_initialize_general_exception(self, mock_loader):
        """Test initialization failure with general exception"""
        mock_loader_instance = MagicMock()
        mock_loader_instance.load_configuration.side_effect = Exception("General error")
        mock_loader.return_value = mock_loader_instance
        
        with patch('sys.stdout', new=StringIO()):
            result = self.app.initialize()
        
        self.assertFalse(result)
    
    @patch('builtins.input', side_effect=['quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_quit_command(self, mock_stdout, mock_input):
        """Test that 'quit' command exits the interactive loop"""
        self.app.tagger_service = MagicMock()
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("Thank you for using the Chat Message Tagger!", output)
    
    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_exit_command(self, mock_stdout, mock_input):
        """Test that 'exit' command exits the interactive loop"""
        self.app.tagger_service = MagicMock()
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("Thank you for using the Chat Message Tagger!", output)
    
    @patch('builtins.input', side_effect=['test message', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_with_message(self, mock_stdout, mock_input):
        """Test processing a message in interactive mode"""
        mock_tagger = MagicMock()
        mock_tagger.analyze_message.return_value = ("TAG1", "TAG2")
        self.app.tagger_service = mock_tagger
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("TAG1", output)
        self.assertIn("TAG2", output)
        mock_tagger.analyze_message.assert_called_with('test message')
    
    @patch('builtins.input', side_effect=['   ', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_empty_message(self, mock_stdout, mock_input):
        """Test handling of empty message input"""
        self.app.tagger_service = MagicMock()
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("Please enter a valid message", output)
    
    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_keyboard_interrupt(self, mock_stdout, mock_input):
        """Test handling of KeyboardInterrupt (Ctrl+C)"""
        self.app.tagger_service = MagicMock()
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("Interrupted by user", output)
    
    @patch('builtins.input', side_effect=EOFError())
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_eof_error(self, mock_stdout, mock_input):
        """Test handling of EOFError"""
        self.app.tagger_service = MagicMock()
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("End of input", output)
    
    @patch.object(ApplicationRunner, 'initialize', return_value=True)
    @patch.object(ApplicationRunner, 'run_interactive')
    def test_run_success(self, mock_interactive, mock_init):
        """Test successful run returns 0"""
        exit_code = self.app.run()
        
        self.assertEqual(exit_code, 0)
        mock_init.assert_called_once()
        mock_interactive.assert_called_once()
    
    @patch.object(ApplicationRunner, 'initialize', return_value=False)
    def test_run_initialization_failure(self, mock_init):
        """Test run returns 1 when initialization fails"""
        exit_code = self.app.run()
        
        self.assertEqual(exit_code, 1)
        mock_init.assert_called_once()
    
    @patch('builtins.input', side_effect=['test', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_interactive_none_tagger_service(self, mock_stdout, mock_input):
        """Test handling when tagger service is None"""
        self.app.tagger_service = None
        
        self.app.run_interactive()
        
        output = mock_stdout.getvalue()
        self.assertIn("Tagger service not initialized", output)


if __name__ == '__main__':
    unittest.main()
