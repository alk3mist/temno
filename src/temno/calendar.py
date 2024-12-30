from collections.abc import Iterable
from datetime import date, datetime
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

from temno.model import OutageEvent


def map_event(d: date, e: OutageEvent) -> Event:
    event = Event()
    event.add("summary", e.type)
    tz = ZoneInfo("Europe/Kyiv")
    event.start = datetime.combine(d, e.start, tz)
    event.end = datetime.combine(d, e.end, tz)
    return event


def from_events(events: Iterable[OutageEvent], day: date) -> Calendar:
    c = Calendar()
    c.add("prodid", "-//Power outages//Temno//en")
    c.add("version", "2.0")
    c["summary"] = "Power Outages"
    for e in events:
        c.add_component(map_event(day, e))

    return c
