"""Basic tests for parsers."""

import pytest

from resume_parser.parsers import PDFParser, WordParser


class TestPDFParser:
    def test_parse_nonexistent_file(self):
        parser = PDFParser()
        with pytest.raises(ValueError):
            parser.parse("nonexistent.pdf")


class TestWordParser:
    def test_parse_nonexistent_file(self):
        parser = WordParser()
        with pytest.raises(ValueError):
            parser.parse("nonexistent.docx")
