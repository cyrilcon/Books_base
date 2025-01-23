# Build stage
FROM python:3.12-slim AS builder

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir poetry

WORKDIR /usr/src/app/books_base_api

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Final stage
FROM python:3.12-slim

WORKDIR /usr/src/app/books_base_api

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /usr/src/app/books_base_api/api

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]