"""The player"""

import arcade

from .character import Character
from ..assets import get_sprite_path


class Player(Character):
    """The main player"""

    def __init__(self, bottom, left):
        with get_sprite_path("player", "realistic_player") as sprite_path:
            super().__init__(bottom, left, "player/realistic_player", 100, hit_box_algorithm="Detailed")

        self.bottom = bottom
        self.left = left

