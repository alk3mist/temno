# 9. Use Wireup for DI (again)

Date: 2025-04-16

## Status

Accepted

Supersedes [8. Use Dependency Injector for DI](0008-use-dependency-injector-for-di.md)

## Context

The Dependency injector package has many issues, for example unclear scopes.
Wireup has better design for the general purpose use and a more convenient interface.

## Decision

Use the Wireup package for DI.

## Consequences

A dependency has been replaced.
Code requires updates in order to match the new DI interface.
