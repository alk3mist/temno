"""Implements the Plugin pattern for DI"""

import uuid
from datetime import datetime
from typing import Annotated

import wireup
from rich.console import Console

from temno.calendar import Clock, IdGenerator
from temno.views import YasnoAPI
from yasno_api import client

container = wireup.create_container()


@container.register
def get_yasno() -> YasnoAPI:
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


@container.register()
def get_id_generator() -> IdGenerator:
    return lambda: uuid.uuid4().hex


@container.register()
def get_clock() -> Clock:
    return datetime.now
