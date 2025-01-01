import logging
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from wireup import Inject

from temno import commands, render
from temno.bootstrap import container
from temno.model import Region, When

app = typer.Typer(no_args_is_help=True)


@app.callback()
def setup(
    debug: Annotated[bool, typer.Option()] = False,
    pretty: bool = True,
):
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
):
    with simple_progress() as progress:
        progress.add_task("Fetching schedule...")

        try:
            events = commands.get_events(region, group, when)
        except commands.TemnoException as e:
            return error_exit(e.msg)

    log(render.events(events))


@app.command()
def cities(region: Region = typer.Option()):
    with simple_progress() as progress:
        progress.add_task("Fetching cities...")
        cities = commands.get_cities(region)

    log(render.cities(cities))
