"""Skills extractor using Google Gemini LLM."""

import json
from typing import Any, Optional

import google.generativeai as genai

from .base import FieldExtractor


class SkillsExtractor(FieldExtractor):
    """Extract technical skills using Google Gemini."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash") -> None:
        """Initialize with Gemini API key and model name."""
        self.model: Optional[Any] = None
        if api_key:
            try:
                genai.configure(api_key=api_key)  # type: ignore[attr-defined]
                self.model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
            except Exception:
                pass

    def extract(self, text: str) -> list[str]:
        """Extract skills from resume text."""
        if not text.strip():
            return []

        if self.model:
            try:
                prompt = f"""Extract all technical skills from this resume.
Return ONLY a JSON array of skills like: ["Python", "Docker", "AWS"]

Resume: {text[:2000]}

Skills:"""
                response = self.model.generate_content(prompt)
                response_text = response.text.strip()

                # Remove markdown if present
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]

                skills = json.loads(response_text)
                if isinstance(skills, list):
                    return [s.strip() for s in skills if isinstance(s, str) and s.strip()]
            except Exception:
                pass

        # Fallback: return empty list
        return []
