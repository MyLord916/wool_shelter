from datetime import datetime


def str_to_date(str_date: str) -> datetime:
    pattern = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(str_date, pattern)


def date_to_str(date: datetime) -> str:
    pattern = "%Y-%m-%d %H:%M:%S"
    return date.strftime(pattern)
