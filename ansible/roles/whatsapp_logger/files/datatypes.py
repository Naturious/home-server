from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Jid:
    server: str
    user: str
    serialized: str


@dataclass
class MessageId:
    fromMe: bool
    remote: str
    id: str
    participant: Optional[Jid]
    serialized: str


@dataclass
class Link:
    link: str
    isSuspicious: bool


@dataclass
class InternalData:
    type: str
    caption: Optional[str]


@dataclass
class WhatsAppMessage:
    id: str
    timestamp: int
    from_: str
    fromMe: bool
    source: str
    to: str
    body: str
    hasMedia: bool
    media: Optional[Any]
    ack: int
    ackName: str
    vCards: List[Any]
    _data: InternalData

