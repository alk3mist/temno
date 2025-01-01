from collections.abc import Iterable

from temno import map_yasno, model
from temno.bootstrap import container
from temno.factories import YasnoAPI
from yasno_api import schema


class TemnoException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self.msg = msg
        super().__init__(*args)


@container.autowire
def get_events(
    region: model.Region,
    group: str,
    when: model.When = model.When("today"),
    *,
    yasno: YasnoAPI,
) -> Iterable[model.OutageEvent]:
    schedule = yasno.fetch_schedule()

    if not schedule.current:
        raise TemnoException("Current schedule not found")

    try:
        region_schedule = schedule.current[region.to_yasno()]
    except KeyError:
        raise TemnoException("Schedule for the region not found")

    day_schedule: schema.DaySchedule | None = getattr(region_schedule, when, None)
    if day_schedule is None:
        raise TemnoException("Schedule for the day not found")

    try:
        events = day_schedule.groups[group]
    except KeyError:
        raise TemnoException("Schedule for the group not found")

    temno_events = map_yasno.events_to_model_events(events)
    return temno_events


@container.autowire
def get_cities(
    region: model.Region,
    *,
    yasno: YasnoAPI,
) -> Iterable[model.City]:
    return yasno.fetch_cities(region.to_yasno())
