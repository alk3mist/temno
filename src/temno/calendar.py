from collections.abc import Iterable, Iterator
from datetime import date, datetime, timedelta
from typing import Final, Protocol
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

from temno.model import OutageEvent

_TZ: Final[ZoneInfo] = ZoneInfo("Europe/Kyiv")


class IdGenerator(Protocol):
    def __call__(self) -> str: ...


class Clock(Protocol):
    def __call__(self) -> datetime:
        "Returns the current time."
        ...


def render_calendar(
    events_by_day: Iterable[Iterable[OutageEvent]],
    clock: Clock,
    get_next_id: IdGenerator,
) -> Calendar:
    "Creates a calendar assuming that the first day is today."
    c = Calendar()
    c.update(__calendar_metadata())
    now = clock()
    pairs = zip(__iter_dates(now.date()), events_by_day)
    for day, events in pairs:
        for event in events:
            c_event = __calendar_event(day, event, now, get_next_id)
            c.add_component(c_event)
    return c


def __calendar_metadata() -> dict[str, str]:
    return {
        "version": "2.0",
        "prodid": "-//Temno//Power Outages//EN",
        "calscale": "GREGORIAN",
        "method": "PUBLISH",
        "summary": "Power Outages",
        "x-wr-calname": "Power Outages",
        "x-wr-timezone": _TZ.key,
    }


def __calendar_event(
    day: date,
    outage_event: OutageEvent,
    ts: datetime,
    get_next_id: IdGenerator,
) -> Event:
    event = Event()
    event.add("summary", outage_event.type)
    event.add("dtstamp", ts)
    event["uid"] = get_next_id()

    event.start = datetime.combine(day, outage_event.start, _TZ)
    end_day = day if outage_event.end.hour != 0 else day + timedelta(days=1)
    event.end = datetime.combine(end_day, outage_event.end, _TZ)

    return event


def __iter_dates(start: date) -> Iterator[date]:
    yield start
    d = start
    while True:
        d += timedelta(days=1)
        yield d
