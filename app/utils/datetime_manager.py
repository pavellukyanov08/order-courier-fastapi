from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class DateTimeManager:
    @staticmethod
    def get_now_utc() -> datetime:
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def get_now_in_timezone(*, tz: str) -> datetime:
        try:
            return datetime.now(ZoneInfo(key=tz))
        except Exception as e:
            raise ValueError(f"Incorrect timezone: {tz}") from e

    @staticmethod
    def convert_to_utc(*, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(tz=timezone.utc)
