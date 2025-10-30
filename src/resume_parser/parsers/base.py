"""Base classes for file parsers."""

from abc import ABC, abstractmethod


class FileParser(ABC):
    """Abstract base class for file parsers.

    Defines the contract that all file parser implementations must follow.
    Each parser is responsible for extracting text content from a specific
    file format (PDF, Word, etc.).
    """

    @abstractmethod
    def parse(self, file_path: str) -> str:
        """Extract text content from a file.

        Args:
            file_path: Path to the file to parse

        Returns:
            Extracted text content as a string

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file format is invalid or corrupted
        """
        pass
