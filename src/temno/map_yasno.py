from collections.abc import Iterable
from datetime import datetime, time, timedelta, timezone
from itertools import chain
from typing import assert_never, cast

import more_itertools

from temno import arange, model
from yasno_api import schema as _yasno


def hours_to_time(v: float) -> time:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    ret = dt.time()
    return ret


def event_to_model_event(v: _yasno.OutageEvent) -> model.OutageEvent:
    return model.OutageEvent(
        start=hours_to_time(v.start),
        end=hours_to_time(v.end),
        type=v.type,
    )


def events_to_model_events(
    events: Iterable[_yasno.OutageEvent],
) -> Iterable[model.OutageEvent]:
    sorted_events = cast(list[_yasno.OutageEvent], arange.sort(events))
    groups_by_type = more_itertools.split_when(
        sorted_events,
        pred=lambda a, b: a.type != b.type,
    )
    return chain.from_iterable(map(__events_to_model_events, groups_by_type))


def __events_to_model_events(
    events: Iterable[_yasno.OutageEvent],
) -> Iterable[model.OutageEvent]:
    temno_events = map(event_to_model_event, events)
    head = more_itertools.first(temno_events, None)
    if head is None:
        return []

    events_type = head.type
    if events_type == "DEFINITE_OUTAGE":
        factory = model.OutageEvent.create_definite
    elif events_type == "POSSIBLE_OUTAGE":
        factory = model.OutageEvent.create_possible
    else:
        assert_never(events_type)

    temno_events = more_itertools.prepend(head, temno_events)
    combined_events = arange.combine_consecutive_groups(temno_events, factory)
    return cast(Iterable[model.OutageEvent], combined_events)
