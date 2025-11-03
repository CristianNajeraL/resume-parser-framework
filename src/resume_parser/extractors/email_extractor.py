"""Email field extractor using regex."""

import logging
import re

from .base import FieldExtractor

logger = logging.getLogger(__name__)


class EmailExtractor(FieldExtractor):
    """Extract email address using regex pattern matching.

    Uses a comprehensive regex pattern to identify valid email addresses
    in resume text. Returns the first valid email found.
    """

    # Comprehensive email regex pattern
    # Handles most common email formats
    EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def __init__(self) -> None:
        """Initialize the email extractor."""
        self.pattern = re.compile(self.EMAIL_PATTERN)
        logger.debug("EmailExtractor initialized with regex pattern")

    def extract(self, text: str) -> str:
        """Extract email address from text.

        Args:
            text: Resume text to extract email from

        Returns:
            First valid email address found

        Raises:
            ValueError: If no email address is found in the text
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to EmailExtractor")
            raise ValueError("Cannot extract email from empty text")

        # Find all email matches
        matches = self.pattern.findall(text)

        if not matches:
            logger.warning("No email address found in text")
            raise ValueError("No email address found in resume")

        # Return the first email found
        email: str = matches[0]
        logger.info(f"Extracted email: {email}")

        return email

    def extract_all(self, text: str) -> list[str]:
        """Extract all email addresses from text.

        Utility method to get all emails if multiple are present.

        Args:
            text: Resume text to extract emails from

        Returns:
            List of all email addresses found
        """
        if not text or not text.strip():
            return []

        matches = self.pattern.findall(text)
        logger.debug(f"Found {len(matches)} email addresses")

        return matches
