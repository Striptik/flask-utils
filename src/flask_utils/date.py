from datetime import datetime

import pytz


def get_now_in_timezone(timezone="Europe/Paris"):
    return datetime.now(pytz.timezone(timezone))


def get_date_in_timezone(date, timezone="Europe/Paris"):
    return date.replace(tzinfo=pytz.timezone(timezone))
