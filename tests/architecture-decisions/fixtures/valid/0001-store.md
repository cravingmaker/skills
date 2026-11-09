---
status: accepted
owner: storage
---
# Choose a single owning writer

## Context

Concurrent imports must preserve exact source values.

## Decision

The ingest component owns canonical writes.

## Confirmation

The source-value readback and concurrent import fixtures pass locally.
