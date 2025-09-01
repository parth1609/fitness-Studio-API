"""Timezone utilities for IST normalization and validation.

Utilities ensure class times are stored in IST (Asia/Kolkata) and make simple
comparisons for future/past checks.

Design decisions
----------------
- If an input datetime is naive (no tzinfo), we assume it is already in IST.
  This prevents unintentional shifting and aligns with local expectations.
- If an input datetime is timezone-aware, we convert it to IST.
"""
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def now_ist() -> datetime:
    """Return the current time in IST."""
    return datetime.now(tz=IST)


def normalize_to_ist(dt: datetime) -> datetime:
    """Return ``dt`` as a timezone-aware IST datetime.

    - If ``dt`` is naive, assume it's IST and attach the IST tzinfo.
    - If ``dt`` is aware, convert to IST.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=IST)
    return dt.astimezone(IST)


def is_past_in_ist(dt: datetime) -> bool:
    """Return True if the given IST datetime is in the past relative to IST now.

    The input should be timezone-aware in IST. Call ``normalize_to_ist`` first
    if you are uncertain.
    """
    current = now_ist()
    return dt < current
