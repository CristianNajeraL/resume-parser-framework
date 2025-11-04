"""Main framework for parsing resumes."""

from .extractors import EmailExtractor, ExtractorConfig, NameExtractor, SkillsExtractor
from .models import ResumeData
from .parsers import ParserFactory
from .resume_extractor import ResumeExtractor


class ResumeParserFramework:
    """Simple framework for parsing resumes from PDF and Word documents."""

    def __init__(self, config: ExtractorConfig | None = None) -> None:
        """Initialize with optional configuration."""
        self.config = config or ExtractorConfig()
        self.parser_factory = ParserFactory()
        self.extractor = ResumeExtractor(
            {
                "name": NameExtractor(model_name=self.config.spacy_model),
                "email": EmailExtractor(),
                "skills": SkillsExtractor(
                    api_key=self.config.gemini_api_key,
                    model_name=self.config.gemini_model,
                ),
            }
        )

    def parse_resume(self, file_path: str) -> ResumeData:
        """Parse a resume file and extract structured data."""
        parser = self.parser_factory.get_parser(file_path)
        text = parser.parse(file_path)
        return self.extractor.extract(text)
