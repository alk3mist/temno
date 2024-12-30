from itertools import starmap

from temno import calendar
from yasno_api.schema import OutageEvent

_CAL = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Power outages//Temno//en
SUMMARY:Power Outages
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
END:VCALENDAR"""


def test_generate():
    cal = calendar.generate(starmap(OutageEvent.create_definite, [(8, 12.5), (19, 22)]))
    assert cal.to_ical().decode("utf-8").replace("\r\n", "\n").strip() == _CAL
