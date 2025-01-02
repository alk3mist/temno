from typing import Annotated

import wireup
from rich.console import Console

from temno import views
from yasno_api import client

container = wireup.create_container()


@container.register
def get_yasno() -> views.YasnoAPI:
    return client


@container.register
def console(*, pretty: Annotated[bool, wireup.Inject(param="pretty")]) -> Console:
    return Console(
        no_color=not pretty,
        highlight=pretty,
    )


@container.register(qualifier="error")
def err_console(*, pretty: Annotated[bool, wireup.Inject(param="pretty")]) -> Console:
    return Console(
        stderr=True,
        style="bold red",
        no_color=not pretty,
        highlight=pretty,
    )
