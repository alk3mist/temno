from datetime import date, time
from itertools import starmap

from temno import calendar
from temno.model import OutageEvent

_CAL = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Temno//Power Outages//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Power Outages
X-WR-TIMEZONE:Europe/Kyiv
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T080000
DTEND;TZID=Europe/Kyiv:20241230T123000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T190000
DTEND;TZID=Europe/Kyiv:20241230T220000
END:VEVENT
BEGIN:VEVENT
SUMMARY:DEFINITE_OUTAGE
DTSTART;TZID=Europe/Kyiv:20241230T233000
DTEND;TZID=Europe/Kyiv:20241231T000000
END:VEVENT
END:VCALENDAR"""


def test_from_events():
    raw_events = [
        (time(8), time(12, 30)),
        (time(19), time(22)),
        (time(23, 30), time(0)),
    ]
    events = starmap(OutageEvent.create_definite, raw_events)
    cal = calendar.from_events(events, date(2024, 12, 30))
    assert cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip() == _CAL
