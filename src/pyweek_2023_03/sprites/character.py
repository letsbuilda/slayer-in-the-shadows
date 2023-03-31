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
        hit_box_alg: str | None = None,
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

        self.attack_cooldown = 0

        self.is_invulnerable = False
        self.invulnerable_duration = 0

    def update(self):
        """Health bar"""
        self.health_bar.update()

    def on_update(self, delta_time: float = 1 / 60):
        """
        Time related cooldowns like attack and invulnerability
        """
        self.attack_cooldown = max(self.attack_cooldown - delta_time, 0)

        self.invulnerable_duration = max(self.invulnerable_duration - delta_time, 0)
        self.is_invulnerable = self.invulnerable_duration > 0
