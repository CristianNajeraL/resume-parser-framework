# Test Fixtures

This directory contains sample files for testing the resume parser.

## Files

- `sample_resume.pdf` - Sample PDF resume with known content
- `sample_resume.docx` - Sample Word resume with known content
- `empty.pdf` - Empty PDF for edge case testing

## Generating Fixtures

From the project root directory, run:

```bash
uv run python tests/fixtures/create_fixtures.py
```

Or from this directory:

```bash
cd tests/fixtures
uv run python create_fixtures.py
```
