# Intelligent Chat Message Tagger POC

A command-line service that analyzes customer messages and assigns relevant tags based on keyword matching. This Proof of Concept (POC) demonstrates a simple, extensible tagging system using Object-Oriented Programming principles.

## Table of Contents

- [Overview](#overview)
- [Minimum Requirements](#minimum-requirements)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [High-Level Implementation Details](#high-level-implementation-details)
- [Acceptance Criteria & Test Cases](#acceptance-criteria--test-cases)
- [Project Structure](#project-structure)
- [Extensibility](#extensibility)
- [License](#license)

## Overview

The Intelligent Chat Message Tagger analyzes customer messages and automatically assigns a primary and secondary tag based on the content. The system uses a configurable keyword-matching algorithm to identify the most relevant tags for each message.

**Key Features:**
- Data-driven configuration using JSON
- Simple keyword frequency scoring algorithm
- Modular OOP design for easy extension
- Interactive command-line interface
- Support for multiple tag categories (SALES, SUPPORT, BILLING, OTHER)

## Minimum Requirements

To run this POC, you need:

- **Python 3.8 or higher**
- **Standard Library Only** (no external dependencies required)

### Verifying Python Installation

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd intelligent-chat-tagger
   ```

2. **Verify the configuration file exists:**
   
   The `tag_config.json` file contains the tag definitions and keywords. It should be present in the project root directory.

3. **No additional installation needed** - the project uses only Python's standard library.

## Usage

### Running the Application

Execute the main script from the command line:

```bash
python main.py
# or
python3 main.py
```

### Interactive Mode

Once started, the application will:
1. Load the tag configuration
2. Display available tags
3. Prompt you to enter a customer message
4. Analyze the message and display the top 2 tags

### Example Session

```
Initializing Intelligent Chat Message Tagger...
Loaded 4 tags: SALES, SUPPORT, BILLING, OTHER

============================================================
INTELLIGENT CHAT MESSAGE TAGGER
============================================================

Enter a customer message to analyze.
HERE ARE SOME EXAMPLE MESSAGES YOU CAN TRY:
************************************************************
- I need help with my order.
- Can you asssit me with a technical issue?
- I'm looking for information on my account.
************************************************************
Type 'quit' or 'exit' to stop.

Enter message: I'm interested in the enterprise plan pricing

------------------------------------------------------------
Primary Tag:   SALES
Secondary Tag: BILLING
------------------------------------------------------------

Enter message: My application keeps crashing when I try to login

------------------------------------------------------------
Primary Tag:   SUPPORT
Secondary Tag: OTHER
------------------------------------------------------------

Enter message: I was charged twice this month

------------------------------------------------------------
Primary Tag:   BILLING
Secondary Tag: SUPPORT
------------------------------------------------------------

Enter message: quit

Thank you for using the Chat Message Tagger!
```

## High-Level Implementation Details

### Architecture

The application follows a modular, object-oriented design with three main components:

#### 1. ConfigurationLoader (`config_loader.py`)

**Purpose:** Loads and parses the tag configuration from `tag_config.json`.

**Key Methods:**
- `load_configuration()`: Reads the JSON file and validates the structure
- `get_tags_config()`: Returns the complete tag-to-keywords mapping
- `get_available_tags()`: Returns a list of all available tag names

**Design Decisions:**
- Validates configuration structure at load time
- Converts all keywords to lowercase for case-insensitive matching
- Raises descriptive errors if the configuration is invalid

#### 2. TaggerService (`tagger_service.py`)

**Purpose:** Implements the core tagging logic using keyword frequency scoring.

**Key Method:**
- `analyze_message(message_text)`: Analyzes a message and returns the top 2 tags

**Scoring Algorithm:**
1. **Normalization:** Convert message to lowercase
2. **Tokenization:** Extract words from the message using regex
3. **Scoring:** For each tag, count how many keywords appear in the message
4. **Ranking:** Sort tags by score (highest first)
5. **Selection:** Return the top 2 tags

**Design Decisions:**
- Uses simple keyword frequency counting (suitable for POC)
- Handles multi-word keywords
- Defaults to "OTHER" tag when no keywords match
- Designed for easy extension to more sophisticated algorithms

#### 3. ApplicationRunner (`main.py`)

**Purpose:** Orchestrates the application flow and provides the CLI interface.

**Key Methods:**
- `initialize()`: Sets up the configuration loader and tagger service
- `run_interactive()`: Manages the interactive command-line loop
- `run()`: Main entry point that coordinates initialization and execution

**Design Decisions:**
- Separates initialization from runtime logic
- Provides clear error messages
- Supports graceful exit (quit/exit/Ctrl+C)
- Displays results in a user-friendly format

### Data Flow

```
1. User Input → ApplicationRunner
2. ApplicationRunner → TaggerService.analyze_message()
3. TaggerService → Tokenizes and scores against ConfigurationLoader data
4. TaggerService → Returns (primary_tag, secondary_tag)
5. ApplicationRunner → Displays results to user
```

## Acceptance Criteria & Test Cases

The following test cases demonstrate that the application meets the "Definition of Done":

### Test Case 1: Sales Inquiry
**Input Message:**
```
"I'm interested in purchasing the enterprise plan. Can you provide a quote and pricing information?"
```

**Expected Output:**
- **Primary Tag:** SALES
- **Secondary Tag:** BILLING

**Rationale:** Keywords matched: "interested", "purchasing", "enterprise", "plan", "quote", "pricing" → Strong SALES signals with BILLING overlap due to pricing-related terms.

---

### Test Case 2: Technical Support Issue
**Input Message:**
```
"The application crashes every time I try to log in. Please help me fix this issue."
```

**Expected Output:**
- **Primary Tag:** SUPPORT
- **Secondary Tag:** OTHER

**Rationale:** Keywords matched: "crashes", "help", "fix", "issue" → Clear SUPPORT indicators, OTHER as secondary due to general inquiry nature.

---

### Test Case 3: Billing Concern
**Input Message:**
```
"I was charged twice on my credit card this month. My payment transaction appears broken and I need help with this billing issue."
```

**Expected Output:**
- **Primary Tag:** BILLING
- **Secondary Tag:** SUPPORT

**Rationale:** Keywords matched: "charged", "credit card", "payment", "transaction", "billing" → Strong BILLING signals with SUPPORT overlap due to "help", "broken", "issue".

---

### Running the Test Cases

To verify these test cases:

1. Run the application: `python main.py`
2. Enter each test message when prompted
3. Verify the output matches the expected tags

## Unit Testing

The project includes a comprehensive unit test suite that validates all components of the application.

### Test Coverage

The unit tests cover:

1. **ConfigurationLoader Tests** (`tests/test_config_loader.py`)
   - Valid configuration loading
   - Error handling (missing files, invalid JSON, malformed config)
   - Keyword normalization (lowercase conversion)
   - Edge cases (empty keywords, missing keys)

2. **TaggerService Tests** (`tests/test_tagger_service.py`)
   - Message analysis and tag assignment
   - Keyword frequency scoring algorithm
   - Case-insensitive matching
   - Multi-word keyword support
   - Edge cases (empty messages, no matches, punctuation handling)
   - Internal method testing (tokenization, scoring, ranking)

3. **ApplicationRunner Tests** (`tests/test_application_runner.py`)
   - Initialization and error handling
   - Interactive mode behavior
   - User input handling (quit/exit commands, empty input)
   - Exception handling (KeyboardInterrupt, EOFError)

### Running Unit Tests

Execute the unit test suite:

```bash
python run_unittests.py
```

**Expected Output:**
```
======================================================================
INTELLIGENT CHAT MESSAGE TAGGER - UNIT TEST RUNNER
======================================================================

... (test execution output) ...

----------------------------------------------------------------------
Ran 37 tests in 0.023s

OK

======================================================================
UNIT TEST SUMMARY
======================================================================
Tests Run: 37
Failures: 0
Errors: 0
Skipped: 0

✓ All unit tests passed!
```

### Running Individual Test Files

You can also run individual test files:

```bash
# Test ConfigurationLoader only
python -m unittest tests.test_config_loader

# Test TaggerService only
python -m unittest tests.test_tagger_service

# Test ApplicationRunner only
python -m unittest tests.test_application_runner
```

### Writing Additional Tests

To add new tests:

1. Create a test file in the `tests/` directory following the naming convention `test_*.py`
2. Import `unittest` and the module you want to test
3. Create a test class inheriting from `unittest.TestCase`
4. Write test methods starting with `test_`

Example:

```python
import unittest
from my_module import MyClass

class TestMyClass(unittest.TestCase):
    def test_my_feature(self):
        obj = MyClass()
        result = obj.my_method()
        self.assertEqual(result, expected_value)
```

## Project Structure

```
intelligent-chat-tagger/
│
├── main.py                      # Application entry point and CLI interface
├── config_loader.py             # Configuration loading and parsing
├── tagger_service.py            # Core tagging logic and scoring algorithm
├── tag_config.json              # Tag definitions and keyword mappings
├── test_runner.py               # Integration test runner
├── run_unittests.py             # Unit test runner
├── tests/                       # Unit test directory
│   ├── __init__.py              # Test package initializer
│   ├── test_config_loader.py    # ConfigurationLoader unit tests
│   ├── test_tagger_service.py   # TaggerService unit tests
│   └── test_application_runner.py  # ApplicationRunner unit tests
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## Extensibility

The modular design makes it easy to extend the application:

### Adding New Tags

Edit `tag_config.json` to add new tags with their keywords:

```json
{
  "tags": {
    "FEEDBACK": {
      "keywords": ["feedback", "suggestion", "improvement", "feature request"]
    }
  }
}
```

### Implementing Advanced Scoring

The `TaggerService` class can be extended to support more sophisticated algorithms:

```python
class AdvancedTaggerService(TaggerService):
    def _calculate_tag_scores(self, message_words):
        # Implement weighted scoring, TF-IDF, or ML-based scoring
        pass
```

### Adding New Output Formats

The `ApplicationRunner` can be extended to support different output formats:

```python
def run_json_output(self):
    # Output results as JSON instead of text
    pass
```

### Integration Opportunities

The core components can be integrated into:
- Web APIs (Flask, FastAPI)
- Chatbot systems
- Customer support platforms
- Message queue processors

## License

This is a Proof of Concept project for demonstration purposes.

---

**Author:** Karabo Lelaka  
**Date:** October 2025
