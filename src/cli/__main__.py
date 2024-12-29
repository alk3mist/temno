import logging
from typing import Annotated

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from cli import render
from yasno_api import yasno
from yasno_api.schema import Region


def main(
    region: Annotated[Region, typer.Option()],
    group: Annotated[str, typer.Option()],
    debug: bool = False,
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Fetching schedules...")
        schedule = yasno.fetch_schedule()

    print(render.schedule_component(schedule, region, group))


if __name__ == "__main__":
    typer.run(main)
