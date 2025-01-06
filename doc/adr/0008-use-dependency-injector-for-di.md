# 8. Use Dependency Injector for DI

Date: 2025-01-06

## Status

Accepted

Supersedes [7. Use Wireup for DI](0007-use-wireup-for-di.md)

## Context

The dependency-injector package is a mature framework.
The wireup package is new and still in the process of implementing features that are already in the dependency injector.
The packages have similar interface.


## Decision

Use the dependency-injector package for DI.

## Consequences

A dependency has been replaced.
The project uses a reliable framework instead of one that is still in development.
The override in tests now requires the `type: ignore` mark due to some typing issues of the DI framework.
