from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

import pytest

from ata.blotter import TradeBlotter, TradeEvent
from ata.blotter.model import TradeKind
from ata.events import EventEnvelope, EventStore
from ata.events.model import PayloadValue


def dt(hour: int) -> datetime:
    return datetime(2026, 6, 9, hour, tzinfo=UTC)


def trade(
    event_id: str,
    *,
    stream_sequence: int,
    quantity: Decimal = Decimal("10"),
    known_at: datetime | None = None,
    trade_time: datetime | None = None,
    kind: TradeKind = "new",
    amends_event_id: str | None = None,
) -> TradeEvent:
    return TradeEvent(
        event_id=event_id,
        stream_id="book:gas",
        stream_sequence=stream_sequence,
        instrument_id="inst:hh",
        quantity=quantity,
        price=Decimal("2.750"),
        trade_time=trade_time or dt(9),
        known_at=known_at or dt(10),
        kind=kind,
        amends_event_id=amends_event_id,
        source_event_ids=[f"source:{event_id}"],
    )


def envelope_for(trade_event: TradeEvent) -> EventEnvelope:
    return EventEnvelope(
        event_id=f"env:{trade_event.event_id}",
        stream_id="manual_blotter:book",
        stream_sequence=trade_event.stream_sequence,
        event_type="TradeEvent",
        source_system="manual_blotter",
        data_scope="derived",
        valid_time=trade_event.trade_time,
        source_time=trade_event.trade_time,
        capture_time=trade_event.known_at,
        ingest_time=trade_event.known_at,
        knowledge_time=trade_event.known_at,
        normalization_version="trade-event-v1",
        calendar_version=None,
        raw_payload_hash=None,
        raw_payload_uri=None,
        payload_schema="trade_event.v1",
        payload=cast(dict[str, PayloadValue], trade_event.to_json_dict()),
    )


def test_trade_events_round_trip_deterministically() -> None:
    event = trade("t1", stream_sequence=1)

    round_tripped = TradeEvent.from_json_line(event.to_json_line())

    assert round_tripped.to_json_line() == event.to_json_line()
    assert round_tripped.quantity == Decimal("10")
    assert round_tripped.known_at == dt(10)


def test_blotter_enforces_append_only_uniqueness_and_stream_order() -> None:
    blotter = TradeBlotter([trade("t1", stream_sequence=1)])

    with pytest.raises(ValueError, match="duplicate"):
        blotter.append(trade("t1", stream_sequence=2))

    with pytest.raises(ValueError, match="stream_sequence"):
        blotter.append(trade("t2", stream_sequence=1))


def test_position_as_of_filters_trade_time_and_known_at() -> None:
    blotter = TradeBlotter(
        [
            trade(
                "known",
                stream_sequence=1,
                quantity=Decimal("10"),
                trade_time=dt(8),
                known_at=dt(9),
            ),
            trade(
                "future",
                stream_sequence=2,
                quantity=Decimal("5"),
                trade_time=dt(12),
                known_at=dt(9),
            ),
            trade(
                "late",
                stream_sequence=3,
                quantity=Decimal("3"),
                trade_time=dt(8),
                known_at=dt(11),
            ),
        ]
    )

    positions = blotter.position_as_of(as_of=dt(10), known_at=dt(10))

    assert len(positions) == 1
    assert positions[0].quantity == Decimal("10")
    assert positions[0].source_event_ids == ["known"]


def test_amend_and_bust_are_new_events_that_change_visible_fold() -> None:
    blotter = TradeBlotter(
        [
            trade("t1", stream_sequence=1, quantity=Decimal("10")),
            trade(
                "amend-t1",
                stream_sequence=2,
                quantity=Decimal("15"),
                kind="amend",
                amends_event_id="t1",
            ),
            trade(
                "bust-amend",
                stream_sequence=3,
                quantity=Decimal("0"),
                known_at=dt(11),
                kind="bust",
                amends_event_id="amend-t1",
            ),
        ]
    )

    amended = blotter.position_as_of(as_of=dt(10), known_at=dt(10))
    busted = blotter.position_as_of(as_of=dt(10), known_at=dt(11))

    assert amended[0].quantity == Decimal("15")
    assert busted == []
    assert len(blotter) == 3


def test_amend_is_only_applied_when_known() -> None:
    blotter = TradeBlotter(
        [
            trade("t1", stream_sequence=1, quantity=Decimal("10"), known_at=dt(9)),
            trade(
                "amend-t1",
                stream_sequence=2,
                quantity=Decimal("15"),
                known_at=dt(11),
                kind="amend",
                amends_event_id="t1",
            ),
        ]
    )

    original = blotter.position_as_of(as_of=dt(10), known_at=dt(10))
    amended = blotter.position_as_of(as_of=dt(10), known_at=dt(11))

    assert original[0].quantity == Decimal("10")
    assert original[0].source_event_ids == ["t1"]
    assert amended[0].quantity == Decimal("15")
    assert amended[0].source_event_ids == ["amend-t1"]


def test_book_version_is_deterministic_from_applied_event_ids() -> None:
    first = TradeBlotter.book_version(["b", "a"])
    second = TradeBlotter.book_version(["a", "b"])

    assert first == second
    assert first != TradeBlotter.book_version(["a"])


def test_positions_reproduce_from_event_store_replay() -> None:
    source_events = [trade("t1", stream_sequence=1), trade("t2", stream_sequence=2)]
    event_store = EventStore([envelope_for(event) for event in source_events])

    original = TradeBlotter(source_events).position_as_of(as_of=dt(10), known_at=dt(10))
    replayed_blotter = TradeBlotter.from_event_envelopes(
        event_store.query(as_of=dt(10), known_at=dt(10))
    )
    replayed = replayed_blotter.position_as_of(as_of=dt(10), known_at=dt(10))

    assert replayed == original
