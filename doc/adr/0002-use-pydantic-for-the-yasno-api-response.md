# 2. Use Pydantic for Yasno API response

Date: 2024-12-27

## Status

Accepted

## Context

The Yasno API response is big and purely designed(probably intended for use with UI only).

## Decision

Use Pydantic for parsing/validating the Yasno API response.

## Consequences

A new dependency has been introduced.
It'll much easier to manipulate the response in client's code.  
