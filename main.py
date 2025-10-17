"""
Intelligent Chat Message Tagger - Main Application

This is the main entry point for the Chat Message Tagger POC.
It provides a command-line interface for users to input messages
and receive tag suggestions.
"""

import sys
from config_loader import ConfigurationLoader
from tagger_service import TaggerService


class ApplicationRunner:
    """
    Main application runner that orchestrates the tagging workflow.
    
    This class ties together the configuration loading and tagging service
    to provide an interactive command-line interface.
    """
    
    def __init__(self):
        """Initialize the application."""
        self.config_loader = None
        self.tagger_service = None
        
    def initialize(self) -> bool:
        """
        Initialize the application by loading configuration.
        
        Returns:
            True if initialization succeeds, False otherwise
        """
        try:
            print("Initializing Intelligent Chat Message Tagger...")
            
            self.config_loader = ConfigurationLoader()
            self.config_loader.load_configuration()
            
            tags_config = self.config_loader.get_tags_config()
            self.tagger_service = TaggerService(tags_config)
            
            available_tags = self.config_loader.get_available_tags()
            print(f"Loaded {len(available_tags)} tags: {', '.join(available_tags)}")
            print()
            
            return True
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Error initializing application: {e}")
            return False
    
    def run_interactive(self) -> None:
        """
        Run the interactive command-line interface.
        
        Prompts the user to enter messages and displays tag suggestions.
        """
        print("=" * 60)
        print("WELCOME TO MY INTELLIGENT CHAT MESSAGE TAGGER")
        print("=" * 60)
        print()
        print("Enter a customer message to analyze.")
        print("HERE ARE SOME EXAMPLE MESSAGES YOU CAN TRY:")
        print("*" * 60)
        print("- I need help with my order.")
        print("- Can you asssit me with a technical issue?")
        print("- I'm looking for information on my account.")
        print("*" * 60)
        print("Type 'quit' or 'exit' to stop.")
        print()
        
        while True:
            try:
                message = input("Enter message: ").strip()
                
                if message.lower() in ['quit', 'exit', 'q']:
                    print("\nThank you for using the Chat Message Tagger!")
                    break
                
                if not message:
                    print("Please enter a valid message.\n")
                    continue
                
                if self.tagger_service is None:
                    print("Error: Tagger service not initialized.\n")
                    continue
                
                primary_tag, secondary_tag = self.tagger_service.analyze_message(message)
                
                print()
                print("-" * 60)
                print(f"Primary Tag:   {primary_tag}")
                print(f"Secondary Tag: {secondary_tag}")
                print("-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except EOFError:
                print("\n\nEnd of input. Exiting...")
                break
    
    def run(self) -> int:
        """
        Main run method for the application.
        
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        if not self.initialize():
            return 1
        
        self.run_interactive()
        return 0


def main():
    """Main entry point."""
    app = ApplicationRunner()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
