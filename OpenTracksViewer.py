#!/usr/bin/env python3

import argparse
import os
import pytz

import gpxpy

from flask import Flask
from gpxpy.gpx import GPXTrack

from otv import config
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gpxs_path")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app = Flask(__name__)
    app.config["tracks"] = load_gpxs(args.gpxs_path)
    app.config["timezone"] = pytz.timezone(config.timezone)
    print(app.config["tracks"])
    app.register_blueprint(frontend)
    app.run(port=args.port)


if __name__ == "__main__":
    main()
