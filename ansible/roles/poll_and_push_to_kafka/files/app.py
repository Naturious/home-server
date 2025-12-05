#!/usr/bin/env python3
import os
import time
import json
from pathlib import Path

import requests
from kafka import KafkaProducer

# -----------------------------
# Configuration (env vars)
# -----------------------------
SERVER_IP = os.getenv("SERVER_IP", "192.168.1.9")
WAHA_API_KEY = os.getenv("WAHA_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "whatsapp-messages")

# Interval between polls (seconds)
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))  # 5 minutes

STATE_DIR = Path(os.getenv("STATE_DIR", "./state"))
STATE_DIR.mkdir(parents=True, exist_ok=True)
TIMESTAMP_FILE = STATE_DIR / "last_timestamp.txt"

BASE_URL = f"http://{SERVER_IP}:3000/api/default/chats/{CHAT_ID}/messages"


def load_last_timestamp():
    if TIMESTAMP_FILE.exists():
        try:
            return int(TIMESTAMP_FILE.read_text().strip())
        except ValueError:
            return 0
    return 0


def save_last_timestamp(timestamp: int):
    TIMESTAMP_FILE.write_text(str(timestamp))


def fetch_messages(since_ts: int):
    params = {
        "limit": 50,
        "filter.timestamp.gte": since_ts,
    }

    headers = {
        "X-Api-Key": WAHA_API_KEY,
        "Content-Type": "application/json",
    }

    resp = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda v: v.encode("utf-8") if v is not None else None,
        linger_ms=10,
        retries=5,
    )


def main_loop():
    if not WAHA_API_KEY:
        raise RuntimeError("WAHA_API_KEY is not set")
    if not CHAT_ID:
        raise RuntimeError("CHAT_ID is not set")

    producer = create_kafka_producer()

    while True:
        try:
            last_ts = load_last_timestamp()
            print(f"[poller] Fetching messages since: {last_ts}")

            messages = fetch_messages(last_ts)

            if not messages:
                print("[poller] No new messages.")
            else:
                # Sort by timestamp just in case
                messages = sorted(messages, key=lambda m: m.get("timestamp", 0))

                for msg in messages:
                    # You can shape the payload here if you want a specific schema
                    payload = {
                        "id": msg.get("id"),
                        "timestamp": msg.get("timestamp"),
                        "chat_id": msg.get("from") or CHAT_ID,
                        "from": msg.get("from"),
                        "fromMe": msg.get("fromMe"),
                        "participant": msg.get("participant"),
                        "body": msg.get("body"),
                        "source": msg.get("source"),
                        "raw": msg,  # keep full original for now
                    }

                    key = msg.get("id") or None
                    producer.send(KAFKA_TOPIC, key=key, value=payload)

                producer.flush()

                latest_ts = messages[-1].get("timestamp", last_ts)
                save_last_timestamp(latest_ts+1)
                print(f"[poller] Sent {len(messages)} message(s) to Kafka. New last_ts={latest_ts}")

        except Exception as e:
            # Rudimentary logging; you can swap for proper logging if you like
            print(f"[poller] ERROR: {e}")

        print(f"[poller] Sleeping for {POLL_INTERVAL_SECONDS} seconds...")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main_loop()

