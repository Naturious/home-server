# Whatsapp message event format

example message:

```
{
  "id": "wamid.HBgLMzYxNzAwMTIzNDU1FQIAEhggODY4QzEwNkFEQTFCNTk2QkMwQ0I4QzNFNjA2RjM0RgA=",
  "timestamp": "2025-11-24T22:30:12Z",
  "sender": {
    "phone": "+31612345678",
    "name": "Adam",
    "is_me": true
  },
  "chat": {
    "id": "1234567890-987654321@g.us",
    "type": "group",
    "name": "Family Chat",
    "participants": ["+31612345678", "+49123456789", "+33798765432"]
  },
  "content": {
    "type": "text",
    "text": "Just arrived home!"
  },
  "reply_to": null,
  "metadata": {
    "received_at": "2025-11-24T22:30:13Z",
    "ingestion_id": "whatsapp-ingest-93f715"
  }
}

```
