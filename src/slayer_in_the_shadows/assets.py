"""Utilities for loading assets"""

from importlib.resources import as_file, files

import arcade


def get_asset_path(*paths: str, is_as_file: bool = True):
    """Gets the path for an asset"""
    file_path = files("slayer_in_the_shadows")
    file_path = file_path.joinpath("assets")
    for path in paths:
        file_path = file_path.joinpath(path)
    return as_file(file_path) if is_as_file else file_path


def get_sprite_path(parent: str, name: str):
    """Gets the path for the sprite image"""
    return get_asset_path("sprites", parent, f"{name}.png")


def get_tile_map_path(name: str):
    """Gets the path for a tile map"""
    return get_asset_path("levels", f"{name}.tmx")


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]
