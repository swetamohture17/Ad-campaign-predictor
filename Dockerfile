# Base image with Python 3.9 and necessary system tools
FROM python:3.9-slim

# Set environment variables
ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH /app/.local/bin:$PATH

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set up working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]