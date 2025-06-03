FROM python:3.11-slim

# Install dependencies and Tectonic
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    xz-utils \
    libgraphite2-3 \
    libharfbuzz0b \
    libicu72 \
    libssl3 \
    libfontconfig1 \
    libfreetype6 && \
    curl -L -o tectonic.tar.gz https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz && \
    tar -xzf tectonic.tar.gz && \
    mv tectonic /usr/local/bin/tectonic && \
    chmod +x /usr/local/bin/tectonic && \
    rm tectonic.tar.gz && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY utls.py .

# Optional: healthcheck to verify tectonic is installed properly
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD tectonic --version || exit 1

# Expose port for FastAPI/Uvicorn
EXPOSE 8000

# Run your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
