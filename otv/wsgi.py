import os

from pathlib import Path

import gpxpy

from flask import Flask

from .frontend import frontend
from .classes.track import Track


def load_gpxs(gpx_folder_path: str) -> dict[str, Track]:
    """Load GPX recursively from path and return them as a dict, key is filename-index."""
    tracks = {}
    for gpx_file_path in Path(gpx_folder_path).expanduser().resolve().glob("*.gpx"):
        with open(gpx_file_path, encoding="utf8") as gpx_file:
            for index, track in enumerate(gpxpy.parse(gpx_file).tracks):
                if track.length_3d():
                    tracks[f"{gpx_file_path.name}-{index}"] = Track(
                        f"{gpx_file_path.name}-{index}", track
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

