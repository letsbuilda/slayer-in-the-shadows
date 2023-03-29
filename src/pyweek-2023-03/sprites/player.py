"""The player"""

from ..constants import DASH_COOLDOWN, MAX_DASHES
from .character import Character


class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, sprite: str, health: int, speed: int, weapon, game):
        super().__init__(bottom, left, sprite, health, speed, weapon, game)
        self.dashes = None
        self.dash_cooldown = None
        self.is_facing_right = True

    def setup_player(self):
        """Setup the player"""
        self.dashes = MAX_DASHES
        self.dash_cooldown = 0

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the animation"""

    def use_dash(self):
        self.dashes -= 1
        self.dash_cooldown = DASH_COOLDOWN

    def on_update(self, delta_time: float = 1 / 60):
        """Reset dash after 1 second"""
        # If still on cooldown
        if self.dash_cooldown:
            self.dash_cooldown = max(self.dash_cooldown - delta_time, 0)
        # Not on cooldown
        elif self.dashes < MAX_DASHES:
            self.dashes += 1
            if self.dashes < MAX_DASHES:
                self.dash_cooldown = DASH_COOLDOWN
