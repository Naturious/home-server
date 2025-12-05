FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir kafka-python

COPY consumer.py /app/consumer.py

CMD ["python", "/app/consumer.py"]

