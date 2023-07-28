import os

import gpxpy

from flask import Flask

from .frontend import frontend
from .classes.track import Track


def load_gpxs(gpxs_path: str) -> dict[str, Track]:
    """Load GPX recursively from path and return them as a dict, key is filename-index."""
    tracks = {}
    for dirpath, _, filenames in os.walk(gpxs_path):
        for filename in filenames:
            if filename.endswith(".gpx"):
                with open(os.path.join(dirpath, filename), encoding="utf8") as gpx_file:
                    for index, track in enumerate(gpxpy.parse(gpx_file).tracks):
                        if track.length_3d():
                            tracks[f"{os.path.splitext(filename)[0]}-{index}"] = Track(
                                f"{os.path.splitext(filename)[0]}-{index}", track
                            )
    return tracks


def load_config(app: Flask):
    """Load config python file, path specified by args.config."""
    app.config.from_object(os.environ.get("OTV_CONFIG", "config.UserConfig"))
    app.logger.setLevel(os.environ.get("OTV_LOG_LEVEL", "info").upper())
    app.logger.info("Config loaded")


def create_app() -> Flask:
    app = Flask(__name__)
    load_config(app)
    if (gpx_files_path := os.environ.get("OTV_TRACKS_FOLDER_PATH", None)) is not None:
        app.config["tracks"] = load_gpxs(gpx_files_path)
    elif (gpx_files_path := app.config.get("TRACKS_FOLDER_PATH", None)) is not None:
        app.config["tracks"] = load_gpxs(gpx_files_path)
    else:
        raise ValueError("No GPX Path provided")
    app.logger.info("%d tracks loaded", len(app.config["tracks"]))
    app.register_blueprint(frontend)
    return app