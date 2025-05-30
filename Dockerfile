# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Add build argument for OpenAI API key
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .
COPY app.py .

# Expose the port Gradio will run on
EXPOSE 7860

# Set environment variable for Gradio to be accessible from outside the container
ENV GRADIO_SERVER_NAME=0.0.0.0

# Command to run the application
CMD ["python", "app.py"] 