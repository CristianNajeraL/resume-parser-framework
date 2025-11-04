"""Email extractor using regex."""

import re

from .base import FieldExtractor


class EmailExtractor(FieldExtractor):
    """Extract email address from resume text."""

    def extract(self, text: str) -> str:
        """Extract email using regex."""
        if not text.strip():
            return ""

        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        match = re.search(pattern, text)
        return match.group(0) if match else ""
