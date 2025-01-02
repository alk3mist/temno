from collections.abc import Iterable
from datetime import datetime, time, timedelta, timezone
from typing import cast

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
    temno_events = list(map(event_to_model_event, events))
    combined_events = arange.combine_consecutive_groups(
        temno_events, model.OutageEvent.create_definite
    )
    combined_events = cast(Iterable[model.OutageEvent], combined_events)
    return combined_events
