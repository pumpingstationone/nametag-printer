# Use an official Python image as the base
FROM python:3.13-slim

# Install uv, following their official instructions
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# Pinned to a specific version for stability
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /uvx /bin/

# Set DEBIAN_FRONTEND to noninteractive to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    # Printer access
    libusb-1.0-0-dev \
    # Keyboard (RFID Reader) access
    kbd \
    # Wand for adding PS:1 logo to labels
    imagemagick \
    # Process management
    supervisor

# Remove unneccessary stuff
RUN rm -rf /var/lib/apt/lists/*

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Track working directory
ENV APP_ROOT="/app"
ENV WEB_PORT=5000

# Expose the webserver port
EXPOSE ${WEB_PORT}

# Set the working directory in the container
WORKDIR ${APP_ROOT}

# Copy requirement files and create expected directory structure
# Do this before copying contents for efficient layer caching
COPY pyproject.toml ${APP_ROOT}/
COPY uv.lock ${APP_ROOT}/

# Install Python dependencies
RUN uv sync --no-dev

# Copy the source code into the container
COPY src/ ${APP_ROOT}/src/

# Start supervisord to run both processes
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
