# Multi-stage build for optimization
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r scraper \
    && useradd -r -g scraper scraper

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY exito_scraper/ ./exito_scraper/
COPY format_json.py clean_existing_json.py ./
COPY requirements.txt ./

# Create data directory
RUN mkdir -p /app/data && \
    chown -R scraper:scraper /app

# Switch to non-root user
USER scraper

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import exito_scraper; print('Health check OK')" || exit 1

# Default command
CMD ["python", "-m", "exito_scraper.main", "--help"]

# Labels for metadata
LABEL maintainer="your-email@example.com" \
      version="1.0" \
      description="Exito E-commerce Scraper" \
      org.opencontainers.image.source="https://github.com/your-username/scrapper-exito"
