from collections.abc import Iterable
from datetime import date, datetime, timedelta
from typing import Final
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

from temno.model import OutageEvent

_TZ: Final[ZoneInfo] = ZoneInfo("Europe/Kyiv")


def map_event(d: date, e: OutageEvent) -> Event:
    event = Event()
    event.add("summary", e.type)
    event.start = datetime.combine(d, e.start, _TZ)
    end_day = d if e.end.hour != 0 else d + timedelta(days=1)
    event.end = datetime.combine(end_day, e.end, _TZ)
    return event


def from_events(events: Iterable[OutageEvent], day: date) -> Calendar:
    c = Calendar()
    c.add("version", "2.0")
    c.add("prodid", "-//Temno//Power Outages//EN")
    c.add("calscale", "GREGORIAN")
    c.add("method", "PUBLISH")
    c.add("x-wr-calname", "Power Outages")
    c.add("x-wr-timezone", _TZ.key)
    for e in events:
        c.add_component(map_event(day, e))

    return c
