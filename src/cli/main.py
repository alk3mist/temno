from datetime import datetime, timezone
from typing import cast

from rich import print

from minions import arange
from yasno_api import yasno
from yasno_api.schema import DaySchedule, OutageEvent, Region


def combine_events(events: list[OutageEvent]) -> list[OutageEvent]:
    groups = arange.consecutive_groups(events)
    combined_events = [
        arange.combination(g, OutageEvent.create_definite) for g in groups
    ]
    return cast(list[OutageEvent], combined_events)


def to_local_time(utc_dt: datetime) -> datetime:
    tz = datetime.now().astimezone().tzinfo
    local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz)
    return local_dt


def print_group_events(daily_events: DaySchedule, group: str) -> None:
    print(daily_events.title)
    try:
        events = daily_events.groups[group]
    except KeyError:
        print(f"Group {group} not found")
    else:
        print(combine_events(events))


def print_schedules(region: Region, group: str):
    schedule = yasno.fetch_schedule()
    print(f"updated at: {to_local_time(schedule.updated_at)}")
    print(f"{region} {group}")

    try:
        region_schedules = schedule.current[region]
    except KeyError:
        print(f"City {region} not found")
        return

    print_group_events(region_schedules.today, group)
    if region_schedules.tomorrow:
        print_group_events(region_schedules.tomorrow, group)


if __name__ == "__main__":
    print_schedules(region="dnipro", group="2.1")
