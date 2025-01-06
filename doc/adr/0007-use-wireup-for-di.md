# 7. Use Wireup for DI

Date: 2025-01-01

## Status

Superseded by [8. Use Dependency Injector for DI](0008-use-dependency-injector-for-di.md)

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
