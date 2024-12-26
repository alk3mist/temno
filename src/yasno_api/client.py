import hishel
from model import ScheduleComponent, ScheduleResponse

SCHEDULE_URL = (
    "https://api.yasno.com.ua/api/v1/pages/home/schedule-turn-off-electricity"
)


def fetch_schedule() -> ScheduleComponent:
    with hishel.CacheClient() as client:
        response = client.get(SCHEDULE_URL)
    response.raise_for_status()
    response_json = response.json()
    return ScheduleResponse.model_validate(response_json).schedule


if __name__ == "__main__":
    schedule = fetch_schedule()
    print(f"updated at: {schedule.updated_at}")
    dnipro = schedule.daily_schedule["dnipro"]
    print(f"today: {dnipro.today.title}")
    print("and")
    if dnipro.tomorrow:
        print(f"tomorrow: {dnipro.tomorrow.title}")
    else:
        print("no tomorrow(")
