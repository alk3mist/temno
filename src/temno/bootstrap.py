"""Implements the Plugin pattern for DI"""

import uuid
from datetime import datetime

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
from rich.console import Console

from temno.calendar import Clock, IdGenerator
from temno.views import YasnoAPI
from yasno_api import client


def get_yasno() -> YasnoAPI:
    return client


def console(pretty: bool) -> Console:
    return Console(
        no_color=not pretty,
        highlight=pretty,
    )


def err_console(pretty: bool) -> Console:
    return Console(
        stderr=True,
        style="bold red",
        no_color=not pretty,
        highlight=pretty,
    )


def get_id_generator() -> IdGenerator:
    return lambda: uuid.uuid4().hex


def get_clock() -> Clock:
    return datetime.now


class Container(DeclarativeContainer):
    config = Configuration()
    yasno = Singleton(get_yasno)
    console = Singleton(console, pretty=config.pretty)
    err_console = Singleton(err_console, pretty=config.pretty)
    id_generator = Singleton(get_id_generator)
    clock = Singleton(get_clock)


container = Container()
