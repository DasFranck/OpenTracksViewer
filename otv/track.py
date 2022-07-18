from datetime import datetime

from gpxpy.gpx import GPXTrack, GPXTrackPoint

from .point import Point

class Track:
    name: str
    activity: str
    points: list[Point]

    start_time: datetime
    end_time: datetime
    
    length_2d: float
    length_3d: float
    
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    
    uphill: float
    downhill: float

    moving_time: float
    stopped_time: float
    moving_distance: float
    stopped_distance: float
    max_speed: float

    def _get_points(self, gpx_points: list[GPXTrackPoint]) -> list[Point]:
        total_2d_distance = 0.
        total_3d_distance = 0.
        points = []
        for index, gpx_point in enumerate(gpx_points):
            points.append(Point(
                latitude=gpx_point.latitude,
                longitude=gpx_point.longitude,
                elevation=gpx_point.elevation,
                time=gpx_point.time,
                time_since_start=gpx_points[0].time - gpx_point.time,
                distance_2d=total_2d_distance,
                distance_3d=total_3d_distance
            ))
            total_2d_distance += gpx_point.distance_2d(gpx_points[index-1])
            total_3d_distance += gpx_point.distance_3d(gpx_points[index-1])
        return points

    def __init__(self, track_name: str, gpx_track: GPXTrack):
        self.name = track_name
        self.activity = gpx_track.type
        self.points = self._get_points(
            [point for segment in gpx_track.segments for point in segment.points]
        )
        time_bounds = gpx_track.get_time_bounds()
        self.start_time = time_bounds.start_time
        self.end_time = time_bounds.end_time
        bounds = gpx_track.get_bounds()
        self.min_latitude = bounds.min_latitude
        self.max_latitude = bounds.max_latitude
        self.min_longitude = bounds.min_longitude
        self.max_longitude = bounds.max_longitude
        uphill_downhill = gpx_track.get_uphill_downhill()
        self.uphill = uphill_downhill.uphill
        self.downhill = uphill_downhill.downhill
        self.length_2d = gpx_track.length_2d()
        self.length_3d = gpx_track.length_3d()
        moving_data = gpx_track.get_moving_data()
        self.moving_time = moving_data.moving_time
        self.stopped_time = moving_data.stopped_time
        self.moving_distance = moving_data.moving_distance
        self.stopped_distance = moving_data.stopped_distance
        self.max_speed = moving_data.max_speed

