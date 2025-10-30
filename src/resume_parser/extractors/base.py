"""Base classes for field extractors."""

from abc import ABC, abstractmethod
from typing import Any


class FieldExtractor(ABC):
    """Abstract base class for field extractors.

    Defines the contract for extracting specific fields from resume text.
    Each extractor implements a specific strategy (regex, NER, LLM, etc.)
    for extracting one type of information.
    """

    @abstractmethod
    def extract(self, text: str) -> Any:
        """Extract a specific field from resume text.

        Args:
            text: Raw text content from the resume

        Returns:
            Extracted field value (type depends on field)

        Raises:
            ValueError: If extraction fails or text is invalid
        """
        pass
