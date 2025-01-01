# 7. Use Wireup for DI

Date: 2025-01-01

## Status

Accepted

## Context

CLI testing requires patching Yasno API responses.
pytest-recording requires a separate cassette for each parameterized test.
Tests will be clearer if the inputs are declared explicitly.
Typer does not implement DI.

## Decision

Use the Wireup package for DI.

## Consequences

A new dependency has been introduced.
Patching different services should now be more convenient.
