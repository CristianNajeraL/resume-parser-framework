"""Factory for creating file parsers based on extension."""

import logging
from pathlib import Path
from typing import Type

from .base import FileParser
from .pdf_parser import PDFParser
from .word_parser import WordParser

logger = logging.getLogger(__name__)


class ParserFactory:
    """Factory for creating appropriate file parsers based on file extension.

    Supports PDF and Word documents by default, with extensibility through
    constructor injection of custom parsers. Validates all parsers at initialization.

    Example:
        # Use default parsers
        factory = ParserFactory()
        parser = factory.get_parser("resume.pdf")

        # Add custom parser
        factory = ParserFactory(custom_parsers={'.txt': TextParser})
    """

    def __init__(self, custom_parsers: dict[str, Type[FileParser]] | None = None) -> None:
        """Initialize factory with default and/or custom parsers.

        Args:
            custom_parsers: Optional dictionary mapping file extensions to parser classes.
                          Extensions must start with '.' and classes must inherit from FileParser.

        Raises:
            ValueError: If extension format is invalid
            TypeError: If parser class doesn't inherit from FileParser
        """
        # Initialize with default parsers
        self._parsers: dict[str, Type[FileParser]] = {
            ".pdf": PDFParser,
            ".docx": WordParser,
            ".doc": WordParser,  # Support older .doc format
        }

        # Validate and add custom parsers
        if custom_parsers:
            for extension, parser_class in custom_parsers.items():
                self._validate_and_add_parser(extension, parser_class)

        logger.info(f"ParserFactory initialized with {len(self._parsers)} parsers")

    def _validate_and_add_parser(self, extension: str, parser_class: Type[FileParser]) -> None:
        """Validate extension and parser class, then add to registry.

        Args:
            extension: File extension (e.g., '.txt')
            parser_class: Parser class that inherits from FileParser

        Raises:
            ValueError: If extension doesn't start with '.'
            TypeError: If parser_class is not a class or doesn't inherit from FileParser
        """
        # Validate extension format
        if not extension.startswith("."):
            error_msg = f"Extension must start with '.': {extension}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Validate parser_class is a class
        if not isinstance(parser_class, type):
            error_msg = f"Parser must be a class, got {type(parser_class).__name__}"
            logger.error(error_msg)
            raise TypeError(error_msg)

        # Validate parser_class inherits from FileParser
        if not issubclass(parser_class, FileParser):
            error_msg = f"{parser_class.__name__} must inherit from FileParser"
            logger.error(error_msg)
            raise TypeError(error_msg)

        # All validation passed, add parser
        self._parsers[extension.lower()] = parser_class
        logger.debug(f"Added parser {parser_class.__name__} for extension {extension}")

    def get_parser(self, file_path: str) -> FileParser:
        """Get appropriate parser instance for the given file.

        Args:
            file_path: Path to the file to be parsed

        Returns:
            Instance of the appropriate FileParser subclass

        Raises:
            ValueError: If file extension is not supported
        """
        extension = Path(file_path).suffix.lower()

        if not extension:
            logger.error(f"File has no extension: {file_path}")
            raise ValueError(f"File has no extension: {file_path}")

        if extension not in self._parsers:
            supported = ", ".join(sorted(self._parsers.keys()))
            error_msg = f"Unsupported file type: {extension}. Supported extensions: {supported}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        parser_class = self._parsers[extension]
        logger.debug(f"Selected {parser_class.__name__} for {extension}")

        return parser_class()

    def supported_extensions(self) -> list[str]:
        """Get list of supported file extensions.

        Returns:
            Sorted list of supported extensions (e.g., ['.doc', '.docx', '.pdf'])
        """
        return sorted(self._parsers.keys())
