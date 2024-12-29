import pytest

from yasno_api import yasno


@pytest.mark.vcr
def test_fetch_is_ok():
    yasno.fetch_schedule()


@pytest.mark.vcr
def test_fetch_without_current_schedule_is_ok():
    yasno.fetch_schedule()


@pytest.mark.vcr
def test_fetch_cities_is_ok():
    yasno.fetch_cities("dnipro")


@pytest.mark.vcr
def test_fetch_streets_is_ok():
    CITY_ID = 5
    yasno.fetch_streets("dnipro", CITY_ID)


@pytest.mark.vcr
def test_fetch_houses_is_ok():
    STREET_ID = 2060
    yasno.fetch_houses("dnipro", STREET_ID)
