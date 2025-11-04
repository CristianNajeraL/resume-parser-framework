"""Basic example: Parse a Word resume."""

from pathlib import Path

from resume_parser import ResumeParserFramework

# Framework automatically loads config from environment
framework = ResumeParserFramework()

# Parse resume
resume_path = Path(__file__).parent / "sample_resume.docx"
result = framework.parse_resume(str(resume_path))

# Display results
print(f"Name: {result.name}")
print(f"Email: {result.email}")
print(f"Skills: {', '.join(result.skills)}")
