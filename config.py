import logging
import pytz

from classes.TileLayer import TileLayer


class UserConfig:
    """
    This is where you can edit OTV Behaviour
    """
    # Timezone used by OTV for date processing
    TIMEZONE = pytz.timezone("Europe/Paris")

    # Default Tile Layer to be used by Leaflet Maps
    DEFAULT_TILE_LAYER = TileLayer.CYCLE

    DEFAULT_LOGGING_LEVEL = logging.INFO