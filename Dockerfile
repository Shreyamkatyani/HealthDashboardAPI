# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default environment configuration (can be overridden at runtime via docker run -e)
ENV APP_ENV=production
ENV PORT=5000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .

# Expose API port
EXPOSE 5000

# Run the Flask API
CMD ["python", "app.py"]
