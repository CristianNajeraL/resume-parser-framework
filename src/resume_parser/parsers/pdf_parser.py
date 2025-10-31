"""PDF file parser implementation."""

import logging
from pathlib import Path

from pypdf import PdfReader

from .base import FileParser

logger = logging.getLogger(__name__)


class PDFParser(FileParser):
    """Parser for PDF files using pypdf library.

    Extracts text content from all pages of a PDF document.
    Handles multi-page documents and basic error cases.
    """

    def parse(self, file_path: str) -> str:
        """Extract text content from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content from all pages

        Raises:
            FileNotFoundError: If the PDF file does not exist
            ValueError: If the file format is invalid or corrupted
        """
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            logger.error(f"PDF file not found: {file_path}")
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        # Validate file extension
        if path.suffix.lower() != ".pdf":
            logger.error(f"Invalid file extension: {path.suffix}")
            raise ValueError(f"Expected .pdf file, got {path.suffix}")

        try:
            reader = PdfReader(str(path))

            # Check if PDF has pages
            if len(reader.pages) == 0:
                logger.warning(f"PDF file has no pages: {file_path}")
                return ""

            # Extract text from all pages
            text_parts: list[str] = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                    logger.debug(f"Extracted text from page {page_num}")

            full_text = "\n".join(text_parts)
            logger.info(f"Successfully extracted {len(full_text)} characters from PDF")

            return full_text

        except Exception as e:
            logger.error(f"Failed to parse PDF: {e}")
            raise ValueError(f"Failed to parse PDF file: {e}") from e
