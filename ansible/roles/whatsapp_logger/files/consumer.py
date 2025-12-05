import os
import time
from kafka import KafkaConsumer

topic = os.getenv("KAFKA_TOPIC", "whatsapp-messages")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
group_id = os.getenv("KAFKA_GROUP_ID", "whatsapp-logger")

def process_message(msg):
    print(f"[WHATSAPP] partition={msg.partition} offset={msg.offset} value={msg.value}")

def main():
    print(f"Starting WhatsApp logger. Topic={topic}, bootstrap_servers={bootstrap_servers}")
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers.split(","),
                group_id=group_id,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: v.decode("utf-8"),
            )

            for msg in consumer:
                process_message(msg)
        except Exception as e:
            print(f"Error in consumer loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

