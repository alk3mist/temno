# 3. Use HTTPX for API Client

Date: 2024-12-27

## Status

Accepted

## Context

We need the HTTP client library for API calls.

## Decision

Use the HTTPX package.

## Consequences

A new dependency has been introduced.
Sync and async modes for HTTP calls are available.
API calls can be moked in tests with the RESPX package.
