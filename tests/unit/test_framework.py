"""Basic tests for framework."""

import pytest

from resume_parser import ResumeParserFramework


class TestResumeParserFramework:
    def test_initialization(self):
        framework = ResumeParserFramework()
        assert framework.extractor is not None

    def test_parse_nonexistent_file(self):
        framework = ResumeParserFramework()
        with pytest.raises(ValueError):
            framework.parse_resume("nonexistent.pdf")
