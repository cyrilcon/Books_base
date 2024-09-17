from datetime import datetime, timezone, timedelta


def convert_utc_datetime(utc_datetime: datetime):
    return (
        utc_datetime.replace(tzinfo=timezone.utc)
        .astimezone(timezone(timedelta(hours=5)))
        .strftime("%m/%d/%Y %H:%M:%S")
    )
