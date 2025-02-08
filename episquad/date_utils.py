from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar

tz_utc0 = ZoneInfo('UTC')
tz_france = ZoneInfo('Europe/Paris')

def get_number_of_days_of_date_month(which_date):
    return calendar.monthrange(which_date.year, which_date.month)[1]

def parse_day(day):
    if day == 'today':
        return (True, now())
    elif day == 'tomorrow':
        return (True, now() + timedelta(days=1))
    elif day.isdigit():
        day = int(day)

        if day <= 0 or day > get_number_of_days_of_date_month(now()):
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

def str_readable(which_date):
    return which_date.strftime("%A %d %B %Hh%M")

def parse(str, micro=False, convert=False):
    parsed = datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%fZ" if micro else "%Y-%m-%dT%H:%M:%SZ",)

    if convert:
        parsed = parsed.replace(tzinfo=tz_utc0)

    return parsed if not convert else parsed.astimezone(tz_france)

def get_week_first_and_last_day(which_date):
    last_sun = last_sunday().replace(hour=23, minute=0, second=0, microsecond=0)
    next_sun = (last_sun + timedelta(days=7)).replace(hour=22, minute=59, second=59, microsecond=999000)

    return last_sun, next_sun

def get_month_first_and_last_day(which_date):
    n_days = get_number_of_days_of_date_month(which_date)

    first_day = datetime(which_date.year, which_date.month, 1).replace(hour=23, minute=0, second=0, microsecond=0)
    last_day = datetime(which_date.year, which_date.month, n_days).replace(hour=22, minute=59, second=59, microsecond=999000)

    return first_day, last_day

def get_current_week_first_and_last_day():
    return get_week_first_and_last_day(now())

def get_next_week_first_and_last_day():
    return get_week_first_and_last_day(now() + timedelta(days=7))

def get_current_month_first_and_last_day():
    return get_month_first_and_last_day(now())    
