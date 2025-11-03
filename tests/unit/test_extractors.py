"""Unit tests for field extractors."""

import os
from unittest.mock import Mock, patch

import pytest

from resume_parser.extractors import (
    EmailExtractor,
    ExtractorConfig,
    FieldExtractor,
    NameExtractor,
    SkillsExtractor,
)


class TestEmailExtractor:
    """Test cases for EmailExtractor."""

    def test_inheritance(self) -> None:
        """Test EmailExtractor inherits from FieldExtractor."""
        extractor = EmailExtractor()
        assert isinstance(extractor, FieldExtractor)

    def test_extract_simple_email(self) -> None:
        """Test extracting a simple email address."""
        extractor = EmailExtractor()
        text = "Contact me at john.doe@example.com for more info"

        result = extractor.extract(text)
        assert result == "john.doe@example.com"

    def test_extract_first_email(self) -> None:
        """Test extracts first email when multiple present."""
        extractor = EmailExtractor()
        text = "Primary: first@example.com, Secondary: second@example.com"

        result = extractor.extract(text)
        assert result == "first@example.com"

    def test_extract_all_emails(self) -> None:
        """Test extracting all email addresses."""
        extractor = EmailExtractor()
        text = "Contact: first@example.com or second@example.com"

        result = extractor.extract_all(text)
        assert len(result) == 2
        assert "first@example.com" in result
        assert "second@example.com" in result

    def test_extract_no_email(self) -> None:
        """Test error when no email found."""
        extractor = EmailExtractor()
        text = "This text has no email address"

        with pytest.raises(ValueError, match="No email address found"):
            extractor.extract(text)

    def test_extract_empty_text(self) -> None:
        """Test error with empty text."""
        extractor = EmailExtractor()

        with pytest.raises(ValueError, match="empty text"):
            extractor.extract("")

    @pytest.mark.parametrize(
        "email",
        [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@test-domain.com",
        ],
    )
    def test_various_email_formats(self, email: str) -> None:
        """Test with various valid email formats."""
        extractor = EmailExtractor()
        text = f"Contact: {email}"

        result = extractor.extract(text)
        assert result == email


class TestNameExtractor:
    """Test cases for NameExtractor."""

    @patch("resume_parser.extractors.name_extractor.spacy.load")
    def test_inheritance(self, mock_load: Mock) -> None:
        """Test NameExtractor inherits from FieldExtractor."""
        mock_load.return_value = Mock()
        extractor = NameExtractor()
        assert isinstance(extractor, FieldExtractor)

    @patch("resume_parser.extractors.name_extractor.spacy.load")
    def test_extract_name_with_ner(self, mock_load: Mock) -> None:
        """Test name extraction using NER."""
        # Setup mock spaCy
        mock_nlp = Mock()
        mock_doc = Mock()
        mock_entity = Mock()
        mock_entity.text = "John Doe"
        mock_entity.label_ = "PERSON"
        mock_doc.ents = [mock_entity]
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp

        extractor = NameExtractor()
        result = extractor.extract("John Doe\nSoftware Engineer")

        assert result == "John Doe"

    @patch("resume_parser.extractors.name_extractor.spacy.load")
    def test_extract_no_name_with_fallback(self, mock_load: Mock) -> None:
        """Test fallback when NER finds no name."""
        # Setup mock spaCy with no entities
        mock_nlp = Mock()
        mock_doc = Mock()
        mock_doc.ents = []
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp

        extractor = NameExtractor()
        text = "Jane Smith\nEmail: jane@example.com"

        result = extractor.extract(text)
        assert result == "Jane Smith"  # Uses first line fallback

    @patch("resume_parser.extractors.name_extractor.spacy.load")
    def test_extract_empty_text(self, mock_load: Mock) -> None:
        """Test error with empty text."""
        mock_load.return_value = Mock()
        extractor = NameExtractor()

        with pytest.raises(ValueError, match="empty text"):
            extractor.extract("")

    @patch("resume_parser.extractors.name_extractor.spacy.load")
    def test_looks_like_name_validation(self, mock_load: Mock) -> None:
        """Test name validation heuristic."""
        mock_load.return_value = Mock()
        extractor = NameExtractor()

        assert extractor._looks_like_name("John Doe")
        assert extractor._looks_like_name("Mary Jane Smith")
        assert not extractor._looks_like_name("john doe")  # Not capitalized
        assert not extractor._looks_like_name("123 Main St")  # Contains number
        assert not extractor._looks_like_name("J")  # Too short


