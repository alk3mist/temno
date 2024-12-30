# TODO: generate calendar for daily events


from collections.abc import Iterable
from datetime import date, datetime, timedelta, timezone
from functools import partial

from ical.calendar import Calendar
from ical.event import Event

from yasno_api.schema import OutageEvent


def hours(d: date, v: float) -> datetime:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    t = dt.time()
    d = date.today()
    return datetime.combine(d, t)


def map_event(d: date, e: OutageEvent) -> Event:
    ret = Event(
        name=e.type,
        dtstart=hours(d, e.start),
        dtend=hours(d, e.end),
    )
    return ret


def generate(events: Iterable[OutageEvent]) -> Calendar:
    c = Calendar()
    c.events.extend(list(map(partial(map_event, date.today()), events)))

    return c
