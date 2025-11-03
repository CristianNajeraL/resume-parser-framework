"""Name field extractor using NER and rule-based heuristics."""

import logging

import spacy
from spacy.language import Language

from .base import FieldExtractor

logger = logging.getLogger(__name__)


class NameExtractor(FieldExtractor):
    """Extract candidate name using NER and heuristics.

    Uses spaCy's NER to identify PERSON entities, combined with
    heuristics based on resume structure (name typically appears first).
    """

    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        """Initialize the name extractor with spaCy model.

        Args:
            model_name: Name of the spaCy model to use
        """
        try:
            self.nlp: Language = spacy.load(model_name)
            logger.info(f"Loaded spaCy model: {model_name}")
        except OSError as e:
            logger.error(f"spaCy model '{model_name}' not found")
            raise ValueError(
                f"spaCy model '{model_name}' not found. "
                f"Install with: python -m spacy download {model_name}"
            ) from e

    def extract(self, text: str) -> str:
        """Extract candidate name from resume text.

        Strategy:
        1. Focus on first 500 characters where name usually appears
        2. Use NER to find PERSON entities
        3. Return the first person name found

        Args:
            text: Resume text to extract name from

        Returns:
            Candidate's full name

        Raises:
            ValueError: If no name is found in the text
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to NameExtractor")
            raise ValueError("Cannot extract name from empty text")

        # Focus on first part of resume where name typically appears
        # This improves accuracy by avoiding false positives later in text
        header_text = text[:500]

        # Process with spaCy
        doc = self.nlp(header_text)

        # Extract PERSON entities
        person_names: list[str] = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

        if not person_names:
            logger.warning("No person name found using NER")
            # Try fallback: first line if it looks like a name
            first_line = text.split("\n")[0].strip()
            if self._looks_like_name(first_line):
                logger.info(f"Using fallback - first line as name: {first_line}")
                return first_line
            raise ValueError("No name found in resume")

        # Return the first person name found
        name: str = person_names[0]
        logger.info(f"Extracted name: {name}")

        return name

    def _looks_like_name(self, text: str) -> bool:
        """Check if text looks like a person's name.

        Simple heuristic: 2-4 capitalized words, no special chars.

        Args:
            text: Text to check

        Returns:
            True if text appears to be a name
        """
        words = text.split()

        # Name should be 2-4 words
        if len(words) < 2 or len(words) > 4:
            return False

        # All words should be capitalized
        if not all(word[0].isupper() for word in words if word):
            return False

        # Should not contain numbers or special characters (except . and ')
        if any(char.isdigit() for char in text):
            return False

        return True
