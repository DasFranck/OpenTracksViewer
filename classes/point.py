"""Includes Point dataclass."""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Point:
    """Dataclass representing a GPX point."""
    latitude: float
    longitude: float
    elevation: float | None
    time: datetime | None
    time_since_start: timedelta | None
    distance_2d: float
    distance_3d: float
