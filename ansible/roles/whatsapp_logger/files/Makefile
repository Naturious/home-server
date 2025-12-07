# Makefile

# Default values for local development (can be overridden from CLI)
KAFKA_BOOTSTRAP_SERVERS ?= 192.168.1.9:9092
KAFKA_TOPIC ?= whatsapp-messages
# WAHA_BASE_URL ?= http://192.168.1.9:3000
# WAHA_API_KEY ?= e9b7e8a660214e398fab708e8f0929ae

# Export all of them to subprocesses (like python)
export KAFKA_BOOTSTRAP_SERVERS
export KAFKA_TOPIC
# export WAHA_BASE_URL
# export WAHA_API_KEY

.PHONY: run-dev
run-dev:
	python3 consumer.py
