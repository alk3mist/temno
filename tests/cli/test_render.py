from itertools import starmap
from typing import Any

import pytest

from cli import render
from yasno_api.schema import OutageEvent, Region, ScheduleComponent


@pytest.fixture
def component() -> ScheduleComponent:
    _8_to_9_30 = [
        (8.0, 8.5),
        (8.5, 9.0),
        (9.0, 9.5),
    ]
    _19_to_21 = [
        (19.0, 19.5),
        (19.5, 20.0),
        (20.0, 20.5),
        (20.5, 21.0),
    ]
    current: dict[str, Any] = {
        "dnipro": {
            "today": {
                "title": "Today",
                "groups": {"1.1": _to_events(_8_to_9_30 + _19_to_21)},
            },
            "tomorrow": {
                "title": "Tomorrow",
                "groups": {"1.1": []},
            },
        },
        "kiev": {
            "today": {
                "title": "Today",
                "groups": {"1.1": []},
            },
        },
    }
    return ScheduleComponent.model_validate({"dailySchedule": current})


@pytest.mark.parametrize(
    "region,group,result",
    [
        (
            "dnipro",
            "1.1",
            [
                "Region: Dnipro",
                "Group: 1.1",
                "Today",
                "08:00 - 09:30",
                "19:00 - 21:00",
                "Tomorrow",
                "😸 no outages 😸",
            ],
        ),
        (
            "kiev",
            "1.1",
            [
                "Region: Kyiv",
                "Group: 1.1",
                "Today",
                "😸 no outages 😸",
            ],
        ),
        (
            "dnipro",
            "2.1",
            [
                "Region: Dnipro",
                "Group: 2.1",
                "Today",
                "Group not found",
                "Tomorrow",
                "Group not found",
            ],
        ),
    ],
)
def test_component(
    region: Region,
    group: str,
    result: str,
    component: ScheduleComponent,
):
    assert render.schedule_component(component, region, group) == "\n".join(result)


def test_component_without_current_schedule(component: ScheduleComponent):
    without_current = component.model_copy(update={"current": None})
    expected = "😺 no current schedules 😺"
    assert render.schedule_component(without_current, "dnipro", "1.1") == expected


def _to_events(ranges: list[tuple[float, float]]) -> list[OutageEvent]:
    return list(starmap(OutageEvent.create_definite, ranges))
