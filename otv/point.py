from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float
    time: datetime
    time_since_start: timedelta
    distance_2d: float
    distance_3d: float