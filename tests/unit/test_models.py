"""Unit tests for resume data models."""

import json

import pytest

from resume_parser.models import ResumeData


class TestResumeData:
    """Test cases for ResumeData dataclass."""

    def test_instantiation(self) -> None:
        """Test basic instantiation of ResumeData."""
        resume = ResumeData(
            name="Jane Doe", email="jane.doe@example.com", skills=["Python", "Machine Learning"]
        )

        assert resume.name == "Jane Doe"
        assert resume.email == "jane.doe@example.com"
        assert resume.skills == ["Python", "Machine Learning"]

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        resume = ResumeData(name="John Smith", email="john@example.com", skills=["Java", "Docker"])

        result = resume.to_dict()

        assert result["name"] == "John Smith"
        assert result["email"] == "john@example.com"
        assert result["skills"] == ["Java", "Docker"]
        assert isinstance(result, dict)

    def test_to_json(self) -> None:
        """Test conversion to JSON string."""
        resume = ResumeData(
            name="Alice Brown", email="alice@example.com", skills=["React", "TypeScript"]
        )

        result = resume.to_json()
        parsed = json.loads(result)

        assert parsed["name"] == "Alice Brown"
        assert parsed["email"] == "alice@example.com"
        assert parsed["skills"] == ["React", "TypeScript"]

    def test_empty_skills_list(self) -> None:
        """Test with empty skills list."""
        resume = ResumeData(name="Bob Wilson", email="bob@example.com", skills=[])

        assert resume.skills == []
        assert isinstance(resume.skills, list)

    def test_default_skills(self) -> None:
        """Test default empty skills list."""
        resume = ResumeData(name="Carol Davis", email="carol@example.com")

        assert resume.skills == []

    def test_validation_empty_name(self) -> None:
        """Test validation fails with empty name."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            ResumeData(name="", email="test@example.com")

    def test_validation_empty_email(self) -> None:
        """Test validation fails with empty email."""
        with pytest.raises(ValueError, match="email cannot be empty"):
            ResumeData(name="Test User", email="")

    def test_validation_invalid_skills_type(self) -> None:
        """Test validation fails with non-list skills."""
        with pytest.raises(TypeError, match="skills must be a list"):
            ResumeData(
                name="Test User",
                email="test@example.com",
                skills="Python",  # type: ignore
            )

    @pytest.mark.parametrize(
        "name,email,skills",
        [
            ("John Doe", "john@example.com", ["Python"]),
            ("Jane Smith", "jane.smith@company.co.uk", ["Java", "Kotlin"]),
            ("Bob O'Brien", "bob+test@example.com", ["JavaScript", "Node.js", "React"]),
        ],
    )
    def test_various_valid_inputs(self, name: str, email: str, skills: list[str]) -> None:
        """Test with various valid input combinations."""
        resume = ResumeData(name=name, email=email, skills=skills)

        assert resume.name == name
        assert resume.email == email
        assert resume.skills == skills
