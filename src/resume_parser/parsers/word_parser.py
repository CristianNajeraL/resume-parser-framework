"""Word document parser."""

from docx import Document

from .base import FileParser


class WordParser(FileParser):
    """Parser for Word documents using python-docx."""

    def parse(self, file_path: str) -> str:
        """Extract text from Word document."""
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        except Exception as e:
            raise ValueError(f"Failed to parse Word document: {e}") from e
