# Event Envelope

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-027, ADR-032

## Shape

```python
class EventEnvelope:
    event_id: str
    stream_id: str
    stream_sequence: int
    event_type: str
    source_system: str       # ice_python | pjm_dataminer | manual_blotter | system_calc | fixture
    data_scope: str          # synthetic | public | derived | local_live
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
    payload: dict
```

## Rules

- `stream_sequence` is monotonic only within `stream_id`.
- There is no global sequence invariant.
- Updates/deletes are not allowed at the event API level.
- Corrections, reposts, amendments, and busts are new events.
- Snapshot IDs include event hashes plus relevant `normalization_version`, `calendar_version`, model version, and calculation version.
- Decimal payload values serialize deterministically as strings.
- Datetimes serialize as timezone-aware RFC3339 UTC; exchange timezone may be carried as payload metadata.
