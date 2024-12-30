from functools import partial
from itertools import starmap

import pytest

from cli import render
from yasno_api.schema import OutageEvent


@pytest.mark.parametrize(
    "values,result",
    [
        (
            (
                (8.0, 8.5),
                (8.5, 9.0),
                (9.0, 9.5),
                (19.0, 19.5),
                (19.5, 20.0),
                (20.0, 20.5),
                (20.5, 21.0),
            ),
            ["08:00 - 09:30", "19:00 - 21:00"],
        ),
        ([], [""]),
    ],
)
def test_events(values: tuple[tuple[float, float], ...], result: str):
    assert render.events(_make_events(values)) == "\n".join(result)


_make_events = partial(starmap, OutageEvent.create_definite)
