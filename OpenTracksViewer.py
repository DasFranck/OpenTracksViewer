#!/usr/bin/env python3

import argparse
import os

import gpxpy

from flask import Flask

from otv.frontend import frontend
from otv.track import Track


def load_gpxs(gpxs_path: str) -> dict[str, Track]:
    tracks = {}
    for dirpath, _, filenames in os.walk(gpxs_path):
        for filename in filenames:
            if filename.endswith(".gpx"):
                with open(os.path.join(dirpath, filename)) as fd:
                    for index, track in enumerate(gpxpy.parse(fd).tracks):
                        if track.length_3d():
                            tracks[f"{os.path.splitext(filename)[0]}-{index}"] = Track(
                                f"{os.path.splitext(filename)[0]}-{index}",
                                track
                            )
    return tracks

def load_config(app: Flask, args: argparse.Namespace):
    app.config.from_object(args.config)
    if args.log_level:
        app.logger.setLevel(args.log_level.upper())
    else:
        app.logger.setLevel(app.config["DEFAULT_LOGGING_LEVEL"])
    app.logger.info("Config loaded")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gpxs_path")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--config", type=str, default="config.UserConfig", help="Config's object path")
    parser.add_argument("--log-level", type=str.capitalize, default=None, choices=["Critical", "Error", "Warning", "Info", "Debug", "NotSet"])

    args = parser.parse_args()

    app = Flask(__name__)
    load_config(app, args)
    app.config["tracks"] = load_gpxs(args.gpxs_path)
    app.logger.info("%d tracks loaded", len(app.config["tracks"]))
    app.register_blueprint(frontend)
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
