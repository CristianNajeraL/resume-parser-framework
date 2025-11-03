"""Unit tests for ResumeExtractor coordinator."""

from typing import Any
from unittest.mock import Mock

import pytest

from resume_parser import ResumeData, ResumeExtractor
from resume_parser.extractors import FieldExtractor


class TestResumeExtractor:
    """Test cases for ResumeExtractor."""

    @pytest.fixture
    def mock_extractors(self) -> dict[str, Mock]:
        """Create mock extractors for testing."""
        name_extractor = Mock(spec=FieldExtractor)
        name_extractor.extract.return_value = "John Doe"

        email_extractor = Mock(spec=FieldExtractor)
        email_extractor.extract.return_value = "john.doe@example.com"

        skills_extractor = Mock(spec=FieldExtractor)
        skills_extractor.extract.return_value = ["Python", "Docker"]

        return {
            "name": name_extractor,
            "email": email_extractor,
            "skills": skills_extractor,
        }

    def test_initialization(self, mock_extractors: dict[str, Mock]) -> None:
        """Test ResumeExtractor initialization."""
        extractor = ResumeExtractor(mock_extractors)

        assert extractor.extractors == mock_extractors
        assert not extractor.allow_partial

    def test_initialization_missing_extractors(self) -> None:
        """Test error when required extractors are missing."""
        incomplete_extractors = {"name": Mock(spec=FieldExtractor)}

        with pytest.raises(ValueError, match="Missing required extractors"):
            ResumeExtractor(incomplete_extractors)

    def test_extract_success(self, mock_extractors: dict[str, Mock]) -> None:
        """Test successful extraction of all fields."""
        extractor = ResumeExtractor(mock_extractors)
        text = "Sample resume text"

        result = extractor.extract(text)

        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == "john.doe@example.com"
        assert result.skills == ["Python", "Docker"]

        # Verify all extractors were called
        mock_extractors["name"].extract.assert_called_once_with(text)
        mock_extractors["email"].extract.assert_called_once_with(text)
        mock_extractors["skills"].extract.assert_called_once_with(text)

    def test_extract_empty_text(self, mock_extractors: dict[str, Mock]) -> None:
        """Test error with empty text."""
        extractor = ResumeExtractor(mock_extractors)

        with pytest.raises(ValueError, match="empty text"):
            extractor.extract("")

    def test_extract_single_field_failure(self, mock_extractors: dict[str, Mock]) -> None:
        """Test extraction fails when one field fails (strict mode)."""
        # Make email extraction fail
        mock_extractors["email"].extract.side_effect = ValueError("No email found")

        extractor = ResumeExtractor(mock_extractors, allow_partial=False)

        with pytest.raises(ValueError, match="Extraction failed"):
            extractor.extract("Sample text")

    def test_extract_partial_success(self, mock_extractors: dict[str, Mock]) -> None:
        """Test partial extraction when one field fails."""
        # Make email extraction fail
        mock_extractors["email"].extract.side_effect = ValueError("No email found")

        extractor = ResumeExtractor(mock_extractors, allow_partial=True)
        result = extractor.extract("Sample text")

        # Should return result with empty email
        assert isinstance(result, ResumeData)
        assert result.name == "John Doe"
        assert result.email == ""  # Failed extraction
        assert result.skills == ["Python", "Docker"]

    def test_extract_multiple_failures(self, mock_extractors: dict[str, Mock]) -> None:
        """Test extraction with multiple field failures."""
        mock_extractors["name"].extract.side_effect = ValueError("No name found")
        mock_extractors["email"].extract.side_effect = ValueError("No email found")

        extractor = ResumeExtractor(mock_extractors, allow_partial=True)
        result = extractor.extract("Sample text")

        assert result.name == ""
        assert result.email == ""
        assert result.skills == ["Python", "Docker"]

    def test_extract_field_single(self, mock_extractors: dict[str, Mock]) -> None:
        """Test extracting a single field."""
        extractor = ResumeExtractor(mock_extractors)

        result = extractor.extract_field("name", "Sample text")

        assert result == "John Doe"
        mock_extractors["name"].extract.assert_called_once_with("Sample text")

    def test_extract_field_not_found(self, mock_extractors: dict[str, Mock]) -> None:
        """Test error when field extractor not configured."""
        extractor = ResumeExtractor(mock_extractors)

        with pytest.raises(KeyError, match="No extractor configured"):
            extractor.extract_field("phone", "Sample text")

    def test_get_configured_fields(self, mock_extractors: dict[str, Mock]) -> None:
        """Test getting list of configured fields."""
        extractor = ResumeExtractor(mock_extractors)

        fields = extractor.get_configured_fields()

        assert "name" in fields
        assert "email" in fields
        assert "skills" in fields
        assert len(fields) == 3

    def test_extract_with_additional_extractors(self) -> None:
        """Test extraction with extra non-required extractors."""
        mock_extractors = {
            "name": Mock(spec=FieldExtractor),
            "email": Mock(spec=FieldExtractor),
            "skills": Mock(spec=FieldExtractor),
            "phone": Mock(spec=FieldExtractor),  # Extra field
        }

        mock_extractors["name"].extract.return_value = "Jane Smith"
        mock_extractors["email"].extract.return_value = "jane@example.com"
        mock_extractors["skills"].extract.return_value = ["Java"]
        mock_extractors["phone"].extract.return_value = "555-1234"

        extractor = ResumeExtractor(mock_extractors)
        result = extractor.extract("Sample text")

        # Should still create valid ResumeData with required fields
        assert result.name == "Jane Smith"
        assert result.email == "jane@example.com"
        assert result.skills == ["Java"]

    @pytest.mark.parametrize(
        "field_name,expected_value",
        [
            ("name", "Alice Brown"),
            ("email", "alice@example.com"),
            ("skills", ["React", "TypeScript"]),
        ],
    )
    def test_extract_various_fields(
        self,
        mock_extractors: dict[str, Mock],
        field_name: str,
        expected_value: Any,
    ) -> None:
        """Test extracting various individual fields."""
        mock_extractors[field_name].extract.return_value = expected_value

        extractor = ResumeExtractor(mock_extractors)
        result = extractor.extract_field(field_name, "Sample text")

        assert result == expected_value
