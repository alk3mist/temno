import logging
from enum import StrEnum, auto
from typing import Annotated, assert_never

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from temno import map_yasno, render
from yasno_api import schema, yasno

app = typer.Typer(no_args_is_help=True)


class Region(StrEnum):
    dnipro = auto()
    kyiv = auto()

    def to_yasno(self) -> schema.Region:
        if self == Region.dnipro:
            return "dnipro"
        elif self == Region.kyiv:
            return "kiev"
        else:
            assert_never(self)


class When(StrEnum):
    today = auto()
    tomorrow = auto()


console: Console
error_console: Console


@app.callback()
def setup(
    debug: Annotated[bool, typer.Option()] = False,
    pretty: bool = True,
):
    global console, error_console
    console = Console(
        no_color=not pretty,
        highlight=pretty,
    )
    error_console = Console(
        stderr=True,
        style="bold red",
        no_color=not pretty,
        highlight=pretty,
    )
    if debug:
        logging.basicConfig(level=logging.DEBUG)


def error_exit(msg: str) -> None:
    error_console.print(msg)
    raise typer.Exit(1)


@app.command()
def schedule(
    region: Annotated[Region, typer.Argument()],
    group: Annotated[str, typer.Argument()],
    when: Annotated[When, typer.Argument()] = When("today"),
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Fetching schedules...")
        schedule = yasno.fetch_schedule()

    if not schedule.current:
        return error_exit("Current schedule not found")

    try:
        region_schedule = schedule.current[region.to_yasno()]
    except KeyError:
        return error_exit("Schedule for the region not found")

    day_schedule: schema.DaySchedule | None = getattr(region_schedule, when, None)
    if day_schedule is None:
        return error_exit("Schedule for the day not found")

    try:
        events = day_schedule.groups[group]
    except KeyError:
        return error_exit("Schedule for the group not found")

    temno_events = map_yasno.events_to_model_events(events)
    output = render.events(temno_events)
    console.print(output)


@app.command()
def cities(region: Region = typer.Option()):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Fetching schedules...")
        cities = yasno.fetch_cities(region.to_yasno())

    console.print(render.cities(cities))
