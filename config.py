"""Configuration file for OTV."""

import logging

from dataclasses import dataclass

import pytz

from classes.tile_layer import TileLayer


@dataclass
class UserConfig:
    """This is where you can edit OTV Behaviour."""

    DEFAULT_LOGGING_LEVEL = logging.INFO

    HOST = "127.0.0.1"
    PORT = 5000

    # Timezone used by OTV for date processing
    TIMEZONE = pytz.timezone("Europe/Paris")

    # Default Tile Layer to be used by Leaflet Maps
    DEFAULT_TILE_LAYER = "Cycle"

    TILE_LAYERS = {
        "Normal": TileLayer(
            "https://{s}.tile.osm.org/{z}/{x}/{y}.png",
            "OpenStreetMap",
        ),
        "Cycle": TileLayer(
            "https://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png",
            "Thunderforest and OpenStreetMap contributors",
        ),
        "Outdoors": TileLayer(
            "https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png",
            "Thunderforest and OpenStreetMap contributors",
        ),
        "Sattelite": TileLayer(
            "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "Esri, Maxar, Earthstar Geographics, and the GIS User Community",
        ),
    }
