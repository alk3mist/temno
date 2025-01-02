from collections.abc import Iterable

from .model import City, OutageEvent


def event(v: OutageEvent) -> str:
    fmt = "%H:%M"
    return f"{v.start:{fmt}} - {v.end:{fmt}}"


def events(v: Iterable[OutageEvent]) -> str:
    body = "\n".join(map(event, v))
    return body


def city(v: City) -> str:
    return f"{v.id} - {v.name}"


def cities(v: list[City]) -> str:
    return "\n".join(map(city, v))
