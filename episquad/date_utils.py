from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar

tz_utc0 = ZoneInfo('UTC')
tz_france = ZoneInfo('Europe/Paris')

def parse_day(day):
    if day == 'today':
        return (True, now())
    elif day == 'tomorrow':
        return (True, now() + timedelta(days=1))
    elif day.isdigit():
        day = int(day)

        if day <= 0 or day > calendar.monthrange(now().year, now().month)[1]:
            return (False, None)

        return (True, now().replace(day=day))

    return (False, None)

def now():
    return datetime.utcnow()

def last_day(offset):
    today = now()
    days_since = (today.weekday() + offset) % 7
    return today - timedelta(days=days_since)

def last_monday():
    return last_day(0)

def last_sunday():
    return last_day(1)

def str(which_date, micro=False):
    return which_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ" if micro else "%Y-%m-%dT%H:%M:%SZ")

def parse(str, micro=False, convert=False):
    parsed = datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ" if micro else "%Y-%m-%dT%H:%M:%SZ",)

    if convert:
        parsed = parsed.replace(tzinfo=tz_utc0)

    return parsed if not convert else parsed.astimezone(tz_france)

def get_week_first_and_last_day(which_date):
    last_sun = last_sunday().replace(hour=23, minute=0, second=0, microsecond=0)
    next_sun = (last_sun + timedelta(days=7)).replace(hour=22, minute=59, second=59, microsecond=999000)

    return last_sun, next_sun

def get_current_week_first_and_last_day():
    return get_week_first_and_last_day(now())

def get_next_week_first_and_last_day():
    return get_week_first_and_last_day(now() + timedelta(days=7))
