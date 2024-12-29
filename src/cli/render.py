from datetime import datetime, time, timedelta, timezone
from typing import NoReturn, cast

from minions import arange
from yasno_api.schema import DaySchedule, OutageEvent, Region, ScheduleComponent


def hours(v: float | int) -> time:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    ret = dt.time()
    return ret


def event(event: OutageEvent) -> str:
    fmt = "%H:%M"
    return f"{hours(event.start):{fmt}} - {hours(event.end):{fmt}}"


def region_(r: Region) -> str:
    if r == "dnipro":
        return "Dnipro"
    elif r == "kiev":
        return "Kyiv"
    else:
        return NoReturn(r)


group_ = str

dt = str


def _combine_events(events: list[OutageEvent]) -> list[OutageEvent]:
    groups = arange.consecutive_groups(arange.sort(events))
    combined_events = [
        arange.combination(g, OutageEvent.create_definite) for g in groups
    ]
    return cast(list[OutageEvent], combined_events)


def group_schedule(s: DaySchedule, group: str) -> str:
    try:
        events = _combine_events(s.groups[group])
    except KeyError:
        body = "Group not found"
    else:
        body = "\n".join(map(event, events)) or "😸 no outages 😸"
    return f"{s.title}\n{body}"


def schedule_component(component: ScheduleComponent, region: Region, group: str) -> str:
    if component.current is None:
        return "😺 no current schedules 😺"
    schedules = component.current[region]
    ret = f"""\
Region: {region_(region)}
Group: {group_(group)}
{group_schedule(schedules.today, group)}\
"""
    if schedules.tomorrow:
        ret += f"""
{group_schedule(schedules.tomorrow, group)}\
"""
    return ret
