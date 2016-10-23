from datetime import timedelta, date
from czech_holidays import holidays
import calendar


def daterange(start_date, end_date):
    """Return generator yielding each day in range."""
    date = start_date
    yield date
    while date < end_date:
        date = date + timedelta(days=1)
        yield date


def is_weekend(datetime):
    """True if given day is weekend day."""
    return datetime.weekday() == 5 or datetime.weekday() == 6


def is_holiday(datetime):
    """True if given day is holiday in Czech republic."""
    return datetime in holidays


def is_workday(datetime):
    """True if given day is work day in Czech republic."""
    return not is_holiday(datetime) and not is_weekend(datetime)


def get_quota_work_hours(year, month, hours_per_day):
    """Return quota hours for given year and month - enter work hours_per_day."""
    start_date = date(year, month, 1)
    dummy, last_day = calendar.monthrange(year, month)
    end_date = date(year, month, last_day)
    dates = daterange(start_date, end_date)
    return sum(hours_per_day for d in dates if is_workday(d))
