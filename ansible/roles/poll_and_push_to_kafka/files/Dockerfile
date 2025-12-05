FROM python:3.12-slim

# Install OS deps (if needed for kafka-python SSL etc; we keep it minimal)
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Copy app and requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# State directory for timestamp file
VOLUME ["/state"]

# Environment defaults (can override at runtime)
ENV POLL_INTERVAL_SECONDS=300
ENV STATE_DIR=/state
ENV WAHA_API_KEY=e9b7e8a660214e398fab708e8f0929ae
ENV CHAT_ID=31615886012-1633085152@g.us
ENV KAFKA_BOOTSTRAP_SERVERS=localhost:9092
ENV KAFKA_TOPIC=whatsapp-messages

CMD ["python", "app.py"]

