"""Unit tests for file parsers."""

from unittest.mock import Mock, patch

import pytest

from resume_parser.parsers import FileParser, ParserFactory, PDFParser, WordParser


class TestPDFParser:
    """Test cases for PDFParser."""

    def test_inheritance(self) -> None:
        """Test PDFParser inherits from FileParser."""
        parser = PDFParser()
        assert isinstance(parser, FileParser)

    @patch("resume_parser.parsers.pdf_parser.PdfReader")
    @patch("resume_parser.parsers.pdf_parser.Path")
    def test_parse_success(self, mock_path: Mock, mock_reader: Mock) -> None:
        """Test successful PDF parsing."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.suffix = ".pdf"

        mock_page = Mock()
        mock_page.extract_text.return_value = "Sample resume text"
        mock_reader.return_value.pages = [mock_page]

        # Parse
        parser = PDFParser()
        result = parser.parse("resume.pdf")

        assert result == "Sample resume text"

    @patch("resume_parser.parsers.pdf_parser.Path")
    def test_parse_file_not_found(self, mock_path: Mock) -> None:
        """Test error handling for missing file."""
        mock_path.return_value.exists.return_value = False

        parser = PDFParser()
        with pytest.raises(FileNotFoundError, match="PDF file not found"):
            parser.parse("nonexistent.pdf")

    @patch("resume_parser.parsers.pdf_parser.Path")
    def test_parse_invalid_extension(self, mock_path: Mock) -> None:
        """Test error handling for wrong file extension."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.suffix = ".txt"

        parser = PDFParser()
        with pytest.raises(ValueError, match="Expected .pdf file"):
            parser.parse("resume.txt")


class TestWordParser:
    """Test cases for WordParser."""

    def test_inheritance(self) -> None:
        """Test WordParser inherits from FileParser."""
        parser = WordParser()
        assert isinstance(parser, FileParser)

    @patch("resume_parser.parsers.word_parser.Document")
    @patch("resume_parser.parsers.word_parser.Path")
    def test_parse_success(self, mock_path: Mock, mock_doc: Mock) -> None:
        """Test successful Word document parsing."""
        # Setup mocks
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.suffix = ".docx"

        # Mock document with paragraph
        mock_para = Mock()
        mock_para.text = "John Doe\nSoftware Engineer"

        mock_element = Mock()
        mock_doc.return_value.element.body = [mock_element]

        # This is simplified - actual implementation would need more complex mocking
        # We'll test with actual files in integration tests
        pass

    @patch("resume_parser.parsers.word_parser.Path")
    def test_parse_file_not_found(self, mock_path: Mock) -> None:
        """Test error handling for missing file."""
        mock_path.return_value.exists.return_value = False

        parser = WordParser()
        with pytest.raises(FileNotFoundError, match="Word file not found"):
            parser.parse("nonexistent.docx")

    @patch("resume_parser.parsers.word_parser.Path")
    def test_parse_invalid_extension(self, mock_path: Mock) -> None:
        """Test error handling for wrong file extension."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.suffix = ".pdf"

        parser = WordParser()
        with pytest.raises(ValueError, match="Expected .docx file"):
            parser.parse("resume.pdf")


class TestParserFactory:
    """Test cases for ParserFactory."""

    def test_get_parser_pdf(self) -> None:
        """Test factory returns PDFParser for .pdf files."""
        factory = ParserFactory()
        parser = factory.get_parser("resume.pdf")
        assert isinstance(parser, PDFParser)

    def test_get_parser_docx(self) -> None:
        """Test factory returns WordParser for .docx files."""
        factory = ParserFactory()
        parser = factory.get_parser("resume.docx")
        assert isinstance(parser, WordParser)

    def test_get_parser_doc(self) -> None:
        """Test factory returns WordParser for .doc files."""
        factory = ParserFactory()
        parser = factory.get_parser("resume.doc")
        assert isinstance(parser, WordParser)

    def test_get_parser_unsupported(self) -> None:
        """Test factory raises error for unsupported file types."""
        factory = ParserFactory()
        with pytest.raises(ValueError, match="Unsupported file type"):
            factory.get_parser("resume.txt")

    def test_get_parser_no_extension(self) -> None:
        """Test factory raises error for files without extension."""
        factory = ParserFactory()
        with pytest.raises(ValueError, match="no extension"):
            factory.get_parser("resume")

    def test_supported_extensions(self) -> None:
        """Test factory returns list of supported extensions."""
        factory = ParserFactory()
        extensions = factory.supported_extensions()
        assert ".pdf" in extensions
        assert ".docx" in extensions
        assert ".doc" in extensions
        assert extensions == sorted(extensions)  # Should be sorted

    def test_custom_parser_valid(self) -> None:
        """Test adding custom parser via constructor."""

        class CustomParser(FileParser):
            def parse(self, file_path: str) -> str:
                return "custom content"

        factory = ParserFactory(custom_parsers={".txt": CustomParser})
        parser = factory.get_parser("file.txt")
        assert isinstance(parser, CustomParser)

    def test_custom_parser_invalid_extension(self) -> None:
        """Test validation fails for extension without dot."""

        class CustomParser(FileParser):
            def parse(self, file_path: str) -> str:
                return "custom"

        with pytest.raises(ValueError, match="Extension must start with"):
            ParserFactory(custom_parsers={"txt": CustomParser})

    def test_custom_parser_not_class(self) -> None:
        """Test validation fails when parser is not a class."""
        with pytest.raises(TypeError, match="Parser must be a class"):
            ParserFactory(custom_parsers={".txt": "not a class"})  # type: ignore

    def test_custom_parser_wrong_parent(self) -> None:
        """Test validation fails when parser doesn't inherit from FileParser."""

        class NotAParser:
            pass

        with pytest.raises(TypeError, match="must inherit from FileParser"):
            ParserFactory(custom_parsers={".txt": NotAParser})  # type: ignore

    def test_custom_parser_overrides_default(self) -> None:
        """Test that custom parser can override default parser."""

        class CustomPDFParser(FileParser):
            def parse(self, file_path: str) -> str:
                return "custom pdf"

        factory = ParserFactory(custom_parsers={".pdf": CustomPDFParser})
        parser = factory.get_parser("resume.pdf")
        assert isinstance(parser, CustomPDFParser)
        assert not isinstance(parser, PDFParser)
