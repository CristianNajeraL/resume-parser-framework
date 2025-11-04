"""Basic tests for ResumeExtractor."""

import pytest

from resume_parser.extractors import EmailExtractor, NameExtractor
from resume_parser.resume_extractor import ResumeExtractor


class TestResumeExtractor:
    def test_extract(self):
        extractors = {"name": NameExtractor(), "email": EmailExtractor()}
        extractor = ResumeExtractor(extractors)
        text = "John Doe\njohn@example.com"
        data = extractor.extract(text)
        assert data.name == "John Doe"
        assert data.email == "john@example.com"

    def test_extract_empty_text(self):
        extractors = {"name": NameExtractor(), "email": EmailExtractor()}
        extractor = ResumeExtractor(extractors)
        with pytest.raises(ValueError):
            extractor.extract("")
