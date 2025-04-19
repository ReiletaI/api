# Base image with CUDA + Ubuntu (no Python yet)
FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04

# Set timezone
ENV TZ=America/Toronto
RUN apt-get update && apt-get install -y \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python and system dependencies
# Install Python & system deps
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    libsox-fmt-mp3 \
    && rm -rf /var/lib/apt/lists/*

# Create venv & install Python deps
WORKDIR /app
COPY requirements.txt ./
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

# Copy app source code
COPY . .

# Make sure data folder exists
RUN mkdir -p /app/data


# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
