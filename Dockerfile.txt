FROM python:3.11-slim

# Install system dependencies (ffmpeg required for song download & voice)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create hosted directory
RUN mkdir -p hosted

CMD ["python", "xy.py"]
