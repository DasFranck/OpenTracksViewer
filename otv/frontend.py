from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app

frontend = Blueprint("frontend", __name__)

@frontend.app_template_filter()
def format_duration(duration: int):
    hours = duration // 3600
    minutes = duration % 3600 // 60
    seconds = duration % 60
    return f"{hours}h {minutes:02}m {seconds:02}s"

@frontend.app_template_filter()
def format_datetime(input_datetime: datetime):
    return(input_datetime.strftime("%Y-%m-%d %H:%M:%S"))

@frontend.route("/track/<string:track_id>")
def track_page(track_id: str):
    return(render_template("track.j2", track=current_app.config["tracks"][track_id]))

@frontend.route("/")
def index_page():
    return(render_template("index.j2", tracks=current_app.config["tracks"]))