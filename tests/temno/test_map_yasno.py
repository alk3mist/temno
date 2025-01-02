from datetime import time

import pytest

from temno import map_yasno, model
from yasno_api import schema as yasno


@pytest.mark.parametrize(
    "values,result",
    [
        (
            [
                (7.5, 8.0, "DEFINITE_OUTAGE"),
                (8.0, 8.5, "DEFINITE_OUTAGE"),
            ],
            [
                (time(7, 30), time(8, 30), "DEFINITE_OUTAGE"),
            ],
        ),
        (
            [
                (7.0, 8.5, "DEFINITE_OUTAGE"),
                (8.5, 9.0, "POSSIBLE_OUTAGE"),
            ],
            [
                (time(7, 00), time(8, 30), "DEFINITE_OUTAGE"),
                (time(8, 30), time(9, 00), "POSSIBLE_OUTAGE"),
            ],
        ),
        (
            [
                (9.0, 9.5, "POSSIBLE_OUTAGE"),
                (14.0, 14.5, "POSSIBLE_OUTAGE"),
                (14.5, 15.0, "POSSIBLE_OUTAGE"),
            ],
            [
                (time(9, 00), time(9, 30), "POSSIBLE_OUTAGE"),
                (time(14, 00), time(15, 00), "POSSIBLE_OUTAGE"),
            ],
        ),
        ([], []),
    ],
)
def test_events_to_model_events(
    values: list[tuple[float, float, yasno.EventType]],
    result: list[tuple[time, time, model.EventType]],
):
    yasno_events = (
        yasno.OutageEvent(start=start, end=end, type=type_)
        for (start, end, type_) in values
    )
    events = map_yasno.events_to_model_events(yasno_events)
    expected = [
        model.OutageEvent(start=start, end=end, type=type_)
        for (start, end, type_) in result
    ]
    assert list(events) == expected
