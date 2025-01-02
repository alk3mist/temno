from collections.abc import Iterable
from operator import attrgetter

from temno import map_yasno, model
from temno.factories import YasnoAPI
from yasno_api import schema


class TemnoException(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self.msg = msg
        super().__init__(*args)


def events(
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


def cities(
    region: model.Region, search: str | None = None, *, yasno: YasnoAPI
) -> Iterable[model.City]:
    response = yasno.fetch_cities(region.to_yasno())
    if not search:
        return response
    return _search(response, "name", search)


def streets(
    region: model.Region, city_id: int, search: str | None = None, *, yasno: YasnoAPI
) -> Iterable[model.Street]:
    response = yasno.fetch_streets(region.to_yasno(), city_id)
    if not search:
        return response
    return _search(response, "name", search)


def houses(
    region: model.Region, street_id: int, search: str | None = None, *, yasno: YasnoAPI
) -> Iterable[model.House]:
    response = yasno.fetch_houses(region.to_yasno(), street_id)
    if not search:
        return response
    return _search(response, "name", search)


def _search[T](items: Iterable[T], field_name: str, search_word: str) -> Iterable[T]:
    normalized_search = _normalize_text(search_word)
    get_field = attrgetter(field_name)
    return (i for i in items if normalized_search in _normalize_text(get_field(i)))


def _normalize_text(w: str) -> str:
    return w.lower().replace("'", "’")
