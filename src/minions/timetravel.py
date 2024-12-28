from datetime import datetime, time, timedelta, timezone


def dt_utc_to_local(utc_dt: datetime) -> datetime:
    ensure_utc = utc_dt.replace(tzinfo=timezone.utc)
    tz = local_tz()
    local_dt = ensure_utc.astimezone(tz)
    return local_dt


def local_tz():
    return datetime.now().astimezone().tzinfo


def hours_as_time(v: float | int) -> time:
    dt = datetime.fromtimestamp(0, tz=timezone.utc) + timedelta(hours=v)
    ret = dt.time()
    return ret
