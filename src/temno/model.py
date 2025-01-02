from datetime import date, time
from enum import StrEnum, auto
from typing import Self, assert_never

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
type Street = _yasno.Street
type House = _yasno.House


class Region(StrEnum):
    dnipro = auto()
    kyiv = auto()

    def to_yasno(self) -> _yasno.Region:
        if self == Region.dnipro:
            return "dnipro"
        elif self == Region.kyiv:
            return "kiev"
        else:
            assert_never(self)


class When(StrEnum):
    today = auto()
    tomorrow = auto()
