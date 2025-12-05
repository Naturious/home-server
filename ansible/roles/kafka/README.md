# Test Kafka

✅ Working consumer
```
docker run --rm -it --network kafka-net \
  confluentinc/cp-kafka:7.6.0 \
  kafka-console-consumer \
    --bootstrap-server kafka:29092 \
    --topic test-topic \
    --from-beginning
```

✅ Working producer
```
docker run --rm -it --network kafka-net \
  confluentinc/cp-kafka:7.6.0 \
  kafka-console-producer \
    --bootstrap-server kafka:29092 \
    --topic test-topic
```

✅ Working topic creation
```
docker run --rm -it --network kafka-net \
  confluentinc/cp-kafka:7.6.0 \
  kafka-topics \
    --create \
    --topic test-topic \
    --bootstrap-server kafka:29092 \
    --partitions 1 \
    --replication-factor 1
```
