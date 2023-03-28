"""The player"""

import threading
import time

import arcade

from ..constants import PLAYER_DASH_SPEED, PLAYER_JUMP_SPEED, PLAYER_MOVEMENT_SPEED
from .character import Character


class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, sprite: str, health: int, speed: int, weapon, game):
        super().__init__(bottom, left, sprite, health, speed, weapon, game)
        self.dashes = None
        self.can_dash = None

        self.change_x = None
        self.change_y = None

    def setup_player(self):
        """Setup the player"""
        self.dashes = 1
        self.can_dash = True

        self.change_x = 0
        self.change_y = 0

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the animation"""

    def update_player_speed(self):
        """Calculate speed based on the keys pressed"""
        self.change_x = 0

        if self.game.left_key_down and not self.game.right_key_down:
            if self.game.shift_key_down and self.can_dash and self.dashes > 0:
                self.change_x = -PLAYER_DASH_SPEED
                self.dashes -= 1
                self.can_dash = False
                rThread = threading.Thread(target=self.reset_dash, daemon=True)
                rThread.start()
            else:
                self.change_x = -PLAYER_MOVEMENT_SPEED

        if self.game.right_key_down and not self.game.left_key_down:
            if self.game.shift_key_down and self.can_dash and self.dashes > 0:
                self.change_x = PLAYER_DASH_SPEED
                self.dashes -= 1
                self.can_dash = False
                rThread = threading.Thread(target=self.reset_dash, daemon=True)
                rThread.start()
            else:
                self.change_x = PLAYER_MOVEMENT_SPEED

    def reset_dash(self):
        """Reset dash after 1 second"""
        print("resetting dash")
        time.sleep(1)
        if self.dashes < 1:
            self.dashes += 1
        print("dash reset")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.game.physics_engine.can_jump():
            self.can_dash = True

        # Jump
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.game.physics_engine.can_jump():
                self.change_y = PLAYER_JUMP_SPEED

        # Dash
        # if key == arcade.key.MOD_SHIFT:
        if key == 65505:
            self.game.shift_key_down = True
            self.update_player_speed()

        # Left
        if key in (arcade.key.LEFT, arcade.key.A):
            self.game.left_key_down = True
            self.update_player_speed()

        # Right
        if key in (arcade.key.RIGHT, arcade.key.D):
            self.game.right_key_down = True
            self.update_player_speed()

    def on_key_release(self, key):
        """Called when the user releases a key."""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.game.left_key_down = False
            self.update_player_speed()

        if key in (arcade.key.RIGHT, arcade.key.D):
            self.game.right_key_down = False
            self.update_player_speed()

        if key == 65505:
            self.game.shift_key_down = False
            self.update_player_speed()
