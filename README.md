# LLM Test Generator

A command-line tool that uses a local LLM (via [Ollama](https://ollama.com)) to automatically generate, validate, and fix unit tests for your code.

## Features

- Generate **pytest** (Python) or **XCTest** (Swift/iOS) test suites from a function or description
- Validate generated pytest tests by actually running them
- Auto-fix failing tests using the error output

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) running locally with the `mistral` model pulled

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull the required Ollama model
ollama pull mistral
```

## Usage

```bash
python main.py --input "<your function or description>" [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--input` | **(Required)** The function code or description to generate tests for |
| `--format` | Test format: `pytest` (default) or `xctest` |
| `--validate` | Run the generated pytest tests and show results |
| `--fix` | Auto-fix failing tests using the error output (requires `--validate`) |

### Examples

Generate pytest tests:
```bash
python main.py --input "def add(a, b): return a + b"
```

Generate tests and validate them:
```bash
python main.py --input "def add(a, b): return a + b" --validate
```

Generate, validate, and auto-fix if they fail:
```bash
python main.py --input "def add(a, b): return a + b" --validate --fix
```

Generate XCTest (Swift) tests:
```bash
python main.py --input "func multiply(_ a: Int, _ b: Int) -> Int" --format xctest
```

## Project Structure

```
LLMTestGenerator/
├── main.py          # CLI entry point
├── generator.py     # LLM prompt logic and test generation
├── validator.py     # Runs pytest and captures results
└── requirements.txt # Python dependencies
```
