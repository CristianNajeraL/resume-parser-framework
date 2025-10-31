"""Word document parser implementation."""

import logging
from pathlib import Path

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

from .base import FileParser

logger = logging.getLogger(__name__)


class WordParser(FileParser):
    """Parser for Word documents using python-docx library.

    Extracts text from paragraphs and tables in .docx files.
    Handles various document structures common in resumes.
    """

    def parse(self, file_path: str) -> str:
        """Extract text content from a Word document.

        Args:
            file_path: Path to the Word document

        Returns:
            Extracted text content from paragraphs and tables

        Raises:
            FileNotFoundError: If the Word file does not exist
            ValueError: If the file is corrupted or not a valid .docx
        """
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            logger.error(f"Word file not found: {file_path}")
            raise FileNotFoundError(f"Word file not found: {file_path}")

        # Validate file extension
        if path.suffix.lower() not in [".docx", ".doc"]:
            logger.error(f"Invalid file extension: {path.suffix}")
            raise ValueError(f"Expected .docx file, got {path.suffix}")

        try:
            doc = Document(str(path))
            text_parts: list[str] = []

            # Extract text from document body elements in order
            for element in doc.element.body:
                if isinstance(element, CT_P):
                    # Paragraph
                    para = Paragraph(element, doc)
                    if para.text.strip():
                        text_parts.append(para.text)

                elif isinstance(element, CT_Tbl):
                    # Table
                    table = Table(element, doc)
                    table_text = self._extract_table_text(table)
                    if table_text:
                        text_parts.append(table_text)

            full_text = "\n".join(text_parts)
            logger.info(f"Successfully extracted {len(full_text)} characters from Word document")

            return full_text

        except Exception as e:
            logger.error(f"Failed to parse Word document: {e}")
            raise ValueError(f"Failed to parse Word document: {e}") from e

    def _extract_table_text(self, table: Table) -> str:
        """Extract text from a table.

        Args:
            table: Table object from python-docx

        Returns:
            Concatenated text from all table cells
        """
        table_text: list[str] = []

        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text:
                    table_text.append(cell_text)

        return " ".join(table_text)
