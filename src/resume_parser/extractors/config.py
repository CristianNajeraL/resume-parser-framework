"""Configuration for field extractors."""

import logging
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class ExtractorConfig(BaseSettings):
    """Configuration for field extractors.

    Centralizes configuration for all extractors, particularly
    settings that require external resources like API keys.

    Environment variables are automatically loaded and prefixed with
    'EXTRACTOR_' by default (configurable via model_config).

    Examples:
        # From environment variables
        config = ExtractorConfig()

        # With explicit values (overrides environment)
        config = ExtractorConfig(
            gemini_api_key="my_key",
            spacy_model="en_core_web_md"
        )

        # Load from .env file
        config = ExtractorConfig(_env_file=".env")
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Email extractor settings
    email_pattern: Optional[str] = Field(
        default=None,
        description="Custom regex pattern for email extraction",
    )

    # Name extractor settings
    spacy_model: str = Field(
        default="en_core_web_sm",
        description="spaCy model name for NER-based name extraction",
    )

    # Skills extractor settings
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API key for LLM-based skills extraction",
    )

    gemini_model: str = Field(
        default="gemini-pro",
        description="Gemini model name to use for skills extraction",
    )

    use_skills_fallback: bool = Field(
        default=True,
        description="Whether to use keyword fallback if LLM extraction fails",
    )

    @field_validator("gemini_api_key")
    @classmethod
    def warn_if_no_api_key(cls, v: Optional[str]) -> Optional[str]:
        """Warn if no Gemini API key is provided."""
        if not v:
            logger.warning(
                "No Gemini API key configured. Skills extraction will use "
                "keyword fallback only. Set GEMINI_API_KEY environment variable "
                "or pass gemini_api_key to enable LLM-based extraction."
            )
        return v
