from collections.abc import Iterable
from datetime import datetime, time, timedelta, timezone
from typing import cast

from temno import arange
from yasno_api.schema import City, OutageEvent


def hours(v: float) -> time:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    ret = dt.time()
    return ret


def event(v: OutageEvent) -> str:
    fmt = "%H:%M"
    return f"{hours(v.start):{fmt}} - {hours(v.end):{fmt}}"


def _combine_events(events: Iterable[OutageEvent]) -> Iterable[OutageEvent]:
    groups = arange.consecutive_groups(arange.sort(events))
    combined_events = (
        arange.combination(g, OutageEvent.create_definite) for g in groups
    )
    return cast(Iterable[OutageEvent], combined_events)


def events(v: Iterable[OutageEvent]) -> str:
    events_ = _combine_events(v)
    body = "\n".join(map(event, events_))
    return body


def city(v: City) -> str:
    return f"{v.id} - {v.name}"


def cities(v: list[City]) -> str:
    return "\n".join(map(city, v))
