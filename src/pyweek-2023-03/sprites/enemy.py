"""Classes for the various enemy types"""

import arcade

from .. import constants
from ..assets import get_sprite_path


class Enemy(arcade.Sprite):
    """Base enemy class from which the various enemy types are made"""

    def __init__(self, bottom, left, sprite, health: int, speed: int, weapon):
        super().__init__(sprite, constants.CHARACTER_SCALING)
        self.bottom = bottom
        self.left = left

        self.health = health
        self.speed = speed
        self.weapon = weapon


class DemoEnemy(Enemy):
    """Example enemy"""

    def __init__(self, bottom, left: tuple):
        with get_sprite_path("enemies", "realistic_enemy") as path:
            super().__init__(bottom, left, path, 100, 20, None)
