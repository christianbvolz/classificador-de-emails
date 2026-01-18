# Use a slim version of Python for a smaller image footprint
FROM python:3.11-slim

# Prevent Python from writing .pyc files and ensure logs are flush straight to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- CRUCIAL: Pre-download NLP models during build ---
# This ensures the container is ready to process text immediately
RUN python -m spacy download pt_core_news_sm && \
    python -m spacy download en_core_web_sm

# Copy the application code
COPY . .

# FastAPI default port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]