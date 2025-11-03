"""Coordinator for extracting all resume fields."""

import logging
from typing import Any

from .extractors import FieldExtractor
from .models import ResumeData

logger = logging.getLogger(__name__)


class ResumeExtractor:
    """Coordinates extraction of all resume fields.

    Takes a dictionary of field extractors and orchestrates the
    extraction process, handling errors gracefully and supporting
    partial extraction when some fields fail.
    """

    def __init__(self, extractors: dict[str, FieldExtractor], allow_partial: bool = False) -> None:
        """Initialize the resume extractor.

        Args:
            extractors: Dictionary mapping field names to extractor instances
                Expected keys: "name", "email", "skills"
            allow_partial: If True, allow partial extraction when some fields fail
        """
        self.extractors = extractors
        self.allow_partial = allow_partial

        # Validate required extractors
        required_fields = {"name", "email", "skills"}
        provided_fields = set(extractors.keys())

        if not required_fields.issubset(provided_fields):
            missing = required_fields - provided_fields
            raise ValueError(f"Missing required extractors: {missing}")

        logger.info(f"ResumeExtractor initialized with extractors: {list(extractors.keys())}")

    def extract(self, text: str) -> ResumeData:
        """Extract all fields from resume text.

        Coordinates extraction of name, email, and skills from the
        provided text using the configured extractors.

        Args:
            text: Raw resume text to extract fields from

        Returns:
            ResumeData object with extracted information

        Raises:
            ValueError: If extraction fails and partial extraction not allowed
        """
        if not text or not text.strip():
            raise ValueError("Cannot extract from empty text")

        logger.info("Starting resume field extraction")

        # Extract each field
        results: dict[str, Any] = {}
        errors: dict[str, str] = {}

        for field_name, extractor in self.extractors.items():
            try:
                logger.debug(f"Extracting field: {field_name}")
                value = extractor.extract(text)
                results[field_name] = value
                logger.info(f"Successfully extracted {field_name}: {value}")

            except Exception as e:
                error_msg = f"Failed to extract {field_name}: {str(e)}"
                logger.error(error_msg)
                errors[field_name] = error_msg

                # Set default values for failed extractions
                if field_name == "skills":
                    results[field_name] = []
                else:
                    results[field_name] = ""

        # Handle extraction errors
        if errors:
            if not self.allow_partial:
                error_summary = "; ".join(errors.values())
                raise ValueError(f"Extraction failed: {error_summary}")
            else:
                logger.warning(f"Partial extraction completed with {len(errors)} errors: {errors}")

        # Create and return ResumeData
        try:
            resume_data = ResumeData(
                name=results["name"],
                email=results["email"],
                skills=results["skills"],
                allow_partial=self.allow_partial,
            )
            logger.info("Resume data extraction completed successfully")
            return resume_data

        except Exception as e:
            logger.error(f"Failed to create ResumeData: {e}")
            raise ValueError(f"Failed to create resume data: {e}") from e

    def extract_field(self, field_name: str, text: str) -> Any:
        """Extract a single field from text.

        Utility method for extracting individual fields.

        Args:
            field_name: Name of the field to extract
            text: Resume text

        Returns:
            Extracted field value

        Raises:
            KeyError: If field extractor not found
            ValueError: If extraction fails
        """
        if field_name not in self.extractors:
            raise KeyError(f"No extractor configured for field: {field_name}")

        extractor = self.extractors[field_name]
        return extractor.extract(text)

    def get_configured_fields(self) -> list[str]:
        """Get list of configured field extractors.

        Returns:
            List of field names that have extractors configured
        """
        return list(self.extractors.keys())
