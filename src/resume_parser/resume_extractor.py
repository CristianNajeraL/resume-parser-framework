"""Coordinator for extracting resume fields."""

from .extractors import FieldExtractor
from .models import ResumeData


class ResumeExtractor:
    """Coordinates extraction of all resume fields."""

    def __init__(self, extractors: dict[str, FieldExtractor]) -> None:
        """Initialize with field extractors."""
        self.extractors = extractors

    def extract(self, text: str) -> ResumeData:
        """Extract all fields from resume text."""
        if not text.strip():
            raise ValueError("Text cannot be empty")

        results = {}
        for field_name, extractor in self.extractors.items():
            try:
                results[field_name] = extractor.extract(text)
            except Exception:
                # Use defaults on failure
                results[field_name] = [] if field_name == "skills" else ""

        return ResumeData(
            name=results.get("name", ""),
            email=results.get("email", ""),
            skills=results.get("skills", []),
        )
