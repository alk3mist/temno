from datetime import datetime
from itertools import starmap

import pytest

from cli import render
from yasno_api.schema import (
    CurrentSchedules,
    DaySchedule,
    OutageEvent,
    Region,
    ScheduleComponent,
)


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

    return ScheduleComponent(
        anchor="foo",
        template_name="electricity-outages-daily-schedule",
        title="bar",
        description="baz",
        available_regions=["kiev", "dnipro"],
        updated_at=datetime.now(),
        current={
            "dnipro": CurrentSchedules(
                today=DaySchedule(
                    title="Today",
                    groups={"1.1": _to_events(_8_to_9_30 + _19_to_21)},
                ),
                tomorrow=DaySchedule(title="Tomorrow", groups={"1.1": []}),
            ),
            "kiev": CurrentSchedules(
                today=DaySchedule(title="Today", groups={"1.1": []})
            ),
        },
    )


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


def _to_events(ranges: list[tuple[float, float]]) -> list[OutageEvent]:
    return list(starmap(OutageEvent.create_definite, ranges))
