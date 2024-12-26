from datetime import datetime, timezone
from typing import Literal, cast

from rich import print

from minions import arange
from yasno_api import yasno
from yasno_api.schema import OutageEvent


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


def print_schedule(city: Literal["kiev", "dnipro"], group: str):
    schedule = yasno.fetch_schedule()
    print(f"updated at: {to_local_time(schedule.updated_at)}")
    print(f"{city} {group}")

    try:
        city_schedule = schedule.daily_schedule[city]
    except KeyError:
        print(f"City {city} not found")
        raise

    try:
        today_group = city_schedule.today.groups[group]
    except KeyError:
        print(f"Group {group} not found for today")
        raise

    print(city_schedule.today.title)
    print(combine_events(today_group))

    if city_schedule.tomorrow:
        print(city_schedule.tomorrow.title)
        try:
            tomorrow_group = city_schedule.tomorrow.groups[group]
        except KeyError:
            print(f"Group {group} not found for tomorrow")
        else:
            print(combine_events(tomorrow_group))


if __name__ == "__main__":
    print_schedule(city="dnipro", group="2.1")
