from datetime import datetime, timezone, timedelta


def is_past(dt: datetime) -> bool:
    """
    Checks if the given datetime is in the past compared to the current UTC time.

    Args:
        dt (datetime): The datetime to be checked.

    Returns:
        bool: True if the datetime is in the past, False otherwise.
    """
    return dt < datetime.now(timezone.utc)


def is_recent(dt: datetime, delta_minutes: int = 10) -> bool:
    """
    Checks if the given datetime is within the recent past defined by delta_minutes.

    Args:
        dt (datetime): The datetime to be checked.
        delta_minutes (int, optional): The time window in minutes to consider as recent. Defaults to 10.

    Returns:
        bool: True if the datetime is within the recent past, False otherwise.

    Raises:
        TypeError: If dt is not a datetime instance or delta_minutes is not an integer.
        ValueError: If delta_minutes is not a positive integer or if dt is not timezone-aware.
    """

    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime.datetime instance")
    if not isinstance(delta_minutes, int):
        raise TypeError("delta_minutes must be an integer")
    if delta_minutes <= 0:
        raise ValueError("delta_minutes must be a positive integer")

    if dt.tzinfo is None:
        raise ValueError("dt must be timezone-aware")

    return abs(dt - datetime.now(timezone.utc)) <= timedelta(minutes=delta_minutes)
