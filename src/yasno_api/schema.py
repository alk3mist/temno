from abc import ABC
from typing import Annotated, Literal, Self

from pydantic import AliasChoices, BaseModel, Field

type Region = Literal["kiev", "dnipro"]
type EventType = Literal["DEFINITE_OUTAGE", "POSSIBLE_OUTAGE"]


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
    type: EventType

    @classmethod
    def create_definite(cls, start: float, end: float) -> Self:
        return cls(start=start, end=end, type="DEFINITE_OUTAGE")


class DaySchedule(BaseModel):
    title: str
    groups: dict[str, list[OutageEvent]]


class DailySchedules(BaseModel):
    today: DaySchedule | None = None
    tomorrow: DaySchedule | None = None


class ScheduleComponent(BaseComponent):
    template_name: Literal["electricity-outages-daily-schedule"] = (
        "electricity-outages-daily-schedule"
    )
    title: str = ""
    description: str = ""
    daily: dict[Region, DailySchedules] | None = Field(
        None, validation_alias=AliasChoices("daily", "dailySchedule")
    )
    weekly: dict[Region, dict[str, list[list[OutageEvent]]]] = Field(
        validation_alias=AliasChoices("weekly", "schedule"),
        default_factory=dict,
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
