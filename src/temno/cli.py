import logging
from calendar import day_abbr
from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, assert_never

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from temno import views
from temno.bootstrap import Container
from temno.calendar import render_calendar
from temno.model import OutageEvent, Region, When

app = typer.Typer(no_args_is_help=True)
schedule = typer.Typer(no_args_is_help=True)


@app.callback()
def setup(
    debug: Annotated[bool, typer.Option()] = False,
    pretty: bool = True,
) -> None:
    container = Container()
    container.config.from_dict({"pretty": pretty})
    container.wire(modules=[__name__])
    if debug:
        logging.basicConfig(level=logging.DEBUG)


ICalOption = Annotated[
    Path | None,
    typer.Option(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        help='The name of the iCalendar file to export to(e.g. "group_1_1.ics").',
        rich_help_panel="Export as iCalendar",
    ),
]


@schedule.command(help="Print the daily outage schedule or export as iCalendar.")
def daily(
    region: Annotated[Region, typer.Argument()],
    group: Annotated[str, typer.Argument()],
    when: Annotated[When, typer.Argument()] = When("today"),
    ical: ICalOption = None,
) -> None:
    with _simple_progress() as progress:
        progress.add_task("Fetching schedule...")
        try:
            yasno = Container.yasno()
            events = views.daily_events(region, group, when, api=yasno)
        except views.TemnoException as e:
            return _error_exit(e.msg)

    if ical is None:
        output = "\n".join(map(_event_to_str, events))
        _log(output)
        raise typer.Exit()

    events_by_day: list[Iterable[OutageEvent]]
    if when == When.today:
        events_by_day = [events]
    elif when == When.tomorrow:
        events_by_day = [[], events]
    else:
        assert_never(when)

    _save_calendar(events_by_day, ical)


@schedule.command(help="Print the weekly outage schedule or export as iCalendar.")
def weekly(
    region: Annotated[Region, typer.Argument()],
    group: Annotated[str, typer.Argument()],
    ical: ICalOption = None,
) -> None:
    with _simple_progress() as progress:
        progress.add_task("Fetching schedule...")
        try:
            yasno = Container.yasno()
            events = views.weekly_events(region, group, api=yasno)
        except views.TemnoException as e:
            return _error_exit(e.msg)

    if ical is not None:
        _save_calendar(events, ical)
        raise typer.Exit()

    for i, day in enumerate(events):
        day_name = day_abbr[i].upper()
        output = "\n".join((f"{day_name} - {_event_to_str(e)}" for e in day))
        _log(output)


def _simple_progress() -> Progress:
    console = Container.console()
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    )


def _error_exit(msg: str) -> None:
    err_console = Container.err_console()
    err_console.print(msg)
    raise typer.Exit(1)


def _log(msg: str) -> None:
    console = Container.console()
    console.print(msg)


def _save_calendar(events_by_day: Iterable[Iterable[OutageEvent]], ical: Path) -> None:
    clock = Container.clock()
    get_next_id = Container.id_generator()
    cal = render_calendar(events_by_day, clock, get_next_id)
    ical.write_bytes(cal.to_ical())
    _log(f'Calendar saved to "{ical.name}"')


def _event_to_str(e: OutageEvent) -> str:
    fmt = "%H:%M"
    return f"{e.start:{fmt}} - {e.end:{fmt}} - {e.type}"


app.add_typer(
    schedule,
    name="schedule",
    help="Print schedules or export as an iCalendar.",
)


@app.command(help="List the cities of the region.")
def cities(
    region: Region = typer.Argument(),
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    with _simple_progress() as progress:
        progress.add_task("Fetching cities...")
        yasno = Container.yasno()
        cities = views.cities(region, search, api=yasno)

    output = "\n".join((f"{c.id} - {c.name}" for c in cities))
    _log(output)


@app.command(help="List the city streets in the region.")
def streets(
    region: Annotated[Region, typer.Argument()],
    city_id: Annotated[int, typer.Option()],
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    with _simple_progress() as progress:
        progress.add_task("Fetching streets...")
        yasno = Container.yasno()
        streets = views.streets(region, city_id, search, api=yasno)

    output = "\n".join((f"{s.id} - {s.name}" for s in streets))
    _log(output)


@app.command(
    help="List the houses of the street along with the group of power outages."
)
def houses(
    region: Annotated[Region, typer.Argument()],
    street_id: Annotated[int, typer.Option()],
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    with _simple_progress() as progress:
        progress.add_task("Fetching houses...")
        yasno = Container.yasno()
        houses = views.houses(region, street_id, search, api=yasno)

    output = "\n".join((f"{h.name} - {h.group}" for h in houses))
    _log(output)
