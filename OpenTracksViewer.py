#!/usr/bin/env python3

"""Main OTV file."""

import argparse
import logging
import os

import gpxpy

from flask import Flask

def main():
    """Parse arguments and runs OTV flask app."""
    parser = argparse.ArgumentParser()
    parser.add_argument("gpxs_path")
    parser.add_argument(
        "--host",
        type=str,
        default=None
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.UserConfig",
        help="Config's object path"
    )
    parser.add_argument(
        "--log-level",
        type=str.capitalize,
        default=None,
        choices=["Critical", "Error", "Warning", "Info", "Debug", "NotSet"]
    )

    args = parser.parse_args()




if __name__ == "__main__":
    main()
