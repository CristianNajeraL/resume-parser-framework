# Multi-stage build for minimal final image size
FROM python:3.11-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files and source code (needed for editable install)
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen

# Download spaCy model using pip (install pip first)
RUN uv pip install --python /app/.venv/bin/python en-core-web-sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl


# Final stage - smaller runtime image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY examples/ ./examples/
COPY pyproject.toml .
COPY README.md .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import resume_parser; print('OK')" || exit 1

# Default command - run tests
CMD ["pytest", "tests/", "-v"]
