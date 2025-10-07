# Use a recent, minimal Python image
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Ensure reliable DNS and network during build
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first
COPY requirements.txt .

# Configure pip to use a reliable mirror (helps if PyPI is slow)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple

# Copy all app files
COPY . .

# Expose Flask port
EXPOSE 5000

# Default environment variable for Flask
ENV FLASK_ENV=development

# Command to run the app
CMD ["python", "app.py"]
