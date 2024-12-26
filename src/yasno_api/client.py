import hishel

from yasno_api.schema import ScheduleComponent, ScheduleResponse

SCHEDULE_URL = (
    "https://api.yasno.com.ua/api/v1/pages/home/schedule-turn-off-electricity"
)


def _fetch_all():
    with hishel.CacheClient() as client:
        response = client.get(SCHEDULE_URL)
    response.raise_for_status()
    response_json = response.json()
    validated_response = ScheduleResponse.model_validate(response_json)
    return validated_response


def fetch_schedule() -> ScheduleComponent:
    validated_response = _fetch_all()
    return validated_response.schedule
