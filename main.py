"""
Main Application Runner
Command-line interface for the Intelligent Chat Message Tagger.
"""

import sys
from config_loader import ConfigurationLoader
from tagger_service import TaggerService
from scoring_strategy import KeywordFrequencyScorer


class MessageTaggerApp:
    """
    Main application class that orchestrates the tagging process.
    Handles CLI interaction and coordinates between components.
    """

    def __init__(self, config_path: str = "tag_config.json"):
        """
        Initialize the application.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config_loader = None
        self.tagger_service = None

    def initialize(self) -> bool:
        """
        Initialize all components and load configuration.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            print("🚀 Initializing Intelligent Chat Message Tagger...")
            print(f"📁 Loading configuration from: {self.config_path}")
            
            # Load configuration
            self.config_loader = ConfigurationLoader(self.config_path)
            tag_config = self.config_loader.load_config()
            
            # Validate configuration
            if not self.config_loader.validate_config():
                print("❌ Configuration validation failed!")
                return False
            
            # Initialize tagger service with keyword frequency scorer
            scoring_strategy = KeywordFrequencyScorer()
            self.tagger_service = TaggerService(tag_config, scoring_strategy)
            
            # Display loaded tags
            tags = self.config_loader.get_tags()
            print(f"✅ Configuration loaded successfully!")
            print(f"📋 Available tags: {', '.join(tags)}\n")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: {str(e)}")
            return False
        except ValueError as e:
            print(f"❌ Configuration Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")
            return False

    def run(self) -> None:
        """
        Run the main application loop.
        Continuously prompts user for messages and displays tag predictions.
        """
        print("=" * 60)
        print("  INTELLIGENT CHAT MESSAGE TAGGER")
        print("=" * 60)
        print("\nEnter customer messages to get tag suggestions.")
        print("Type 'quit', 'exit', or press Ctrl+C to stop.\n")
        
        try:
            while True:
                # Get user input
                message = input("💬 Enter message: ").strip()
                
                # Check for exit commands
                if message.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using the Message Tagger. Goodbye!")
                    break
                
                # Skip empty messages
                if not message:
                    print("⚠️  Please enter a message.\n")
                    continue
                
                # Analyze message
                self._process_message(message)
                print()  # Blank line for readability
                
        except KeyboardInterrupt:
            print("\n\n👋 Application terminated by user. Goodbye!")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

    def _process_message(self, message: str) -> None:
        """
        Process a single message and display results.
        
        Args:
            message: The message to analyze
        """
        try:
            # Get tag predictions
            primary_tag, secondary_tag = self.tagger_service.analyze_message(message)
            
            # Display results
            print("\n" + "-" * 60)
            print("📊 ANALYSIS RESULTS")
            print("-" * 60)
            print(f"🥇 Primary Tag:   {primary_tag}")
            
            if secondary_tag:
                print(f"🥈 Secondary Tag: {secondary_tag}")
            else:
                print(f"🥈 Secondary Tag: None (only one relevant tag found)")
            
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error processing message: {str(e)}")

    def run_test_cases(self) -> None:
        """
        Run predefined test cases to demonstrate functionality.
        Useful for acceptance criteria validation.
        """
        print("\n" + "=" * 60)
        print("  RUNNING ACCEPTANCE TEST CASES")
        print("=" * 60 + "\n")
        
        test_cases = [
            {
                'message': "I want to buy your product and see pricing",
                'expected_primary': "SALES",
                'expected_secondary': "OTHER"
            },
            {
                'message': "My account is broken and I need help now",
                'expected_primary': "SUPPORT",
                'expected_secondary': "OTHER"
            },
            {
                'message': "Why was I charged twice on my invoice?",
                'expected_primary': "BILLING",
                'expected_secondary': "OTHER"
            }
        ]
        
        passed = 0
        failed = 0
        
        for i, test_case in enumerate(test_cases, 1):
            message = test_case['message']
            expected_primary = test_case['expected_primary']
            expected_secondary = test_case.get('expected_secondary')
            
            print(f"Test Case #{i}")
            print(f"Message: \"{message}\"")
            
            primary, secondary = self.tagger_service.analyze_message(message)
            
            print(f"Expected: Primary={expected_primary}, Secondary={expected_secondary}")
            print(f"Actual:   Primary={primary}, Secondary={secondary}")
            
            # Check results
            primary_match = primary == expected_primary
            secondary_match = (secondary == expected_secondary) if expected_secondary else True
            
            if primary_match and secondary_match:
                print("✅ PASSED")
                passed += 1
            else:
                print("❌ FAILED")
                failed += 1
            
            print("-" * 60 + "\n")
        
        print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests\n")


def main():
    """
    Application entry point.
    """
    # Check for command line arguments
    config_path = "tag_config.json"
    test_mode = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_mode = True
        else:
            config_path = sys.argv[1]
    
    # Create and initialize application
    app = MessageTaggerApp(config_path)
    
    if not app.initialize():
        print("\n❌ Application failed to initialize. Exiting.")
        sys.exit(1)
    
    # Run in test mode or interactive mode
    if test_mode:
        app.run_test_cases()
    else:
        app.run()


if __name__ == "__main__":
    main()
