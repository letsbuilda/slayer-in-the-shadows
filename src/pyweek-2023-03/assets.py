"""Utilities for loading assets"""

from importlib.resources import as_file, files


def get_asset_path(*paths: str):
    """Gets the path for an asset"""
    file_path = files("pyweek-2023-03")
    file_path = file_path.joinpath("assets")
    for path in paths:
        file_path = file_path.joinpath(path)
    return as_file(file_path)


def get_sprite_path(parent: str, name: str):
    """Gets the path for the sprite image"""
    return get_asset_path("sprites", parent, f"{name}.png")


def get_tile_map_path(name: str):
    """Gets the path for a tile map"""
    return get_asset_path("levels", f"{name}.tmx")
