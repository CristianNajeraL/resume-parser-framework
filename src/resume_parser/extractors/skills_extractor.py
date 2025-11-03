"""Skills field extractor using LLM (Google Gemini)."""

# mypy: disable-error-code="import-untyped,attr-defined,union-attr"

import json
import logging
import os
from typing import Any, Optional

import google.generativeai as genai

from .base import FieldExtractor

logger = logging.getLogger(__name__)


class SkillsExtractor(FieldExtractor):
    """Extract technical skills using LLM (Google Gemini).

    Uses a language model to intelligently identify technical and
    professional skills from resume text. Falls back to keyword
    matching if LLM is unavailable.
    """

    # Common technical skills for fallback
    COMMON_SKILLS = [
        "Python",
        "Java",
        "JavaScript",
        "C++",
        "C#",
        "Ruby",
        "Go",
        "Rust",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Django",
        "Flask",
        "Spring",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "GCP",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision",
        "SQL",
        "PostgreSQL",
        "MongoDB",
        "Redis",
        "Git",
        "CI/CD",
        "Agile",
        "Scrum",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-pro",
        use_fallback: bool = True,
    ) -> None:
        """Initialize the skills extractor.

        Args:
            api_key: Google Gemini API key (or None to use env var)
            model_name: Name of the Gemini model to use
            use_fallback: Whether to use keyword fallback if LLM fails
        """
        self.use_fallback = use_fallback
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model: Optional[Any] = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"Initialized Gemini model: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
                self.model = None
        else:
            logger.warning("No API key provided, will use fallback method")

    def extract(self, text: str) -> list[str]:
        """Extract skills from resume text.

        Args:
            text: Resume text to extract skills from

        Returns:
            List of technical and professional skills

        Raises:
            ValueError: If extraction fails and no fallback is available
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to SkillsExtractor")
            raise ValueError("Cannot extract skills from empty text")

        # Try LLM extraction first
        if self.model:
            try:
                skills = self._extract_with_llm(text)
                if skills:
                    return skills
            except Exception as e:
                logger.warning(f"LLM extraction failed: {e}")

        # Fall back to keyword matching
        if self.use_fallback:
            logger.info("Using fallback keyword matching")
            return self._extract_with_keywords(text)

        raise ValueError("Skills extraction failed and fallback is disabled")

    def _extract_with_llm(self, text: str) -> list[str]:
        """Extract skills using LLM.

        Args:
            text: Resume text

        Returns:
            List of extracted skills
        """
        prompt = f"""Analyze the following resume text and extract all technical skills,
programming languages, frameworks, tools, and technologies mentioned.

Return ONLY a JSON array of skills, nothing else. Example format:
["Python", "Machine Learning", "Docker", "AWS"]

Resume text:
{text[:2000]}

JSON array of skills:"""

        response = self.model.generate_content(prompt)
        response_text = response.text.strip()

        # Parse JSON response
        try:
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]

            skills = json.loads(response_text)

            if not isinstance(skills, list):
                raise ValueError("Response is not a list")

            # Filter and clean skills
            skills = [s.strip() for s in skills if isinstance(s, str) and s.strip()]
            logger.info(f"Extracted {len(skills)} skills using LLM")

            return skills

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise

    def _extract_with_keywords(self, text: str) -> list[str]:
        """Extract skills using keyword matching (fallback).

        Args:
            text: Resume text

        Returns:
            List of matched skills
        """
        text_lower = text.lower()
        found_skills: list[str] = []

        for skill in self.COMMON_SKILLS:
            # Case-insensitive match
            if skill.lower() in text_lower:
                found_skills.append(skill)

        if not found_skills:
            logger.warning("No skills found even with keyword matching")
        else:
            logger.info(f"Extracted {len(found_skills)} skills using keywords")

        return found_skills
