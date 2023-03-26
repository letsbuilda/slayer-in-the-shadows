"""Utilities for loading assets"""

from importlib.abc import Traversable
from importlib.resources import files


def get_asset_path(*paths: str) -> Traversable:
    """Gets the path for an asset"""
    file_path = files("pyweek-2023-03").joinpath("assets")
    for path in paths:
        file_path = file_path.joinpath(path)
    return file_path


def get_sprite_path(parent: str, name: str) -> Traversable:
    """Gets the path for the sprite image"""
    return get_asset_path("sprites", parent, name)


def get_tile_map_path(name: str) -> Traversable:
    """Gets the path for a tile map"""
    return get_asset_path("levels", name)
