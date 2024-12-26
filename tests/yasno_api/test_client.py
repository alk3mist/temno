import pytest

from yasno_api import yasno


@pytest.mark.vcr
def test_fetch_is_ok():
    yasno.fetch_schedule()
