from datatypes import *

def parse_jid(obj: Optional[dict]) -> Optional[Jid]:
    if not obj:
        return None
    return Jid(
        server=obj.get("server"),
        user=obj.get("user"),
        serialized=obj.get("_serialized"),
    )


def parse_message_id(obj: dict) -> MessageId:
    return MessageId(
        fromMe=obj.get("fromMe"),
        remote=obj.get("remote"),
        id=obj.get("id"),
        participant=parse_jid(obj.get("participant")),
        serialized=obj.get("_serialized"),
    )


def parse_links(arr: list) -> List[Link]:
    return [Link(link=lk["link"], isSuspicious=lk["isSuspicious"]) for lk in arr or []]


def parse_internal_data(obj: dict) -> InternalData:
    return InternalData(
        type=obj.get("type"),
        caption=obj.get("caption"),
    )


def parse_message(raw: dict) -> WhatsAppMessage:
    return WhatsAppMessage(
        id=raw["id"],
        timestamp=raw["timestamp"],
        from_=raw["from"],
        fromMe=raw["fromMe"],
        source=raw.get("source"),
        to=raw["to"],
        body=raw.get("body", ""),
        hasMedia=raw["hasMedia"],
        media=raw.get("media"),
        ack=raw.get("ack"),
        ackName=raw.get("ackName"),
        vCards=raw.get("vCards", []),
        _data=parse_internal_data(raw.get("_data", {}))
    )

