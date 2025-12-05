# test_process_message.py

import json
import textwrap

import pytest

from consumer import process_message


class DummyMsg:
    """Minimal stand-in for kafka.consumer.fetcher.ConsumerRecord."""
    def __init__(self, partition: int, offset: int, value: str):
        self.partition = partition
        self.offset = offset
        self.value = value


def _build_sample_message_json() -> str:
    """
    Build a JSON string that mimics the WhatsApp message payload
    you showed in the example.
    """
    msg = {
        "id": "false_31615886012-1633085152@g.us_3AC36C312EC0607FEC6C_191465464549445@lid",
        "timestamp": 1764939046,
        "from": "31615886012-1633085152@g.us",
        "fromMe": False,
        "participant": "191465464549445@lid",
        "source": "app",
        "to": "31685039540@c.us",
        "body": "Today we start at 19:00, all styles welcome 🙏🙏",
        "hasMedia": True,
        "media": {
            "url": "http://localhost:3000/api/files/default/false_31615886012-1633085152@g.us_3AC36C312EC0607FEC6C_191465464549445@lid.jpeg",
            "filename": None,
            "mimetype": "image/jpeg",
        },
        "ack": 1,
        "ackName": "SERVER",
        # we don’t need the full gigantic _data field here for this test;
        # the important part is that the JSON structure is valid and
        # contains the "body" text we care about.
        "_data": {
            "type": "image",
            "caption": "Today we start at 19:00, all styles welcome 🙏🙏",
        },
    }
    return json.dumps(msg, ensure_ascii=False)


def test_process_message_prints_partition_offset_and_value(capsys: pytest.CaptureFixture) -> None:
    # Arrange
    value = _build_sample_message_json()
    msg = DummyMsg(partition=0, offset=42, value=value)

    # Act
    process_message(msg)
    captured = capsys.readouterr().out.strip()

    # Assert basic structure
    assert captured.startswith("[WHATSAPP] "), "Output should start with [WHATSAPP] prefix"
    assert "partition=0" in captured
    assert "offset=42" in captured

    # And we expect the JSON payload to be present in the printed value
    assert '"body": "Today we start at 19:00, all styles welcome 🙏🙏"' in captured


@pytest.mark.skip(reason="Example of a future test once event extraction is implemented")
def test_process_message_triggers_event_detection(monkeypatch, capsys):
    """
    Example skeleton for when you add OpenAI-based event extraction.

    Imagine process_message() calls some helper like `extract_event_info(text)`
    and then prints/returns it. This shows how you'd test that behavior
    *without* actually calling the OpenAI API.
    """

    # Fake event detection function
    detected_event = {
        "has_event": True,
        "event_type": "cultural",
        "category": "dance / music",
        "start_time": "19:00",
        "description": "Today we start at 19:00, all styles welcome 🙏🙏",
    }

    # Suppose in consumer.py you eventually have:
    #   from consumer import extract_event_info
    # We monkeypatch that here.
    import consumer

    def fake_extract_event_info(text: str):
        assert "Today we start at 19:00" in text
        return detected_event

    monkeypatch.setattr(consumer, "extract_event_info", fake_extract_event_info)

    value = _build_sample_message_json()
    msg = DummyMsg(partition=1, offset=99, value=value)

    # Act
    consumer.process_message(msg)
    captured = capsys.readouterr().out

    # Assert that some representation of the detected event ended up in logs/output.
    # (Adjust this to whatever you actually decide process_message should do.)
    assert "has_event" in captured
    assert "dance" in captured or "music" in captured

