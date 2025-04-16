"""Implements the Plugin pattern for DI"""

import sys
import uuid
from dataclasses import dataclass
from datetime import datetime

from rich.console import Console
from wireup import create_sync_container, service

from temno.calendar import Clock, IDGenerator
from temno.views import YasnoAPI
from yasno_api import client


@service
def get_yasno() -> YasnoAPI:
    return client


@dataclass
class Config:
    pretty: bool


@service
def config() -> Config:
    return Config(pretty=False)


@service
def console(config: Config) -> Console:
    return Console(
        no_color=not config.pretty,
        highlight=config.pretty,
    )


@service(qualifier="error")
def err_console(config: Config) -> Console:
    return Console(
        stderr=True,
        style="bold red",
        no_color=not config.pretty,
        highlight=config.pretty,
    )


@service
def get_id_generator() -> IDGenerator:
    return lambda: uuid.uuid4().hex


@service
def get_clock() -> Clock:
    return datetime.now


container = create_sync_container(service_modules=[sys.modules[__name__]])
