"""PDF file parser."""

from pypdf import PdfReader

from .base import FileParser


class PDFParser(FileParser):
    """Parser for PDF files using pypdf."""

    def parse(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(file_path)
            text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
            return "\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {e}") from e
