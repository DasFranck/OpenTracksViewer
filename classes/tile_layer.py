from enum import Enum


class TileLayer(Enum):
    NORMAL = (
        "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
        "OpenStreetMap"
    )
    CYCLE = (
        "http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png",
        "Thunderforest and OpenStreetMap contributors",
    )
    SATELLITE = (
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "Esri, Maxar, Earthstar Geographics, and the GIS User Community",
    )
