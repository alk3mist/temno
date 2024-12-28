from datetime import datetime

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
                    groups={
                        "1.1": [
                            # "08:00 - 10:30",
                            OutageEvent.create_definite(8, 8.5),
                            OutageEvent.create_definite(8.5, 9),
                            OutageEvent.create_definite(9, 9.5),
                            OutageEvent.create_definite(9.5, 10),
                            OutageEvent.create_definite(10, 10.5),
                            # "19:00 - 22:00",
                            OutageEvent.create_definite(19, 19.5),
                            OutageEvent.create_definite(19.5, 20),
                            OutageEvent.create_definite(20, 20.5),
                            OutageEvent.create_definite(20.5, 21),
                            OutageEvent.create_definite(21, 21.5),
                            OutageEvent.create_definite(21.5, 22),
                        ],
                    },
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
            "1.1",
            [
                "Region: Dnipro",
                "Group: 1.1",
                "Today",
                "08:00 - 10:30",
                "19:00 - 22:00",
                "Tomorrow",
                "😸 no outages 😸",
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
