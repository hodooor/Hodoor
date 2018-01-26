from datetime import timedelta, date, datetime
from czech_holidays import Holidays
import calendar


def daterange(start_date, end_date):
    """Generator yielding each day in range."""
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
    return datetime in Holidays(datetime.year)


def is_workday(datetime):
    """True if given day is work day in Czech republic."""
    return not is_holiday(datetime) and not is_weekend(datetime)


def get_quota_work_hours(year, month, hours_per_day):
    """Return quota hours for given year and month - enter work hours_per_day."""
    return get_number_of_work_days(year, month) * hours_per_day


def get_number_of_work_days(year, month, last_day=None):
    """
    Return number of days in given year and month.

    If last_day is not specified, last date of the month will be used.
    """
    start_date = date(year, month, 1)
    if not last_day:
        dummy, last_day = calendar.monthrange(year, month)
    end_date = date(year, month, last_day)
    dates = daterange(start_date, end_date)
    return sum(1 for d in dates if is_workday(d))


def get_num_of_elapsed_workdays_in_month(date):
    """
    Return number of elapsed work days this month
    
    This number should be same as number number_of_workdays if today is not
    work day. If today is work day, it should be decremented by one.
    
    """
    number_of_workdays = get_number_of_work_days(date.year, date.month, date.day)
    if is_workday(date):
        return number_of_workdays - 1
    else:
        return number_of_workdays
        

def last_month(this_month=datetime.now().month):
	"""
	Return previus month
	
	When It's January return December last year.
	
	"""
	if 0 < this_month <= 12:
		if this_month == 1:
			return 12
		else:
			return this_month-1
	else: 
		raise ValueError("Number of month does not exist")

def daily_hours(hours):
    """ 
    Return number of hours in range from 0 to 24
     """
    if hours > 24:
        return 24
    elif hours < 0:
        return 0
    else:
        return hours
