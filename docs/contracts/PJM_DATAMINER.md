# PJM Data Miner

Status: canonical
Last updated: 2026-06-09
Backing ADR: ADR-029

## Scope

Implement a direct PJM Data Miner client with raw-call persistence, pagination, checkpointing, and revision-aware normalization.

## Required metadata

```text
feed_name
request_url
query_params
valid_time
source_time
source_publish_time
source_last_updated_time
capture_time
ingest_time
knowledge_time
raw_payload_hash
normalization_version
revision_policy
```

## Events

```text
RawPjmDataMinerCall
PjmObservationEvent
PjmRevisionEvent
PjmIngestCheckpointEvent
```

## Rules

- PJM is public/fundamental/underlying data for the power vertical.
- PJM does not drive Henry marks.
- Corrections, reposts, and overwrites are new events.
