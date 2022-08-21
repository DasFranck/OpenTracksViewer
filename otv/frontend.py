import calendar
import logging
from pprint import pprint
import random

from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Any, Optional

from flask import Blueprint, render_template, current_app

from classes.TileLayer import TileLayer
from otv.track import Track

frontend = Blueprint("frontend", __name__)


@frontend.app_template_global()
def get_monthly_report_list() -> dict[str, set[str]]:
    """
    Output dict with year as key and set of months as value
    """
    monthly_reports: dict[str, set[str]] = {}

    for track in current_app.config["tracks"].values():
        if (year := track.start_time.year) in monthly_reports:
            monthly_reports[year].add(track.start_time.month)
        else:
            monthly_reports[year] = {track.start_time.month}
    return monthly_reports

@frontend.app_template_global()
def get_all_points(activity: str = None, year: int = None, month: int = None, day: int = None) -> list[tuple[float, float]]:
    """
    Get all points, useful for heatmaps
    Can filter by activity, year and/or month
    """
    all_points = []
    for track in current_app.config["tracks"].values():
        if ((not activity or track.activity == activity) and
            (not year and track.start_time.year != year) and
            (not month or track.start_time.month != month) and
            (not day or track.start_time.day != day)):
            all_points += [(point.latitude, point.longitude) for point in track.points]
    return all_points

def get_all_tracks(activity: str = None, year: int = 0, month: int = 0, day: int = 0) -> list[Track]:
    all_tracks = []
    for track in current_app.config["tracks"].values():
        if ((not activity or track.activity == activity) and
            (not year or track.start_time.year == year) and
            (not month or track.start_time.month == month) and
            (not day or track.start_time.day == day)):
            all_tracks.append(track)
    return all_tracks

@frontend.app_template_global()
def get_activity_list(tracks: Optional[list[Track]|dict[Any, Track]] = None) -> set[str]:
    if tracks == None:
        tracks = current_app.config["tracks"]
    if isinstance(tracks, dict):
        return {track.activity for track in tracks.values() if track.activity}
    elif isinstance(tracks, list):
        return {track.activity for track in tracks if track.activity}
    else:
        raise TypeError("get_activity_list only takes list of Track or dict with Track as a value")


@frontend.app_template_filter()
def get_month_name(month_number: int) -> str:
    return calendar.month_name[month_number]

@frontend.app_template_filter()
def get_activity_emoji(activity_name: str, with_text: bool = False) -> str:
    match activity_name.lower():
        case "biking":
            emoji = "🚴"
        case "kayaking":
            emoji = "🚣"
        case "walking":
            emoji = "🚶"
        case "jogging":
            emoji = "🏃"
        case _:
            emoji = ""
    return f"{activity_name.capitalize() + ' ' if with_text else ''}{emoji}"

@frontend.app_template_filter()
def get_activity_color(activity_name: str) -> str:
    match activity_name.lower():
        case "biking":
            return "#fff859"
        case "kayaking":
            return "#ffa559"
        case "walking":
            return "#a559ff"
        case "jogging":
            return "#59b3ff"
        case _:
            return f"#{''.join([random.choice('0123456789ABCDEF') for j in range(6)])}"

@frontend.app_template_filter()
def format_duration(duration: int) -> str:
    hours = duration // 3600
    minutes = duration % 3600 // 60
    seconds = duration % 60
    return f"{hours}h {minutes:02}m {seconds:02}s"

@frontend.app_template_filter()
def format_datetime(input_datetime: datetime) -> str:
    return(input_datetime.strftime("%Y-%m-%d %H:%M:%S")) #Careful UTC


@frontend.route("/track/<string:track_id>")
def track_page(track_id: str) -> str:
    track: Track = current_app.config["tracks"][track_id]
    pprint(current_app.config)
    return(render_template("track.html.j2",
           track=track,
           default_tile_layer=current_app.config["DEFAULT_TILE_LAYER"],
           tile_layers=TileLayer,
           polyline_points=[[point.latitude, point.longitude] for point in track.points],
           elevation_list=[[point.distance_2d, point.elevation] for point in track.points]
    ))

@frontend.route("/activity/<string:activity>")
def activity_page(activity: str) -> str:
    return(render_template("activity.html.j2",
        activity=activity
    ))

@frontend.route("/report/<int:year>")
def report_year_page(year: int) -> str:
    tracks = get_all_tracks(year=year)
    return(render_template("periodic_report.html.j2",
        year=year,
        activities=get_activity_list(tracks),
        tracks=tracks,
        periods_label=[f"{month:02}/{year}" for month in range(1, 13)],
        periods=[(
            datetime(year, month, 1, tzinfo=current_app.config["TIMEZONE"]),
            (datetime(year, month, 1, tzinfo=current_app.config["TIMEZONE"]) + relativedelta(months=+1)) - relativedelta(microseconds=+1)
            )
            for month in range(1, 13)
        ]
    ))

@frontend.route("/report/<int:year>/<int:month>")
def report_month_page(year: int, month: int) -> str:
    day_list = range(1, calendar.monthrange(year, month)[1] + 1)
    tracks = get_all_tracks(year=year, month=month)
    return(render_template("periodic_report.html.j2",
        year=year,
        month=month,
        activities=get_activity_list(tracks),
        tracks=tracks,
        periods_label=[f"{day:02}/{month:02}" for day in day_list],
        periods=[(
            datetime(year, month, day, tzinfo=current_app.config["TIMEZONE"]),
            (datetime(year, month, day, tzinfo=current_app.config["TIMEZONE"]) + relativedelta(days=+1)) - relativedelta(microseconds=+1)
            )
            for day in day_list
        ]
    ))

@frontend.route("/report/<int:year>/<int:month>/<int:day>")
def report_day_page(year: int, month: int, day: int) -> str:
    tracks = get_all_tracks(year=year, month=month, day=day)
    return(render_template("periodic_report.html.j2",
        year=year,
        month=month,
        day=day,
        activities=get_activity_list(tracks),
        tracks=tracks,
    ))

@frontend.route("/")
def index_page() -> str:
    return(render_template(
        "index.html.j2",
        tracks=current_app.config["tracks"])
    )
