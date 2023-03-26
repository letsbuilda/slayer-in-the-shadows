"""The player"""

import arcade

from .. import constants
from ..assets import get_sprite_path


class Player(arcade.Sprite):
    """The main player"""

    def __init__(self, bottom, left):
        with get_sprite_path("player", "realistic_player") as sprite_path:
            super().__init__(sprite_path, constants.CHARACTER_SCALING)

        self.bottom = bottom
        self.left = left

        self.health = 100
        self.speed = 30
        self.weapon = None
