"""Character class from"""
import arcade

from .. import constants
from ..assets import get_sprite_path
from .healthbar import HealthBar


class Character(arcade.Sprite):
    """Base enemy class from which the various enemy types are made"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, sprite: str, health: int, speed: int, weapon, game):
        sprite_type, sprite_name = sprite.split("/")

        with get_sprite_path(sprite_type, sprite_name) as sprite_path:
            super().__init__(sprite_path, constants.CHARACTER_SCALING)

        self.bottom = bottom
        self.left = left

        self.health = health
        self.max_health = health
        self.speed = speed
        self.weapon = weapon

        self.game = game

        self.health_bar = HealthBar(self)

    def take_damage(self, damage: int):
        """Changes health bar"""
        self.health -= damage
        self.health_bar.update_health()

    def update(self):
        """Helper"""
        self.health_bar.update()
