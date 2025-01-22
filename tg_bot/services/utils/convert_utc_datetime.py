from datetime import datetime, timezone

from config import config


def convert_utc_datetime(utc_datetime: datetime) -> str:
    """
    Converts UTC time to local time, according to the numeric offset (timezone) from the configuration.

    :param utc_datetime: Date and time in UTC
    :type utc_datetime: datetime
    :return: Date and time in local timezone in string format
    """

    return (
        utc_datetime.replace(tzinfo=timezone.utc)
        .astimezone(config.timezone)
        .strftime("%m/%d/%Y %I:%M:%S %p")
    )
