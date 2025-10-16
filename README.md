# Intelligent Chat Message Tagger POC

A self-contained service that intelligently analyzes customer messages and assigns primary and secondary tags based on keyword matching and scoring algorithms.

## 📋 Table of Contents
- [Overview](#overview)
- [Minimum Requirements](#minimum-requirements)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Architecture](#architecture)
- [Acceptance Criteria](#acceptance-criteria)
- [Extensibility](#extensibility)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

This POC demonstrates a modular, extensible message tagging system that:
- Loads tag configurations from a JSON file
- Analyzes customer messages using keyword-based scoring
- Returns the top 2 most relevant tags (Primary and Secondary)
- Provides a simple command-line interface for interaction

**Use Case:** Automatically categorize customer support messages for routing to appropriate teams (Sales, Support, Billing, etc.)

---

## ⚙️ Minimum Requirements

### Software Requirements
- **Python:** Version 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Dependencies:** None (uses Python standard library only)

### Files Required
- `main.py` - Application entry point
- `config_loader.py` - Configuration loading module
- `tagger_service.py` - Core tagging logic
- `scoring_strategy.py` - Scoring algorithm implementations
- `tag_config.json` - Tag and keyword configuration

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/intelligent-chat-tagger.git
cd intelligent-chat-tagger
```

### 2. Verify Python Installation
```bash
python --version
# or
python3 --version
```

### 3. Verify Configuration File
Ensure `tag_config.json` exists in the project root directory with the following structure:
```json
{
  "tags": {
    "SALES": {
      "keywords": ["buy", "purchase", "price", "demo"]
    },
    "SUPPORT": {
      "keywords": ["help", "issue", "broken", "error"]
    }
  }
}
```

### 4. Run the Application
```bash
python main.py
```

---

## 💻 Usage

### Interactive Mode
Run the application and enter messages when prompted:

```bash
$ python main.py

🚀 Initializing Intelligent Chat Message Tagger...
📁 Loading configuration from: tag_config.json
✅ Configuration loaded successfully!
📋 Available tags: SALES, SUPPORT, BILLING, OTHER

============================================================
  INTELLIGENT CHAT MESSAGE TAGGER
============================================================

Enter customer messages to get tag suggestions.
Type 'quit', 'exit', or press Ctrl+C to stop.

💬 Enter message: I want to buy your product and see pricing

------------------------------------------------------------
📊 ANALYSIS RESULTS
------------------------------------------------------------
🥇 Primary Tag:   SALES
🥈 Secondary Tag: OTHER
------------------------------------------------------------
```

### Test Mode
Run predefined test cases for validation:

```bash
python main.py --test
```

### Custom Configuration File
Use a different configuration file:

```bash
python main.py path/to/custom_config.json
```

---

## 🏗️ Architecture

### High-Level Design

```
┌─────────────────────────────────────────────┐
│        MessageTaggerApp (main.py)           │
│         (CLI & Orchestration)               │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼─────────┐
│ Configuration  │   │  Tagger Service  │
│    Loader      │   │  (Core Logic)    │
└───────┬────────┘   └────────┬─────────┘
        │                     │
        │            ┌────────▼─────────┐
        │            │ Scoring Strategy │
        │            │   (Algorithm)    │
        │            └──────────────────┘
        │
┌───────▼────────┐
│ tag_config.json│
└────────────────┘
```

### Key Components

#### 1. ConfigurationLoader (`config_loader.py`)
**Responsibility:** Load and validate tag configuration from JSON file

**Key Methods:**
- `load_config()` - Reads and parses the JSON configuration
- `validate_config()` - Ensures configuration is valid
- `get_tags()` - Returns list of available tags
- `get_keywords(tag)` - Returns keywords for a specific tag

**Design Principle:** Single Responsibility - only handles configuration operations

---

#### 2. ScoringStrategy (`scoring_strategy.py`)
**Responsibility:** Define scoring algorithm interface and implementations

**Classes:**
- `ScoringStrategy` (Abstract Base Class) - Defines the interface
- `KeywordFrequencyScorer` - Counts keyword occurrences
- `WeightedKeywordScorer` - Optional weighted scoring

**Key Method:**
- `calculate_score(message, keywords)` - Returns a score for how well a message matches keywords

**Design Principle:** Strategy Pattern - allows easy swapping of scoring algorithms

---

#### 3. TaggerService (`tagger_service.py`)
**Responsibility:** Core business logic for message analysis

**Key Methods:**
- `analyze_message(message)` - Returns (primary_tag, secondary_tag)
- `_score_all_tags(message)` - Calculates scores for all tags
- `get_detailed_analysis(message)` - Returns detailed scoring information
- `set_scoring_strategy(strategy)` - Changes scoring algorithm at runtime

**Algorithm Flow:**
1. Calculate score for each tag using the scoring strategy
2. Sort tags by score (descending)
3. Return top 2 tags with highest scores

**Design Principle:** Dependency Injection - scoring strategy is injected, making it testable and extensible

---

#### 4. MessageTaggerApp (`main.py`)
**Responsibility:** Application orchestration and CLI interface

**Key Methods:**
- `initialize()` - Sets up all components
- `run()` - Main interactive loop
- `_process_message(message)` - Processes a single message
- `run_test_cases()` - Runs predefined test cases

**Design Principle:** Facade Pattern - provides a simple interface to the complex subsystem

---

### Scoring Algorithm Explanation

**Algorithm:** Keyword Frequency Count

```python
def calculate_score(message, keywords):
    1. Normalize message to lowercase
    2. Extract words using regex: \b\w+\b
    3. For each keyword:
       - Count exact word matches
       - Add 0.5 points for substring matches (multi-word keywords)
    4. Return total score
```

**Example:**
```
Message: "I want to buy your product and see pricing"
Keywords (SALES): ["buy", "purchase", "price", "pricing", "product"]

Score calculation:
- "buy" appears 1 time → +1 point
- "product" appears 1 time → +1 point
- "pricing" appears 1 time → +1 point
Total Score: 3.0

Keywords (OTHER): ["question", "info", "general"]
- No matches → 0 points
```

**Why This Works:**
- Simple and fast (O(n*m) where n = words, m = keywords)
- Case-insensitive for user-friendliness
- Handles both single-word and multi-word keywords
- Deterministic ordering (alphabetical) for ties

---

## ✅ Acceptance Criteria

### Test Case 1: Sales Inquiry
**Input:**
```
"I want to buy your product and see pricing"
```
**Expected Output:**
- Primary Tag: `SALES`
- Secondary Tag: `OTHER`

**Rationale:** Contains "buy", "product", and "pricing" keywords strongly associated with SALES.

---

### Test Case 2: Support Request
**Input:**
```
"My account is broken and I need help now"
```
**Expected Output:**
- Primary Tag: `SUPPORT`
- Secondary Tag: `OTHER`

**Rationale:** Contains "broken" and "help" keywords strongly associated with SUPPORT.

---

### Test Case 3: Billing Question
**Input:**
```
"Why was I charged twice on my invoice?"
```
**Expected Output:**
- Primary Tag: `BILLING`
- Secondary Tag: `OTHER`

**Rationale:** Contains "charged" and "invoice" keywords strongly associated with BILLING.

---

### Running Test Cases

Execute the built-in test suite:
```bash
python main.py --test
```

Expected output:
```
============================================================
  RUNNING ACCEPTANCE TEST CASES
============================================================

Test Case #1
Message: "I want to buy your product and see pricing"
Expected: Primary=SALES, Secondary=OTHER
Actual:   Primary=SALES, Secondary=OTHER
✅ PASSED
------------------------------------------------------------

Test Case #2
Message: "My account is broken and I need help now"
Expected: Primary=SUPPORT, Secondary=OTHER
Actual:   Primary=SUPPORT, Secondary=OTHER
✅ PASSED
------------------------------------------------------------

Test Case #3
Message: "Why was I charged twice on my invoice?"
Expected: Primary=BILLING, Secondary=OTHER
Actual:   Primary=BILLING, Secondary=OTHER
✅ PASSED
------------------------------------------------------------

Results: 3 passed, 0 failed out of 3 tests
```

---

## 🔧 Extensibility

### Adding New Tags
Simply update `tag_config.json`:
```json
{
  "tags": {
    "SALES": { "keywords": [...] },
    "SUPPORT": { "keywords": [...] },
    "FEEDBACK": {
      "keywords": ["feedback", "suggestion", "improve", "feature request"]
    }
  }
}
```
No code changes required!

### Implementing a New Scoring Strategy

1. Create a new class inheriting from `ScoringStrategy`:
```python
class TFIDFScorer(ScoringStrategy):
    def calculate_score(self, message, keywords):
        # Your algorithm here
        return score
```

2. Use it in the application:
```python
scorer = TFIDFScorer()
tagger_service = TaggerService(tag_config, scorer)
```

### Adding More Output Formats
Extend `MessageTaggerApp._process_message()` to support JSON, CSV, or other formats.

---

## 🚀 Future Enhancements

### Short-Term Improvements
1. **Confidence Scores:** Return confidence percentages with tags
2. **Multi-language Support:** Handle messages in different languages
3. **Fuzzy Matching:** Handle typos and variations (e.g., "hlep" → "help")
4. **Synonym Support:** Expand keywords with synonyms

### Medium-Term Enhancements
1. **TF-IDF Scoring:** Weight keywords by rarity across messages
2. **Context Analysis:** Consider word proximity and sentence structure
3. **API Interface:** REST API for integration with other systems
4. **Batch Processing:** Analyze multiple messages from a file

### Long-Term Vision
1. **Machine Learning:** Train classifier on labeled data
2. **Sentiment Analysis:** Factor in emotional tone
3. **Entity Recognition:** Extract names, products, dates
4. **Auto-learning:** Improve keyword lists based on feedback

---

## 📂 Project Structure

```
intelligent-chat-tagger/
├── README.md                 # This file
├── tag_config.json          # Tag and keyword configuration
├── main.py                  # Application entry point
├── config_loader.py         # Configuration loading module
├── tagger_service.py        # Core tagging logic
├── scoring_strategy.py      # Scoring algorithm implementations
└── .gitignore              # Git ignore file
```

---

## 🤝 Contributing

This is a POC project. For production use, consider:
- Adding comprehensive unit tests
- Implementing logging
- Adding input validation and sanitization
- Performance optimization for large keyword sets
- Error recovery mechanisms

---

## 📝 License

This project is created as a proof-of-concept for technical assessment purposes.

---

## 👤 Author

KARABO LELAKA

---

## 🙏 Acknowledgments

- Built using Python 3 standard library
- Follows SOLID principles and clean code practices
- Designed for extensibility and maintainability
