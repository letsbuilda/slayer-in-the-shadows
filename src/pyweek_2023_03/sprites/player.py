"""The player"""
import arcade

from ..constants import (
    DASH_COOLDOWN,
    MAX_DASHES,
    SLOW_TIME_COOLDOWN,
    SLOW_TIME_DURATION,
)
from .character import Character
from ..assets import get_sprite_path


# pylint: disable=too-many-instance-attributes
class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, health: int, speed: int, game):
        super().__init__(bottom, left, None, health, speed, game)
        self.dashes = None
        self.dash_cooldown = None

        self.is_slowing_time = None
        self.slow_time_duration = None
        self.slow_time_cooldown = None

        self.is_facing_right = None
        self.is_on_ground = None
        self.force = None
        with get_sprite_path("player", "idle") as sprite_path:
            self.idle = arcade.load_spritesheet(sprite_path, 32, 26, 4, 4, hit_box_algorithm="Detailed")
            self.texture = self.idle[0]
        with get_sprite_path("player", "move") as sprite_path:
            self.move = arcade.load_spritesheet(sprite_path, 36, 26, 4, 4, hit_box_algorithm="Detailed")

        self.bottom = bottom
        self.left = left

    def setup_player(self):
        """Setup the player"""
        self.dashes = MAX_DASHES
        self.dash_cooldown = 0

        self.is_slowing_time = False
        self.slow_time_duration = 0
        self.slow_time_cooldown = 0

        self.is_facing_right = True
        self.is_on_ground = True
        self.force = (0, 0)

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the animation"""
        self.cur_texture_index += 1
        if self.cur_texture_index >= 4 * 7 * 3:
            self.cur_texture_index = 0
        if self.force == (0, 0):
            self.texture = self.idle[self.cur_texture_index // (3 * 7)]
        else:
            self.texture = self.move[self.cur_texture_index // (4 * 7)]

    def use_dash(self):
        """
        Uses a dash
        Doesn't implement it, just adjusts player values
        """
        self.dashes -= 1
        self.dash_cooldown = DASH_COOLDOWN

    def slow_time(self):
        """
        Slows time
        Doesn't implement it, just adjusts player values
        """
        self.slow_time_duration = SLOW_TIME_DURATION
        self.is_slowing_time = True

    def on_update(self, delta_time: float = 1 / 60):
        """Reset dash after 1 second"""
        # Dash
        # If still on cooldown
        if self.dash_cooldown:
            self.dash_cooldown = max(self.dash_cooldown - delta_time, 0)
        # Not on cooldown
        elif self.dashes < MAX_DASHES:
            self.dashes += 1
            if self.dashes < MAX_DASHES:
                self.dash_cooldown = DASH_COOLDOWN

        # Time slow
        if self.is_slowing_time:
            if not self.slow_time_duration:
                self.is_slowing_time = False
                self.slow_time_cooldown = SLOW_TIME_COOLDOWN
            else:
                self.slow_time_duration = max(self.slow_time_duration - delta_time, 0)
        elif self.slow_time_cooldown:
            self.slow_time_cooldown = max(self.slow_time_cooldown - delta_time, 0)
