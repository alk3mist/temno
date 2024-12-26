from abc import ABC
from datetime import datetime
from typing import Annotated, Literal, Self

from pydantic import AliasChoices, BaseModel, Field

type Region = Literal["kiev", "dnipro"]


class BaseComponent(BaseModel, ABC):
    anchor: str
    available_regions: list[Region]


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


class DailyGroups(BaseModel):
    groups: dict[str, list[OutageEvent]]
    title: str


class DailySchedule(BaseModel):
    today: DailyGroups
    tomorrow: DailyGroups | None = None


type WeeklySchedule = Annotated[
    list[list[OutageEvent]], Field(min_length=7, max_length=7)
]


type WeeklyGroups = dict[str, WeeklySchedule]


class ScheduleComponent(BaseComponent):
    template_name: Literal["electricity-outages-daily-schedule"]
    title: str
    description: str
    updated_at: datetime = Field(
        validation_alias=AliasChoices("updated_at", "lastRegistryUpdateTime")
    )
    daily_schedule: dict[Region, DailySchedule] = Field(
        validation_alias=AliasChoices("daily_schedule", "dailySchedule")
    )
    schedule: dict[Region, WeeklyGroups]


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
            raise RuntimeError("Schedule not found")
