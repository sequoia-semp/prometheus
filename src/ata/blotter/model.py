"""Append-only trade blotter and deterministic position projection."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal, TypeAlias, cast

from ata.events import EventEnvelope

TradeKind: TypeAlias = Literal["new", "amend", "bust"]


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime values must be timezone-aware")
    return value.astimezone(UTC)


def _to_rfc3339(value: datetime) -> str:
    return _utc_datetime(value).isoformat().replace("+00:00", "Z")


def _from_rfc3339(value: str) -> datetime:
    return _utc_datetime(datetime.fromisoformat(value.replace("Z", "+00:00")))


def _required_str(data: dict[str, object], key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _optional_str(data: dict[str, object], key: str) -> str | None:
    value = data[key]
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string or null")
    return value


def _required_int(data: dict[str, object], key: str) -> int:
    value = data[key]
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _required_decimal(data: dict[str, object], key: str) -> Decimal:
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a decimal string")
    return Decimal(value)


def _required_datetime(data: dict[str, object], key: str) -> datetime:
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} must be an RFC3339 datetime string")
    return _from_rfc3339(value)


def _required_str_list(data: dict[str, object], key: str) -> list[str]:
    value = data[key]
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list of strings")
    items = cast(list[object], value)
    if not all(isinstance(item, str) for item in items):
        raise ValueError(f"{key} must be a list of strings")
    return [cast(str, item) for item in items]


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class TradeEvent:
    """Append-only trade event."""

    event_id: str
    stream_id: str
    stream_sequence: int
    instrument_id: str
    quantity: Decimal
    price: Decimal
    trade_time: datetime
    known_at: datetime
    kind: TradeKind
    amends_event_id: str | None
    source_event_ids: list[str]

    def __post_init__(self) -> None:
        for field_name in ["event_id", "stream_id", "instrument_id"]:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")
        if self.stream_sequence < 1:
            raise ValueError("stream_sequence must be >= 1")
        _utc_datetime(self.trade_time)
        _utc_datetime(self.known_at)
        if self.kind == "new" and self.amends_event_id is not None:
            raise ValueError("new trades cannot reference amends_event_id")
        if self.kind in {"amend", "bust"} and not self.amends_event_id:
            raise ValueError(f"{self.kind} trades require amends_event_id")

    def to_json_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "stream_id": self.stream_id,
            "stream_sequence": self.stream_sequence,
            "instrument_id": self.instrument_id,
            "quantity": str(self.quantity),
            "price": str(self.price),
            "trade_time": _to_rfc3339(self.trade_time),
            "known_at": _to_rfc3339(self.known_at),
            "kind": self.kind,
            "amends_event_id": self.amends_event_id,
            "source_event_ids": self.source_event_ids,
        }

    def to_json_line(self) -> str:
        return _canonical_json(self.to_json_dict())

    @classmethod
    def from_json_dict(cls, data: dict[str, object]) -> TradeEvent:
        return cls(
            event_id=_required_str(data, "event_id"),
            stream_id=_required_str(data, "stream_id"),
            stream_sequence=_required_int(data, "stream_sequence"),
            instrument_id=_required_str(data, "instrument_id"),
            quantity=_required_decimal(data, "quantity"),
            price=_required_decimal(data, "price"),
            trade_time=_required_datetime(data, "trade_time"),
            known_at=_required_datetime(data, "known_at"),
            kind=cast(TradeKind, _required_str(data, "kind")),
            amends_event_id=_optional_str(data, "amends_event_id"),
            source_event_ids=_required_str_list(data, "source_event_ids"),
        )

    @classmethod
    def from_json_line(cls, line: str) -> TradeEvent:
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError("trade event JSON must contain an object")
        return cls.from_json_dict(cast(dict[str, Any], data))

    @classmethod
    def from_event_envelope(cls, envelope: EventEnvelope) -> TradeEvent:
        if envelope.payload_schema != "trade_event.v1":
            raise ValueError(f"unsupported trade payload_schema: {envelope.payload_schema}")
        return cls.from_json_dict(cast(dict[str, object], envelope.payload))


@dataclass(frozen=True, slots=True)
class Position:
    """Projected position for one instrument."""

    instrument_id: str
    quantity: Decimal
    book_version: str
    as_of: datetime
    known_at: datetime
    source_event_ids: list[str]


class TradeBlotter:
    """Append-only trade blotter with deterministic position projection."""

    def __init__(self, events: list[TradeEvent] | None = None) -> None:
        self._events: list[TradeEvent] = []
        self._event_ids: set[str] = set()
        self._last_sequence_by_stream: dict[str, int] = {}
        for event in events or []:
            self.append(event)

    def append(self, event: TradeEvent) -> None:
        if event.event_id in self._event_ids:
            raise ValueError(f"duplicate trade event_id: {event.event_id}")
        last_sequence = self._last_sequence_by_stream.get(event.stream_id)
        if last_sequence is not None and event.stream_sequence <= last_sequence:
            raise ValueError(
                f"stream_sequence for {event.stream_id} must be greater than {last_sequence}"
            )
        self._events.append(event)
        self._event_ids.add(event.event_id)
        self._last_sequence_by_stream[event.stream_id] = event.stream_sequence

    def __iter__(self) -> Iterator[TradeEvent]:
        return iter(self._events)

    def __len__(self) -> int:
        return len(self._events)

    @classmethod
    def from_event_envelopes(cls, envelopes: list[EventEnvelope]) -> TradeBlotter:
        return cls([TradeEvent.from_event_envelope(envelope) for envelope in envelopes])

    def position_as_of(self, *, as_of: datetime, known_at: datetime) -> list[Position]:
        as_of_utc = _utc_datetime(as_of)
        known_at_utc = _utc_datetime(known_at)
        visible = [
            event
            for event in self._events
            if _utc_datetime(event.trade_time) <= as_of_utc
            and _utc_datetime(event.known_at) <= known_at_utc
        ]
        visible.sort(
            key=lambda event: (
                event.known_at,
                event.stream_id,
                event.stream_sequence,
                event.event_id,
            )
        )

        active_events: dict[str, TradeEvent] = {}
        for event in visible:
            if event.kind == "new":
                active_events[event.event_id] = event
            elif event.kind == "amend":
                if event.amends_event_id in active_events:
                    del active_events[event.amends_event_id]
                active_events[event.event_id] = event
            elif event.kind == "bust":
                if event.amends_event_id in active_events:
                    del active_events[event.amends_event_id]

        quantities: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        source_event_ids: defaultdict[str, list[str]] = defaultdict(list)
        for event in sorted(active_events.values(), key=lambda item: item.event_id):
            quantities[event.instrument_id] += event.quantity
            source_event_ids[event.instrument_id].append(event.event_id)

        applied_event_ids = [event.event_id for event in visible]
        book_version = self.book_version(applied_event_ids)
        return [
            Position(
                instrument_id=instrument_id,
                quantity=quantity,
                book_version=book_version,
                as_of=as_of_utc,
                known_at=known_at_utc,
                source_event_ids=source_event_ids[instrument_id],
            )
            for instrument_id, quantity in sorted(quantities.items())
            if quantity != 0
        ]

    @staticmethod
    def book_version(event_ids: list[str]) -> str:
        payload = json.dumps(sorted(event_ids), separators=(",", ":"))
        return "book_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
