from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from ata.events import DuplicateEventError, EventEnvelope, EventOrderError, EventStore


def dt(hour: int) -> datetime:
    return datetime(2026, 6, 9, hour, tzinfo=UTC)


def event(
    event_id: str,
    *,
    stream_id: str = "ice:hh",
    stream_sequence: int = 1,
    valid_time: datetime | None = None,
    knowledge_time: datetime | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        stream_id=stream_id,
        stream_sequence=stream_sequence,
        event_type="QuoteEvent",
        source_system="ice_python",
        data_scope="local_live",
        valid_time=valid_time or dt(9),
        source_time=dt(9),
        capture_time=dt(10),
        ingest_time=dt(10),
        knowledge_time=knowledge_time or dt(10),
        normalization_version="ice-normalizer-v1",
        calendar_version="cal-v1",
        raw_payload_hash="raw-hash",
        raw_payload_uri=None,
        payload_schema="quote.v1",
        payload={"price": Decimal("2.750"), "symbol": "HHM26"},
    )


def test_envelope_serializes_datetimes_and_decimals_deterministically() -> None:
    envelope = event("evt-1")

    data = envelope.to_json_dict()

    assert data["source_system"] == "ice_python"
    assert data["data_scope"] == "local_live"
    assert data["valid_time"] == "2026-06-09T09:00:00Z"
    assert data["payload"] == {"price": "2.750", "symbol": "HHM26"}
    round_tripped = EventEnvelope.from_json_line(envelope.to_json_line())
    assert envelope.to_json_line() == round_tripped.to_json_line()


def test_event_store_enforces_append_only_ids_and_stream_order() -> None:
    store = EventStore()
    store.append(event("evt-1", stream_sequence=1))

    with pytest.raises(DuplicateEventError):
        store.append(event("evt-1", stream_sequence=2))

    with pytest.raises(EventOrderError):
        store.append(event("evt-2", stream_sequence=1))

    store.append(event("evt-other", stream_id="pjm:load", stream_sequence=1))
    assert [item.event_id for item in store.iter_stream("pjm:load")] == ["evt-other"]


def test_bitemporal_query_filters_by_valid_time_and_known_at() -> None:
    store = EventStore(
        [
            event("known-valid", stream_sequence=1, valid_time=dt(8), knowledge_time=dt(9)),
            event("future-valid", stream_sequence=2, valid_time=dt(12), knowledge_time=dt(9)),
            event("late-known", stream_sequence=3, valid_time=dt(8), knowledge_time=dt(11)),
        ]
    )

    result = store.query(as_of=dt(10), known_at=dt(10))

    assert [item.event_id for item in result] == ["known-valid"]


def test_snapshot_id_is_deterministic_for_same_event_set() -> None:
    first = event("evt-1", stream_sequence=1)
    second = event("evt-2", stream_sequence=2)
    store = EventStore([first, second])

    snapshot_a = store.snapshot_id(model_version="m1", calculation_version="c1")
    snapshot_b = store.snapshot_id([second, first], model_version="m1", calculation_version="c1")
    snapshot_c = store.snapshot_id([first], model_version="m1", calculation_version="c1")

    assert snapshot_a == snapshot_b
    assert snapshot_a != snapshot_c


def test_jsonl_export_import_round_trips(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    store = EventStore([event("evt-1", stream_sequence=1), event("evt-2", stream_sequence=2)])

    store.export_jsonl(path)
    imported = EventStore.import_jsonl(path)

    assert [item.to_json_dict() for item in imported] == [item.to_json_dict() for item in store]
    assert imported.snapshot_id() == store.snapshot_id()
