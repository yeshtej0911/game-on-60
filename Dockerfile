FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
COPY prompts ./prompts
RUN pip install --no-cache-dir -e .
RUN mkdir -p /app/output /app/assets/approved
EXPOSE 8080
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
