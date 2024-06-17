from datetime import datetime, timezone
from enum import IntEnum
from functools import wraps
from uuid import UUID


class CommitMode(IntEnum):
    """
    Commit modes for the managed db methods
    """

    NONE = 0
    FLUSH = 1
    COMMIT = 2
    ROLLBACK = 3


def menage_db_commit_method(auto_commit: CommitMode = CommitMode.FLUSH):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match auto_commit:
                case CommitMode.FLUSH:
                    await self.session.flush()
                case CommitMode.COMMIT:
                    await self.session.commit()
                case CommitMode.ROLLBACK:
                    await self.session.rollback()

            return result

        return wrapped_f

    return decorator


def utcnow() -> datetime:
    """Return the current utc date and time with tzinfo set to UTC."""
    return datetime.now(timezone.utc)


def timestamp_to_datetime(v: int) -> datetime:
    res = datetime.utcfromtimestamp(float(v))
    res = res.astimezone(timezone.utc)

    return res


def unaware_to_utc(d: datetime | None) -> datetime:
    """Set timezeno to UTC if datetime is unaware (tzinfo == None)."""
    if d and d.tzinfo is None:
        return d.replace(tzinfo=timezone.utc)
    return d


def is_uuid(input_string):
    try:
        uuid_obj = UUID(input_string)
    except ValueError:
        return False
    return True
