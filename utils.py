import datetime
from datetime import date


def convert_time_str_to_time(hh, mm):
    return datetime.datetime(hour=hh, minute=mm)


def convert_str_to_time(time_str: str) -> datetime.time:
    [hh, mm] = time_str.split(":")
    return datetime.time(hour=int(hh), minute=int(mm))


def subtract_times(start: datetime.time, end: datetime.time) -> int:
    return 60 * (end.hour - start.hour) + end.minute - start.minute
