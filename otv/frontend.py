import os

from flask import Blueprint, render_template, flash, redirect, url_for, g, current_app

frontend = Blueprint("frontend", __name__)

@frontend.route("/track/<string:track_id>")
def track_page(track_id: str):
    return(render_template("track.j2", track=current_app.config["tracks"][track_id]))

@frontend.route("/")
def index_page():
    return(render_template("index.j2", tracks=current_app.config["tracks"]))