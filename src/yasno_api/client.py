import logging
from collections.abc import Callable
from typing import Any

import hishel
from httpx import Response
from pydantic import TypeAdapter

from yasno_api.schema import (
    City,
    House,
    Region,
    ScheduleComponent,
    ScheduleResponse,
    Street,
)

logger = logging.getLogger("yasno_api.client")

BASE_URL = "https://api.yasno.com.ua/api/v1"
SCHEDULE_URL = f"{BASE_URL}/pages/home/schedule-turn-off-electricity"
CITIES_URL = f"{BASE_URL}/electricity-outages-schedule/cities"
STREETS_URL = f"{BASE_URL}/electricity-outages-schedule/streets"
HOUSES_URL = f"{BASE_URL}/electricity-outages-schedule/houses"


def fetch_schedule() -> ScheduleComponent:
    validated_response = _fetch_schedule()
    return validated_response.schedule


def _fetch_schedule() -> ScheduleResponse:
    with hishel.CacheClient() as client:
        response = client.get(SCHEDULE_URL)

    valid_response = _validate_response(response, ScheduleResponse.model_validate)
    return valid_response


def fetch_cities(region: Region) -> list[City]:
    with hishel.CacheClient() as client:
        response = client.get(
            CITIES_URL,
            params=dict(region=region),
            extensions={"cache_disabled": True},
        )

    valid_response = _validate_response(
        response, TypeAdapter(list[City]).validate_python
    )
    return valid_response


def fetch_streets(region: Region, city_id: int) -> list[Street]:
    with hishel.CacheClient() as client:
        response = client.get(
            STREETS_URL,
            params=dict(region=region, city_id=city_id),
            extensions={"cache_disabled": True},
        )

    valid_response = _validate_response(
        response, TypeAdapter(list[Street]).validate_python
    )
    return valid_response


def fetch_houses(region: Region, street_id: int) -> list[House]:
    with hishel.CacheClient() as client:
        response = client.get(
            HOUSES_URL,
            params=dict(region=region, street_id=street_id),
            extensions={"cache_disabled": True},
        )

    valid_response = _validate_response(
        response, TypeAdapter(list[House]).validate_python
    )
    return valid_response


def _validate_response[T](response: Response, validator: Callable[[Any], T]) -> T:
    logger.info(f"{response.url=}:{response.extensions.get('from_cache')=}")
    response.raise_for_status()
    response_json = response.json()
    validated_response = validator(response_json)
    return validated_response
