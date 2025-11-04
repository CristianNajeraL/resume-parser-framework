# Resume Parser Framework

A Python framework for parsing resumes from PDF and Word documents using Object-Oriented Design principles.

## Installation

```bash
# Clone the repository
git clone https://github.com/CristianNajeraL/resume-parser-framework.git
cd resume-parser-framework

# Install dependencies
uv sync

# Install spaCy model
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Set up API key (create .env file)
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

```bash
# Run the PDF example
uv run python examples/basic_pdf_example.py

# Run the Word example
uv run python examples/basic_word_example.py
```

## Run Tests

```bash
uv run pytest
```

## Docker

```bash
# Build
docker-compose build

# Run example
docker-compose run --rm examples

# Run tests
docker-compose run --rm resume-parser pytest
```
