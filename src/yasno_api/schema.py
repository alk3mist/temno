from abc import ABC
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import AliasChoices, BaseModel, Field

Region = StrEnum("Region", ["kiev", "dnipro"])


class BaseComponent(BaseModel, ABC):
    anchor: str = ""
    available_regions: list[Region] = []


class EditorComponent(BaseComponent):
    template_name: Literal["editor"]


class FAQComponent(BaseComponent):
    template_name: Literal["FrequentlyAskedQuestions"]


class OutageEvent(BaseModel):
    start: float
    end: float
    type: Literal["DEFINITE_OUTAGE", "POSSIBLE_OUTAGE"]

    @classmethod
    def create_definite(cls, start: float, end: float) -> Self:
        return cls(start=start, end=end, type="DEFINITE_OUTAGE")


class DaySchedule(BaseModel):
    title: str
    groups: dict[str, list[OutageEvent]]


class CurrentSchedules(BaseModel):
    today: DaySchedule
    tomorrow: DaySchedule | None = None


class ScheduleComponent(BaseComponent):
    template_name: Literal["electricity-outages-daily-schedule"] = (
        "electricity-outages-daily-schedule"
    )
    title: str = ""
    description: str = ""
    current: dict[Region, CurrentSchedules] | None = Field(
        None, validation_alias=AliasChoices("current", "dailySchedule")
    )


type Component = Annotated[
    EditorComponent | ScheduleComponent | FAQComponent,
    Field(discriminator="template_name"),
]


class ScheduleResponse(BaseModel):
    components: list[Component]

    @property
    def schedule(self) -> ScheduleComponent:
        for c in self.components:
            if isinstance(c, ScheduleComponent):
                return c
        else:
            raise RuntimeError("Schedule components not found")


class City(BaseModel):
    id: int
    name: str


class Street(BaseModel):
    id: int
    name: str


class House(BaseModel):
    street_id: int
    name: str
    group: str
