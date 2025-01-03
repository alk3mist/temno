import uuid
from datetime import date, datetime, time
from itertools import starmap

from icalendar import Calendar

from temno import calendar
from temno.model import OutageEvent

_CAL = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Temno//Power Outages//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
SUMMARY:Power Outages
X-WR-CALNAME:Power Outages
X-WR-TIMEZONE:Europe/Kyiv
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T080000
DTEND;TZID=Europe/Kyiv:20241230T123000
DTSTAMP:20241230T032200Z
UID:00000000000000000000000000000000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T190000
DTEND;TZID=Europe/Kyiv:20241230T220000
DTSTAMP:20241230T032200Z
UID:00000000000000000000000000000000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T233000
DTEND;TZID=Europe/Kyiv:20241231T000000
DTSTAMP:20241230T032200Z
UID:00000000000000000000000000000000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241231T180000
DTEND;TZID=Europe/Kyiv:20241231T220000
DTSTAMP:20241230T032200Z
UID:00000000000000000000000000000000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241231T233000
DTEND;TZID=Europe/Kyiv:20250101T000000
DTSTAMP:20241230T032200Z
UID:00000000000000000000000000000000
END:VEVENT
END:VCALENDAR"""


def test_from_events():
    day_1_raw_events = [
        (time(8), time(12, 30)),
        (time(19), time(22)),
        (time(23, 30), time(0)),
    ]
    day_2_raw_events = [
        (time(18), time(22)),
        (time(23, 30), time(0)),
    ]
    day_1_events = starmap(OutageEvent.create_definite, day_1_raw_events)
    day_2_events = starmap(OutageEvent.create_definite, day_2_raw_events)
    day_1 = date(2024, 12, 30)
    day_2 = date(2024, 12, 31)
    ts = datetime(2024, 12, 30, 3, 22)
    cal = calendar.from_events(
        events=[
            (day_1, day_1_events),
            (day_2, day_2_events),
        ],
        ts=ts,
        get_next_id=lambda: uuid.UUID(int=0).hex,
    )
    assert display_calendar(cal) == _CAL


def display_calendar(cal: Calendar) -> str:
    return cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip()
