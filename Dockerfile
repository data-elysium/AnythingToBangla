# Use Python 3.10.12 slim image as base
FROM python:3.10.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies including audio-related packages
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    python3-dev \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY voice_translator.py .

ENV GRADIO_SERVER_NAME="0.0.0.0"

# Expose the port Gradio will run on (default is 7860)
EXPOSE 7860

# Command to run the application
CMD ["python", "voice_translator.py"]