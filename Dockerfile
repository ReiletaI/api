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
    ffmpeg \
    libsox-fmt-mp3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Make sure data folder exists
RUN mkdir -p /app/data
VOLUME ["/app/data"]

# Exposer le port sur lequel FastAPI écoute
EXPOSE 8123

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8123"]