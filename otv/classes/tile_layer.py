"""Includes Tile Layer Enum."""

from dataclasses import dataclass


@dataclass
class TileLayer:
    generic_tile_format: str
    attribution: str
    api_key: str | None = None
