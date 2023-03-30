"""The player"""

from ..constants import DASH_COOLDOWN, MAX_DASHES, SLOW_TIME_COOLDOWN, SLOW_TIME_DURATION
from .character import Character


class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, sprite: str, health: int, speed: int, weapon, game):
        super().__init__(bottom, left, sprite, health, speed, weapon, game, "Detailed")
        self.dashes = None
        self.dash_cooldown = None

        self.is_slowing_time = None
        self.slow_time_duration = None
        self.slow_time_cooldown = None

        self.is_facing_right = None
        self.is_on_ground = None
        self.force = None

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
