from datetime import datetime

import pytz
import dateutil.parser


def get_now_in_timezone(timezone="Europe/Paris"):
    return datetime.now(pytz.timezone(timezone))


def get_date_in_timezone(date, timezone="Europe/Paris"):
    return date.replace(tzinfo=pytz.timezone(timezone))


def get_start_and_end_of_today():
    return (
        datetime.now().replace(hour=0, minute=0),
        datetime.now().replace(hour=23, minute=59),
    )


def get_start_of_month():
    return datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_start_of_day(date):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def parse_date(date_string):
    if not date_string:
        return datetime.now()
    return dateutil.parser.isoparse(date_string)
