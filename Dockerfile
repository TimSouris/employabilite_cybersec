FROM python:3.11-slim

# Install system dependencies for Selenium (Chromium + Firefox + geckodriver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    firefox-esr \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install pinned geckodriver version for Firefox
ARG GECKODRIVER_VERSION=0.34.0
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz" -O /tmp/geckodriver.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ \
    && rm /tmp/geckodriver.tar.gz

WORKDIR /app

# Install Python dependencies before copying source for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Main.py"]
