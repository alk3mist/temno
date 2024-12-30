from collections.abc import Iterable
from datetime import date, datetime, timedelta, timezone, tzinfo
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

from yasno_api.schema import OutageEvent


def hours(d: date, v: float, tz: tzinfo = timezone.utc) -> datetime:
    dt = datetime.fromtimestamp(0, timezone.utc) + timedelta(hours=v)
    t = dt.time()
    return datetime.combine(d, t, tz)


def map_event(d: date, e: OutageEvent) -> Event:
    event = Event()
    event.add("summary", e.type)
    tz = ZoneInfo("Europe/Kyiv")
    event.start = hours(d, e.start, tz)
    event.end = hours(d, e.end, tz)
    return event


def generate(events: Iterable[OutageEvent]) -> Calendar:
    c = Calendar()
    c.add("prodid", "-//Power outages//Temno//en")
    c.add("version", "2.0")
    c["summary"] = "Power Outages"
    d = date.today()
    for e in events:
        c.add_component(map_event(d, e))

    return c
