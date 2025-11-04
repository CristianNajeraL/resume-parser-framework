"""Name extractor using simple pattern matching."""

import re

import spacy

from .base import FieldExtractor


class NameExtractor(FieldExtractor):
    """Extract candidate name from resume text."""

    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        """Initialize with spaCy model."""
        self.nlp = spacy.load(model_name)

    def extract(self, text: str) -> str:
        """Extract name from resume text."""
        if not text.strip():
            return ""

        # Try first line
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if lines:
            first_line = lines[0]
            # Handle titles (e.g., "John Doe - Software Engineer")
            for sep in [" - ", " | ", " — "]:
                if sep in first_line:
                    first_line = first_line.split(sep)[0].strip()

            # Check if it looks like a name
            name_pattern = r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+$"
            if re.match(name_pattern, first_line):
                return first_line

        # Fallback to NER
        doc = self.nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name: str = ent.text.strip()
                return name

        return ""
