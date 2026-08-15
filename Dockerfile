FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TESSERACT_CMD=/usr/bin/tesseract

# Install system dependencies (Tesseract, poppler for PDF text extraction)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       tesseract-ocr \
       poppler-utils \
       libtiff5-dev \
       libjpeg62-turbo-dev \
       zlib1g-dev \
       libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application
COPY . /app

# Run as non-root for safety
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser || true
USER appuser

EXPOSE 10000

# Run migrations then start the app. Render exposes $PORT at runtime.
CMD ["bash", "-lc", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
