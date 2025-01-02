from dataclasses import dataclass, field
from typing import Any

import pytest
from typer.testing import CliRunner

from temno.bootstrap import container
from temno.cli import app
from temno.views import YasnoAPI
from yasno_api.schema import City, House, Region, ScheduleComponent, Street

runner = CliRunner()


@dataclass
class DummyAPI(YasnoAPI):
    schedule: ScheduleComponent
    cities: list[City] = field(default_factory=list)
    streets: list[Street] = field(default_factory=list)
    houses: list[House] = field(default_factory=list)

    def fetch_schedule(self) -> ScheduleComponent:
        return self.schedule

    def fetch_cities(self, region: Region) -> list[City]:
        return self.cities

    def fetch_streets(self, region: Region, city_id: int) -> list[Street]:
        return self.streets

    def fetch_houses(self, region: Region, street_id: int) -> list[House]:
        return self.houses


@pytest.fixture
def schedule() -> ScheduleComponent:
    current: dict[str, Any] = {
        "dnipro": {
            "today": {
                "title": "today",
                "groups": {
                    "1.1": [],
                    "1.2": [{"start": 8, "end": 12.5, "type": "DEFINITE_OUTAGE"}],
                },
            }
        }
    }
    return ScheduleComponent.model_validate({"dailySchedule": current})


@pytest.mark.parametrize(
    "args,code,output",
    [
        (("dnipro", "1.1", "today"), 0, "\n\n"),
        (("dnipro", "1.2", "today"), 0, "\n08:00 - 12:30\n"),
        (("dnipro", "1.1", "tomorrow"), 1, "Schedule for the day not found\n\n"),
        (("kyiv", "1.1", "today"), 1, "Schedule for the region not found\n\n"),
    ],
)
@pytest.mark.vcr
def test_schedule(
    args: tuple[str, ...],
    code: int,
    output: str,
    schedule: ScheduleComponent,
):
    dummy_api = DummyAPI(schedule)
    with container.override.service(YasnoAPI, dummy_api):
        result = runner.invoke(app, ["schedule", *args])

    assert result.exit_code == code, result.output
    assert result.stdout == output
