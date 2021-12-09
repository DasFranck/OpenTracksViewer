import argparse
import os

from typing import List

import gpxpy

from flask import Flask
from gpxpy.gpx import GPXTrack

from otv.frontend import frontend

def load_tracks(tracks_path: str) -> List[GPXTrack]:
    tracks = {}
    for dirpath, _, filenames in os.walk(tracks_path):
        for filename in filenames:
            if filename.endswith(".gpx"):
                with open(os.path.join(dirpath, filename)) as fd:
                    tracks[os.path.splitext(filename)[0]] = gpxpy.parse(fd)
    return tracks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tracks_path")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app = Flask(__name__)
    app.config["tracks"] = load_tracks(args.tracks_path)
    print(app.config["tracks"])
    app.register_blueprint(frontend)
    app.run(port=args.port)


if __name__ == "__main__":
    main()