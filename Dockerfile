# ┌──────────────────────────────────────────────┐
# │ Project : Rulingvo AI System                 │
# │ Author  : Mr.DosMa                           │
# │ Year    : 2025                               │
# │ Langs   : Uzbek / English / Russian          │
# ├──────────────────────────────────────────────┤
# │ Ushbu kod Rulingvo loyihasiga tegishli.     │
# │ This code is property of Rulingvo Project.   │
# │ Этот код принадлежит проекту Rulingvo.      │
# └──────────────────────────────────────────────┘

FROM ubuntu:latest
LABEL authors="Win11"

ENTRYPOINT ["top", "-b"]



# Dockerfile for Russian Learner Bot
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/temp /app/audio /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port (if using webhooks)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the bot
CMD ["python", "bot.py"]