# Use an official Python image as the base
FROM python:3.10-slim

# Set DEBIAN_FRONTEND to noninteractive to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for keyboard input
RUN apt-get update && apt-get install -y \
    libusb-1.0-0-dev \
    kbd \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for production-grade WSGI server
RUN pip install gunicorn

# Install supervisord for process management
# RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copy the supervisord configuration file
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the Flask webserver port
EXPOSE 5000

# Start supervisord to run both processes
# CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
CMD ["python", "rfid.py"]
