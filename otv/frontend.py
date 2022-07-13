import logging

from calendar import month_name
from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app
from gpxpy.gpx import GPXTrackPoint, GPX

frontend = Blueprint("frontend", __name__)


@frontend.app_template_global()
def get_monthly_report_name() -> dict[str, set[str]]:
    monthly_reports = {}

    for track in current_app.config["tracks"].values():
        if (start := track.get_time_bounds()[0]):
            if (year := start.date().year) in monthly_reports:
                monthly_reports[year].add(start.date().month)
            else:
                monthly_reports[year] = {start.date().month}
        else:
            logging.info("Track %s has no start date, it may be empty", track.name)
    return monthly_reports

@frontend.app_template_global()
def get_all_gpx_points(activity: str = "", year: int = 0, month: int = 0) -> list[GPXTrackPoint]:
    """
    Get all points.
    Can filter by activity, year and/or month
    """
    all_points = []
    for track in current_app.config["tracks"].values():
        track: GPX
        if activity and track.tracks[0].type != activity:
            continue
        if year and track.get_time_bounds().start_time.year != year:
            continue
        if month and track.get_time_bounds().start_time.month != month:
            continue
        all_points += [[point_data.point.latitude, point_data.point.longitude] for point_data in track.get_points_data()]
    return all_points

@frontend.app_template_global()
def get_activity_list() -> set[str]:
    return {track.tracks[0].type for track in current_app.config["tracks"].values()}

@frontend.app_template_filter()
def get_month_name(month_number: int) -> str:
    return month_name[month_number]

@frontend.app_template_filter()
def get_activity_emoji(activity_name: str, with_text: bool = False) -> str:
    match activity_name.lower():
        case "biking":
            emoji = "🚴"
        case "kayaking":
            emoji = "🚣"
        case "walking":
            emoji = "🚶"
        case _:
            emoji = ""
    return f"{activity_name.capitalize() + ' ' if with_text else ''}{emoji}"

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
    track = current_app.config["tracks"][track_id]
    return(render_template("track.html.j2",
           track=track,
           polyline_points=[[point.point.latitude, point.point.longitude] for point in track.get_points_data()],
           elevation_list=[[point.distance_from_start, point.point.elevation] for point in track.get_points_data()]
    ))

@frontend.route("/activity/<string:activity>")
def activity_page(activity: str) -> str:
    return(render_template("activity.html.j2",
        activity=activity
    ))

@frontend.route("/report/<int:year>")
def report_year_page(year: int) -> str:
    return(render_template("report_year.html.j2",
    ))

@frontend.route("/report/<int:year>/<int:month>")
def report_month_page(year: int, month: int) -> str:
    return(render_template("report_month.html.j2",
    ))

@frontend.route("/report/<int:year>/<int:month>/<int:day>")
def report_day_page(year: int, month: int, day: int) -> str:
    return(render_template("report_day.html.j2",
    ))

@frontend.route("/")
def index_page() -> str:
    return(render_template("index.html.j2", tracks=current_app.config["tracks"]))
