import logging
from enum import StrEnum
from typing import Annotated, cast, get_args

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli import render
from yasno_api import schema, yasno

app = typer.Typer(no_args_is_help=True)

Region = StrEnum("Region", list(get_args(schema.Region.__value__)))
When = StrEnum("When", ["today", "tomorrow"])

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
    region: Annotated[Region, typer.Option()],
    group: Annotated[str, typer.Option()],
    when: Annotated[When, typer.Option()],
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
        region_schedule = schedule.current[cast(schema.Region, region)]
    except KeyError:
        return error_exit("Schedule for the region not found")

    day_schedule: schema.DaySchedule | None = getattr(region_schedule, when, None)
    if day_schedule is None:
        return error_exit("Schedule for the day not found")

    try:
        events = day_schedule.groups[group]
    except KeyError:
        return error_exit("Schedule for the group not found")

    output = render.events(events)
    console.print(output)


@app.command()
def cities(region: Region = typer.Option(), *, ctx: typer.Context):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Fetching schedules...")
        cities = yasno.fetch_cities(cast(schema.Region, region))

    console.print(render.cities(cities))
