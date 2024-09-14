from datetime import datetime, timezone

from tgbot.config import config


def convert_utc_datetime(utc_datetime: datetime):
    return (
        utc_datetime.replace(tzinfo=timezone.utc)
        .astimezone(config.misc.yekaterinburg_timezone)
        .strftime("%m/%d/%Y %H:%M:%S")
    )
