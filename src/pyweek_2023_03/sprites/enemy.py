"""Classes for the various enemy types"""

import math
from random import choice, randint

import arcade

from ..assets import get_asset_path, get_sprite_path
from ..constants import ENEMY_RENDER_DISTANCE, FRAMES_PER_RAYCAST
from .character import Character


# pylint: disable=too-many-instance-attributes
class Enemy(Character):
    """Base enemy class from which the various enemy types are made"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        bottom: float,
        left: float,
        sprite: str,
        health: int,
        speed: int,
        weapon,
        game,
    ):
        super().__init__(
            bottom, left, sprite, health, speed, weapon, game, "Detailed"
        )

        # Time (in seconds) until the enemy moves again
        self.movement_cd = randint(3, 8)

        self.raycast_cd = FRAMES_PER_RAYCAST

        # The position the enemy wants to be in, None if it likes where it is
        self.target_position = None

        self.cur_movement_cd = self.movement_cd
        self.moving = False
        self.direction = 1

        self.available_spaces = []

        # The actions an enemy will do.
        # Mode 0 is passive, the enemy wanders around the platform.
        # Mode 1 is attack, the enemy charges the player.
        self.mode = 0

        with get_asset_path("sounds", "enemy_notices.wav") as path:
            self.alert_sound = arcade.load_sound(path)

    def on_update(self, delta_time: float = 1 / 60):
        if self.mode == 0:
            if self.cur_movement_cd >= 0:
                self.cur_movement_cd -= delta_time
            else:
                self.target_position = self.find_new_spot()
                self.moving = True
                self.cur_movement_cd = self.movement_cd

    def look_for(self, player, blocks):
        """
        Checks if the player is visible to the enemy.

        This method will determine if an enemy can "see" the player. It does this with 3 checks:
        1. It checks all the blocks between the player and the enemy and determines if any interfere.
        2. It determines if the player is in the field of view. When the enemy is facing right (enemy.direction == 1),
        its field of view is from 7pi/4 to pi/4. When it's facing left (enemy.direction == -1), its FOV is modeled by
        3pi/4 to 5pi/4. If the angle between the horizontal and the player is in one of those ranges, it moves on.
        3. The player isn't too far away. The distance between the player and the enemy is less than the enemy's render
        distance.
        """

        # Check if the enemy can check the position yet to save performance
        if self.raycast_cd > 0:
            self.raycast_cd -= 1
            return False

        # Check if the distance between the player and the enemy is less than the enemy's render distance
        # and the enemy is in passive mode
        if (
            math.dist(player.position, self.position) < ENEMY_RENDER_DISTANCE
            and self.mode == 0
        ):
            if self.in_fov(player):
                self.raycast_cd = FRAMES_PER_RAYCAST
                return self.space_clear(player, blocks)
        return False

    def in_fov(self, player):
        """Check if the player is in the field of view."""
        # Use trig to find the angle between the horizontal and the player
        angle = math.atan2(
            player.center_y - self.center_y,
            player.center_x - self.center_x,
        )
        if self.direction == 1:
            if -math.pi / 4 <= angle <= math.pi / 4:
                return True
        else:
            if 3 * math.pi / 4 <= angle <= 5 * math.pi / 4:
                return True
        return False

    def notice_player(self):
        """The enemy has detected the player and will now attack."""

        self.mode = 1
        self.alert_sound.play()
        self.moving = True

    def space_clear(self, player, blocks):
        """Checks if the space is clear between an enemy and the player."""

        dx, dy = (
            player.center_x - self.center_x,
            player.center_y - self.center_y,
        )
        distance = math.sqrt(dx**2 + dy**2)
        direction = (dx / distance, dy / distance)

        # Iterate over points along the direction vector
        step_size = 30
        for i in range(0, int(distance), step_size):
            x, y = (
                self.center_x + direction[0] * i,
                self.center_y + direction[1] * i,
            )

            # Check for collisions with blocks
            for block in blocks:
                if block.collides_with_point((x, y)):
                    return False

        return True

    def find_new_spot(self):
        """Finds a new spot for the enemy to stand on when it is passive."""

        new_pos = choice(self.available_spaces)
        pos_x = new_pos.position[0] - self.position[0]
        self.direction = abs(pos_x) / pos_x
        if self.direction == 1:
            val = new_pos.left
        else:
            val = new_pos.right

        return val, self.bottom

    def generate_available_spaces(self, sprite_list):
        """Generates available spaces"""
        self.available_spaces = [
            block for block in sprite_list if block.top == self.bottom
        ]


class DemoEnemy(Enemy):
    """Example enemy"""

    def __init__(self, bottom: float, left: float, game):
        """DemoEnemy Init"""
        with get_sprite_path("enemies", "realistic_enemy") as path:
            super().__init__(bottom, left, path, 100, 20, None, game)
