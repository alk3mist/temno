# 4. Use HTTP caching for API calls

Date: 2024-12-27

## Status

Accepted

## Context

Yasno's API utilizes Etag for response caching.
HTTPX library doesn't contain the response caching out of the box.
Schedule updates rarely(~up to 10 times a day).
We'd like to make requests often for the fresh data.

## Decision

The change that we're proposing or have agreed to implement.
Use HTTP caching via the Hishel package.

## Consequences

A new dependency has been introduced.
The network traffic for API calls reduced.