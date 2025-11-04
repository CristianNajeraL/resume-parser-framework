"""Basic tests for extractors."""

from resume_parser.extractors import EmailExtractor, NameExtractor


class TestNameExtractor:
    def test_extract_name(self):
        extractor = NameExtractor()
        text = "John Doe\nSoftware Engineer\njohn@example.com"
        assert extractor.extract(text) == "John Doe"


class TestEmailExtractor:
    def test_extract_email(self):
        extractor = EmailExtractor()
        text = "John Doe\njohn.doe@example.com"
        assert extractor.extract(text) == "john.doe@example.com"
