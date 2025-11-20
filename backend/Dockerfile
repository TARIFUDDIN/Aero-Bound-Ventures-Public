FROM python:3.12-slim

# Install curl & unzip
RUN apt-get update && apt-get install -y curl unzip && apt-get clean

# Install uv (the correct Astral version)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Sync dependencies (creates .venv)
RUN uv sync --frozen --no-cache

# Use uvicorn inside the uv-created virtual env
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
