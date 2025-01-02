from typing import Annotated, Protocol

import wireup
from rich.console import Console

from yasno_api import client, schema


class YasnoAPI(Protocol):
    def fetch_schedule(self) -> schema.ScheduleComponent: ...
    def fetch_cities(self, region: schema.Region) -> list[schema.City]: ...
    def fetch_streets(
        self, region: schema.Region, city_id: int
    ) -> list[schema.Street]: ...
    def fetch_houses(
        self, region: schema.Region, street_id: int
    ) -> list[schema.House]: ...


@wireup.service
def yasno() -> YasnoAPI:
    return client


@wireup.service
def console(*, pretty: Annotated[bool, wireup.Inject(param="pretty")]) -> Console:
    return Console(
        no_color=not pretty,
        highlight=pretty,
    )


@wireup.service(qualifier="error")
def err_console(*, pretty: Annotated[bool, wireup.Inject(param="pretty")]) -> Console:
    return Console(
        stderr=True,
        style="bold red",
        no_color=not pretty,
        highlight=pretty,
    )
