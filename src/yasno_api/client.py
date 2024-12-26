import httpx
from model import ScheduleResponse

SCHEDULE_URL = (
    "https://api.yasno.com.ua/api/v1/pages/home/schedule-turn-off-electricity"
)


def fetch_schedule() -> ScheduleResponse:
    response = httpx.get(SCHEDULE_URL)
    response.raise_for_status()
    response_json = response.json()
    return ScheduleResponse.model_validate(response_json)


if __name__ == "__main__":
    print(fetch_schedule())
