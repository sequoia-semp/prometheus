"""Event envelope DTOs and deterministic serialization helpers."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, TypeAlias, cast

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
PayloadValue: TypeAlias = JsonValue | Decimal | list["PayloadValue"] | dict[str, "PayloadValue"]


def utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("datetime values must be timezone-aware")
    return value.astimezone(UTC)


def _to_rfc3339(value: datetime) -> str:
    return utc_datetime(value).isoformat().replace("+00:00", "Z")


def _from_rfc3339(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return utc_datetime(parsed)


def _payload_to_json(value: PayloadValue) -> JsonValue:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, list):
        return [_payload_to_json(item) for item in value]
    if isinstance(value, dict):
        return {key: _payload_to_json(item) for key, item in value.items()}
    return value


def _optional_datetime_to_json(value: datetime | None) -> str | None:
    if value is None:
        return None
    return _to_rfc3339(value)


def _optional_datetime_from_json(value: JsonValue) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("datetime fields must be strings or null")
    return _from_rfc3339(value)


def _required_str(data: dict[str, JsonValue], key: str) -> str:
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    return value


def _required_int(data: dict[str, JsonValue], key: str) -> int:
    value = data[key]
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer")
    return value


def _optional_str(data: dict[str, JsonValue], key: str) -> str | None:
    value = data[key]
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string or null")
    return value


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Contract-compatible append-only event envelope."""

    event_id: str
    stream_id: str
    stream_sequence: int
    event_type: str
    source_system: str
    data_scope: str
    valid_time: datetime | None
    source_time: datetime | None
    capture_time: datetime
    ingest_time: datetime
    knowledge_time: datetime
    normalization_version: str
    calendar_version: str | None
    raw_payload_hash: str | None
    raw_payload_uri: str | None
    payload_schema: str
    payload: dict[str, PayloadValue]

    def __post_init__(self) -> None:
        if self.stream_sequence < 1:
            raise ValueError("stream_sequence must be >= 1")
        for field_name in ["event_id", "stream_id", "event_type", "source_system", "data_scope"]:
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} is required")
        if not self.normalization_version:
            raise ValueError("normalization_version is required")
        if not self.payload_schema:
            raise ValueError("payload_schema is required")
        for value in [
            self.valid_time,
            self.source_time,
            self.capture_time,
            self.ingest_time,
            self.knowledge_time,
        ]:
            if value is not None:
                utc_datetime(value)

    def to_json_dict(self) -> dict[str, JsonValue]:
        """Return a deterministic JSON-compatible dictionary."""
        return {
            "event_id": self.event_id,
            "stream_id": self.stream_id,
            "stream_sequence": self.stream_sequence,
            "event_type": self.event_type,
            "source_system": self.source_system,
            "data_scope": self.data_scope,
            "valid_time": _optional_datetime_to_json(self.valid_time),
            "source_time": _optional_datetime_to_json(self.source_time),
            "capture_time": _to_rfc3339(self.capture_time),
            "ingest_time": _to_rfc3339(self.ingest_time),
            "knowledge_time": _to_rfc3339(self.knowledge_time),
            "normalization_version": self.normalization_version,
            "calendar_version": self.calendar_version,
            "raw_payload_hash": self.raw_payload_hash,
            "raw_payload_uri": self.raw_payload_uri,
            "payload_schema": self.payload_schema,
            "payload": _payload_to_json(self.payload),
        }

    def to_json_line(self) -> str:
        """Serialize the envelope as canonical JSONL text."""
        return json.dumps(self.to_json_dict(), sort_keys=True, separators=(",", ":"))

    def content_hash(self) -> str:
        """Hash the canonical serialized envelope."""
        return hashlib.sha256(self.to_json_line().encode("utf-8")).hexdigest()

    @classmethod
    def from_json_dict(cls, data: dict[str, JsonValue]) -> EventEnvelope:
        payload = data["payload"]
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        return cls(
            event_id=_required_str(data, "event_id"),
            stream_id=_required_str(data, "stream_id"),
            stream_sequence=_required_int(data, "stream_sequence"),
            event_type=_required_str(data, "event_type"),
            source_system=_required_str(data, "source_system"),
            data_scope=_required_str(data, "data_scope"),
            valid_time=_optional_datetime_from_json(data["valid_time"]),
            source_time=_optional_datetime_from_json(data["source_time"]),
            capture_time=_from_rfc3339(_required_str(data, "capture_time")),
            ingest_time=_from_rfc3339(_required_str(data, "ingest_time")),
            knowledge_time=_from_rfc3339(_required_str(data, "knowledge_time")),
            normalization_version=_required_str(data, "normalization_version"),
            calendar_version=_optional_str(data, "calendar_version"),
            raw_payload_hash=_optional_str(data, "raw_payload_hash"),
            raw_payload_uri=_optional_str(data, "raw_payload_uri"),
            payload_schema=_required_str(data, "payload_schema"),
            payload=cast(dict[str, PayloadValue], payload),
        )

    @classmethod
    def from_json_line(cls, line: str) -> EventEnvelope:
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError("event JSON line must contain an object")
        return cls.from_json_dict(cast(dict[str, Any], data))

    def write_json(self, path: Path) -> None:
        path.write_text(self.to_json_line() + "\n", encoding="utf-8")
