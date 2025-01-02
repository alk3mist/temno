from datetime import time
from functools import partial
from itertools import starmap

import pytest

from temno import map_yasno, model
from yasno_api import schema as yasno


@pytest.mark.parametrize(
    "values,result",
    [
        (
            [
                (8.0, 8.5),
                (8.5, 9.0),
                (9.0, 9.5),
                (19.0, 19.5),
                (19.5, 20.0),
                (20.0, 20.5),
                (20.5, 21.0),
                (23.5, 24.0),
            ],
            [
                (time(8, 00), time(9, 30)),
                (time(19, 00), time(21, 00)),
                (time(23, 30), time(0, 00)),
            ],
        ),
        ([], []),
    ],
)
def test_events_to_model_events(
    values: list[tuple[float, float]], result: list[tuple[time, time]]
):
    yasno_events = _make_yasno_events(values)
    model_events = map_yasno.events_to_model_events(yasno_events)
    assert list(model_events) == list(_make_model_events(result))


@pytest.mark.parametrize(
    "values,result",
    [
        (
            [
                (8, 8.5, "DEFINITE_OUTAGE"),
                (8.5, 9.0, "POSSIBLE_OUTAGE"),
                (9.0, 9.5, "POSSIBLE_OUTAGE"),
            ],
            [
                (time(8, 00), time(8, 30), "DEFINITE_OUTAGE"),
                (time(8, 30), time(9, 30), "POSSIBLE_OUTAGE"),
            ],
        ),
    ],
)
def test_events_to_model_events_different_types(
    values: list[tuple[float, float, yasno.EventType]],
    result: list[tuple[time, time, model.EventType]],
): ...


_make_yasno_events = partial(starmap, yasno.OutageEvent.create_definite)
_make_model_events = partial(starmap, model.OutageEvent.create_definite)
