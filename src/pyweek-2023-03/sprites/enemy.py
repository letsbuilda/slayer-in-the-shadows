"""Classes for the various enemy types"""

from random import choice, randint

import arcade

from .. import constants
from ..assets import get_sprite_path


class Enemy(arcade.Sprite):
    """Base enemy class from which the various enemy types are made"""

    def __init__(self, bottom, left, sprite, health: int, speed: int, weapon):
        super().__init__(
            sprite, constants.CHARACTER_SCALING, hit_box_algorithm="Detailed"
        )
        self.bottom = bottom
        self.left = left

        self.health = health
        self.speed = 10
        self.weapon = weapon

        # Time (in seconds) until the enemy moves again
        self.movement_cd = randint(3, 8)

        # The position the enemy wants to be in, None if it likes where it is
        self.target_position = None

        self.cur_movement_cd = self.movement_cd
        self.moving = False
        self.direction = 0

        self.available_spaces = []

    def on_update(self, delta_time: float = 1 / 60):
        self.update_position(delta_time)

    def update_position(self, delta_time: float):
        if self.cur_movement_cd >= 0:
            self.cur_movement_cd -= delta_time
        else:
            self.target_position = self.find_new_spot()
            self.moving = True
            self.cur_movement_cd = self.movement_cd

    def find_new_spot(self):
        """Finds a new spot for the enemy to stand on when it is passive."""

        new_pos = choice(self.available_spaces)
        x = new_pos.position[0] - self.position[0]
        self.direction = abs(x) / x
        if self.direction == 1:
            val = new_pos.left
        else:
            val = new_pos.right

        return val, self.bottom

    def generate_available_spaces(self, sprite_list):
        self.available_spaces = [
            block for block in sprite_list if block.top == self.bottom
        ]


class DemoEnemy(Enemy):
    """Example enemy"""

    def __init__(self, bottom: float, left: float):
        with get_sprite_path("enemies", "realistic_enemy") as path:
            super().__init__(bottom, left, path, 100, 20, None)
