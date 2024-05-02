from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current utc date and time with tzinfo set to UTC."""
    return datetime.now(timezone.utc)


def unaware_to_utc(d: datetime | None) -> datetime:
    """Set timezeno to UTC if datetime is unaware (tzinfo == None)."""
    if d and d.tzinfo is None:
        return d.replace(tzinfo=timezone.utc)
    return d
