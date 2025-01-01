# 5. Use VCR for API calls

Date: 2024-12-27

## Status

Accepted

## Context

Yasno API response is complex and could be changed over time.
The refactoring of the API's schema requires its continuous validation against response.
We need the VCR functionality only in tests for now.

## Decision

Use the pytest-recording package to record and reuse the API responses.

## Consequences

A new dependency has been introduced.
API schema could be easily tested against recorded response.
