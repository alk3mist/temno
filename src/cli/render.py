from collections.abc import Iterable
from datetime import datetime, time, timedelta, timezone
from typing import cast

from minions import arange
from yasno_api.schema import City, OutageEvent


def hours(v: float) -> time:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    ret = dt.time()
    return ret


def event(event: OutageEvent) -> str:
    fmt = "%H:%M"
    return f"{hours(event.start):{fmt}} - {hours(event.end):{fmt}}"


def _combine_events(events: Iterable[OutageEvent]) -> Iterable[OutageEvent]:
    groups = arange.consecutive_groups(arange.sort(events))
    combined_events = (
        arange.combination(g, OutageEvent.create_definite) for g in groups
    )
    return cast(Iterable[OutageEvent], combined_events)


def events(events_: Iterable[OutageEvent]) -> str:
    events = _combine_events(events_)
    body = "\n".join(map(event, events))
    return body


def city(city_: City) -> str:
    return f"{city_.id} - {city_.name}"


def cities(cities_: list[City]) -> str:
    return "\n".join(map(city, cities_))
