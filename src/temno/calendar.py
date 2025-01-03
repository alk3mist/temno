from collections.abc import Callable, Iterable
from datetime import date, datetime, timedelta
from typing import Final
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

from temno.model import OutageEvent

_TZ: Final[ZoneInfo] = ZoneInfo("Europe/Kyiv")


type IdGenerator = Callable[[], str]


def _calendar_event(
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


def _calendar_metadata() -> dict[str, str]:
    return {
        "version": "2.0",
        "prodid": "-//Temno//Power Outages//EN",
        "calscale": "GREGORIAN",
        "method": "PUBLISH",
        "summary": "Power Outages",
        "x-wr-calname": "Power Outages",
        "x-wr-timezone": _TZ.key,
    }


def from_events(
    events: Iterable[tuple[date, Iterable[OutageEvent]]],
    ts: datetime,
    get_next_id: IdGenerator,
) -> Calendar:
    c = Calendar()
    c.update(_calendar_metadata())
    for day, day_events in events:
        for e in day_events:
            c_event = _calendar_event(day, e, ts, get_next_id)
            c.add_component(c_event)
    return c
