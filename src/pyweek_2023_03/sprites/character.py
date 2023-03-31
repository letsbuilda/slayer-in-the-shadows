"""Character class from"""
import arcade

# pylint: disable=no-name-in-module
from .. import constants
from ..assets import get_sprite_path
from .healthbar import HealthBar
from .attacks import AttackSpec


class Character(arcade.Sprite):
    """Base enemy class from which the various enemy types are made"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        bottom,
        left,
        sprite: str | None,
        health: int,
        speed: int,
        attacks: list[AttackSpec],
        game,
        hit_box_alg=None,
        character_scaling=constants.CHARACTER_SCALING,
    ):
        if isinstance(sprite, str):
            sprite_type, sprite_name = sprite.split("/")

            with get_sprite_path(sprite_type, sprite_name) as sprite_path:
                super().__init__(sprite_path, character_scaling, hit_box_algorithm=hit_box_alg)
        else:
            super().__init__(sprite, character_scaling, hit_box_algorithm=hit_box_alg)

        if sprite is not None:
            self.bottom = bottom
            self.left = left

        self.health = health
        self.max_health = health
        self.speed = speed
        self.attacks = attacks

        self.game = game

        self.health_bar = HealthBar(self)

    def take_damage(self, damage: int):
        """Changes health bar"""
        self.health -= damage
        self.health_bar.update_health()

    def update(self):
        """Helper"""
        self.health_bar.update()
