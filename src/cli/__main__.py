from rich import print

from cli import render
from yasno_api import yasno

if __name__ == "__main__":
    # import logging

    # logging.basicConfig(level=logging.INFO)

    schedule = yasno.fetch_schedule()
    print(render.schedule_component(schedule, region="dnipro", group="2.1"))
