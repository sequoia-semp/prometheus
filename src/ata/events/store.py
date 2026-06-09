"""Append-only local bitemporal event store."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Iterator
from datetime import datetime
from pathlib import Path

from ata.events.model import EventEnvelope, JsonValue, utc_datetime


class DuplicateEventError(ValueError):
    """Raised when an event ID is appended more than once."""


class EventOrderError(ValueError):
    """Raised when per-stream sequence ordering is not monotonic."""


class EventStore:
    """In-memory append-only store with deterministic JSONL import/export."""

    def __init__(self, events: Iterable[EventEnvelope] = ()) -> None:
        self._events: list[EventEnvelope] = []
        self._event_ids: set[str] = set()
        self._last_sequence_by_stream: dict[str, int] = {}
        for event in events:
            self.append(event)

    def append(self, event: EventEnvelope) -> None:
        """Append one event, enforcing uniqueness and per-stream monotonicity."""
        if event.event_id in self._event_ids:
            raise DuplicateEventError(f"duplicate event_id: {event.event_id}")

        last_sequence = self._last_sequence_by_stream.get(event.stream_id)
        if last_sequence is not None and event.stream_sequence <= last_sequence:
            raise EventOrderError(
                f"stream_sequence for {event.stream_id} must be greater than {last_sequence}"
            )

        self._events.append(event)
        self._event_ids.add(event.event_id)
        self._last_sequence_by_stream[event.stream_id] = event.stream_sequence

    def extend(self, events: Iterable[EventEnvelope]) -> None:
        for event in events:
            self.append(event)

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self) -> Iterator[EventEnvelope]:
        return iter(self._events)

    def iter_stream(self, stream_id: str) -> Iterator[EventEnvelope]:
        return (event for event in self._events if event.stream_id == stream_id)

    def query(self, *, as_of: datetime, known_at: datetime) -> list[EventEnvelope]:
        """Return events valid as of `as_of` and known by `known_at`."""
        as_of_utc = utc_datetime(as_of)
        known_at_utc = utc_datetime(known_at)
        return [
            event
            for event in self._events
            if (event.valid_time is None or utc_datetime(event.valid_time) <= as_of_utc)
            and utc_datetime(event.knowledge_time) <= known_at_utc
        ]

    def snapshot_id(
        self,
        events: Iterable[EventEnvelope] | None = None,
        *,
        model_version: str | None = None,
        calculation_version: str | None = None,
    ) -> str:
        """Compute a deterministic snapshot ID for an event set and lineage."""
        selected_events = list(self._events if events is None else events)
        event_parts: list[dict[str, JsonValue]] = [
            {
                "event_hash": event.content_hash(),
                "event_id": event.event_id,
                "stream_id": event.stream_id,
                "stream_sequence": event.stream_sequence,
                "normalization_version": event.normalization_version,
                "calendar_version": event.calendar_version,
            }
            for event in sorted(
                selected_events,
                key=lambda event: (event.stream_id, event.stream_sequence, event.event_id),
            )
        ]
        payload = json.dumps(
            {
                "events": event_parts,
                "model_version": model_version,
                "calculation_version": calculation_version,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return "snap_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def export_jsonl(self, path: Path, events: Iterable[EventEnvelope] | None = None) -> None:
        selected_events = self._events if events is None else list(events)
        with path.open("w", encoding="utf-8", newline="\n") as output:
            for event in selected_events:
                output.write(event.to_json_line())
                output.write("\n")

    @classmethod
    def import_jsonl(cls, path: Path) -> EventStore:
        store = cls()
        with path.open("r", encoding="utf-8") as input_file:
            for line_number, line in enumerate(input_file, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    store.append(EventEnvelope.from_json_line(stripped))
                except ValueError as exc:
                    raise ValueError(f"invalid event JSONL at line {line_number}: {exc}") from exc
        return store
