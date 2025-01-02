import logging
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from wireup import Inject

from temno import views
from temno.bootstrap import container
from temno.model import Region, When

app = typer.Typer(no_args_is_help=True)


@app.callback()
def setup(
    debug: Annotated[bool, typer.Option()] = False,
    pretty: bool = True,
) -> None:
    container.params.update({"pretty": pretty})
    if debug:
        logging.basicConfig(level=logging.DEBUG)


@container.autowire
def error_exit(
    msg: str, *, err_console: Annotated[Console, Inject(qualifier="error")]
) -> None:
    err_console.print(msg)
    raise typer.Exit(1)


@container.autowire
def log(msg: str, *, console: Annotated[Console, Inject()]) -> None:
    console.print(msg)


def simple_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )


@app.command()
def schedule(
    region: Annotated[Region, typer.Argument()],
    group: Annotated[str, typer.Argument()],
    when: Annotated[When, typer.Argument()] = When("today"),
) -> None:
    yasno = container.get(views.YasnoAPI)
    with simple_progress() as progress:
        progress.add_task("Fetching schedule...")
        try:
            events = views.events(region, group, when, yasno=yasno)
        except views.TemnoException as e:
            return error_exit(e.msg)

    fmt = "%H:%M"
    output = "\n".join((f"{e.start:{fmt}} - {e.end:{fmt}}" for e in events))
    log(output)


@app.command()
def cities(
    region: Region = typer.Argument(),
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    yasno = container.get(views.YasnoAPI)
    with simple_progress() as progress:
        progress.add_task("Fetching cities...")
        cities = views.cities(region, search, yasno=yasno)

    output = "\n".join((f"{c.id} - {c.name}" for c in cities))
    log(output)


@app.command()
def streets(
    region: Annotated[Region, typer.Argument()],
    city_id: Annotated[int, typer.Option()],
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    yasno = container.get(views.YasnoAPI)
    with simple_progress() as progress:
        progress.add_task("Fetching streets...")
        streets = views.streets(region, city_id, search, yasno=yasno)

    output = "\n".join((f"{s.id} - {s.name}" for s in streets))
    log(output)


@app.command()
def houses(
    region: Annotated[Region, typer.Argument()],
    street_id: Annotated[int, typer.Option()],
    search: Annotated[str | None, typer.Option()] = None,
) -> None:
    yasno = container.get(views.YasnoAPI)
    with simple_progress() as progress:
        progress.add_task("Fetching houses...")
        houses = views.houses(region, street_id, search, yasno=yasno)

    output = "\n".join((f"{h.name} - {h.group}" for h in houses))
    log(output)
