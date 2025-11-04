"""Resume parser framework for extracting structured information from resumes."""

from .extractors import (
    EmailExtractor,
    ExtractorConfig,
    FieldExtractor,
    NameExtractor,
    SkillsExtractor,
)
from .framework import ResumeParserFramework
from .models import ResumeData
from .parsers import FileParser, ParserFactory, PDFParser, WordParser
from .resume_extractor import ResumeExtractor

__version__ = "1.0.0"

__all__ = [
    # Models
    "ResumeData",
    # Parsers
    "FileParser",
    "PDFParser",
    "WordParser",
    "ParserFactory",
    # Extractors
    "FieldExtractor",
    "EmailExtractor",
    "NameExtractor",
    "SkillsExtractor",
    "ExtractorConfig",
    # Coordinator
    "ResumeExtractor",
    # Framework
    "ResumeParserFramework",
]