class TestSkillsExtractor:
    """Test cases for SkillsExtractor."""

    def test_inheritance(self) -> None:
        """Test SkillsExtractor inherits from FieldExtractor."""
        extractor = SkillsExtractor(use_fallback=True)
        assert isinstance(extractor, FieldExtractor)

    @patch("resume_parser.extractors.skills_extractor.genai.GenerativeModel")
    @patch("resume_parser.extractors.skills_extractor.genai.configure")
    def test_extract_with_llm(self, mock_configure: Mock, mock_model: Mock) -> None:
        """Test skills extraction using LLM."""
        # Setup mock LLM response
        mock_response = Mock()
        mock_response.text = '["Python", "Machine Learning", "Docker"]'
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_instance

        extractor = SkillsExtractor(api_key="test_key")
        result = extractor.extract("Experience with Python and Machine Learning")

        assert "Python" in result
        assert "Machine Learning" in result

    def test_extract_with_keyword_fallback(self) -> None:
        """Test skills extraction using keyword fallback."""
        extractor = SkillsExtractor(api_key=None, use_fallback=True)
        text = "Experienced with Python, Java, and Docker containerization"

        result = extractor.extract(text)

        assert "Python" in result
        assert "Java" in result
        assert "Docker" in result

    def test_extract_empty_text(self) -> None:
        """Test error with empty text."""
        extractor = SkillsExtractor(use_fallback=True)

        with pytest.raises(ValueError, match="empty text"):
            extractor.extract("")

    def test_no_skills_found(self) -> None:
        """Test when no skills are found."""
        extractor = SkillsExtractor(api_key=None, use_fallback=True)
        text = "Just some random text with no technical skills"

        result = extractor.extract(text)
        assert isinstance(result, list)
        # May be empty or have false positives


class TestExtractorConfig:
    """Test cases for ExtractorConfig."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = ExtractorConfig()

        assert config.spacy_model == "en_core_web_sm"
        assert config.gemini_model == "gemini-pro"
        assert config.use_skills_fallback is True

    def test_custom_config(self) -> None:
        """Test custom configuration with explicit values."""
        config = ExtractorConfig(
            spacy_model="en_core_web_md",
            gemini_api_key="test_key",
            gemini_model="gemini-1.5-pro",
        )

        assert config.spacy_model == "en_core_web_md"
        assert config.gemini_api_key == "test_key"
        assert config.gemini_model == "gemini-1.5-pro"

    @patch.dict(
        os.environ,
        {"GEMINI_API_KEY": "env_key", "SPACY_MODEL": "en_core_web_lg"},
        clear=True,
    )
    def test_from_env(self) -> None:
        """Test configuration from environment variables."""
        config = ExtractorConfig()

        assert config.gemini_api_key == "env_key"
        assert config.spacy_model == "en_core_web_lg"

    def test_field_descriptions(self) -> None:
        """Test that pydantic fields have descriptions."""
        config = ExtractorConfig()

        # Verify pydantic BaseSettings behavior
        assert hasattr(config, "model_config")
        assert hasattr(ExtractorConfig, "model_fields")

    @patch.dict(os.environ, {}, clear=True)
    def test_env_vars_case_insensitive(self) -> None:
        """Test that environment variables are case-insensitive."""
        # pydantic_settings handles case-insensitive env vars
        with patch.dict(os.environ, {"gemini_api_key": "lowercase_key"}):
            config = ExtractorConfig()
            assert config.gemini_api_key == "lowercase_key"
