"""Basic tests to verify project setup."""


def test_import_resume_parser() -> None:
    """Test that the resume_parser package can be imported."""
    import resume_parser  # noqa: F401


def test_import_extractors() -> None:
    """Test that the extractors module can be imported."""
    from resume_parser import extractors  # noqa: F401


def test_import_models() -> None:
    """Test that the models module can be imported."""
    from resume_parser import models  # noqa: F401


def test_import_parsers() -> None:
    """Test that the parsers module can be imported."""
    from resume_parser import parsers  # noqa: F401
