"""Classes for the various enemy types"""

import arcade

from .. import constants
from ..assets import get_sprite_path
from ..sprites.character import Character


class Enemy(Character):
    """Base enemy class from which the various enemy types are made"""
