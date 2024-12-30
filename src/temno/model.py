from datetime import date, time
from typing import Self

from pydantic import BaseModel

from yasno_api import schema as _yasno

type EventType = _yasno.EventType


class OutageEvent(BaseModel):
    start: time
    end: time
    type: EventType

    @classmethod
    def create_definite(cls, start: time, end: time) -> Self:
        return cls(start=start, end=end, type="DEFINITE_OUTAGE")


class DaySchedule(BaseModel):
    day: date
    events: list[OutageEvent]


type City = _yasno.City
