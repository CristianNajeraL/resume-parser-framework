"""Data models for resume parsing."""

import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class ResumeData:
    """Encapsulates extracted resume information.

    Attributes:
        name: Full name of the candidate
        email: Email address of the candidate
        skills: List of technical or professional skills
        allow_partial: If True, allows empty name/email for partial extraction
    """

    name: str
    email: str
    skills: List[str] = field(default_factory=list)
    allow_partial: bool = field(default=False, repr=False, compare=False)

    def to_dict(self) -> dict[str, str | List[str]]:
        """Convert resume data to dictionary format.

        Returns:
            Dictionary with name, email, and skills fields
        """
        return {"name": self.name, "email": self.email, "skills": self.skills}

    def to_json(self) -> str:
        """Convert resume data to JSON string.

        Returns:
            JSON formatted string representation
        """
        return json.dumps(self.to_dict(), indent=2)

    def __post_init__(self) -> None:
        """Validate resume data after initialization."""
        if not isinstance(self.skills, list):
            raise TypeError("skills must be a list")

        # Only validate non-empty name/email in strict mode
        if not self.allow_partial:
            if not self.name:
                raise ValueError("name cannot be empty")
            if not self.email:
                raise ValueError("email cannot be empty")
