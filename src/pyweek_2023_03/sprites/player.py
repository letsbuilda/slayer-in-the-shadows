"""The player"""
import arcade

from ..constants import DASH_COOLDOWN, MAX_DASHES, ANIMATION_FREEZE_TIME
from .character import Character
from ..assets import get_sprite_path


class Player(Character):
    """The main player The player sprite is 32x26"""

    # pylint: disable=too-many-arguments
    def __init__(self, bottom, left, health: int, speed: int, game):
        super().__init__(bottom, left, None, health, speed, game, character_scaling=2)
        self.jump_index = None
        self.dashes = None
        self.dash_cooldown = None
        self.is_facing_right = None
        self.is_on_ground = None
        self.force = None
        self.last_position = None
        with get_sprite_path("player", "idle") as sprite_path:
            self.idle = [[], []]
            for i in range(2):
                self.idle[i] = arcade.load_textures(sprite_path, [(j*32, 0, 32, 26) for j in range(4)], bool(i), hit_box_algorithm="Detailed")
            self.texture = self.idle[0][0]
        with get_sprite_path("player", "move") as sprite_path:
            self.move = [[], []]
            for i in range(2):
                self.move[i] = arcade.load_textures(sprite_path, [(j*36, 0, 36, 26) for j in range(3)], bool(i), hit_box_algorithm="Detailed")
        with get_sprite_path("player", "jump") as sprite_path:
            self.jump = [[], []]
            for i in range(2):
                self.jump[i] = arcade.load_textures(sprite_path, [(j*34, 0, 34, 30) for j in range(8)], bool(i), hit_box_algorithm="Detailed")

        self.bottom = bottom
        self.left = left

    def setup_player(self):
        """Setup the player"""
        self.dashes = MAX_DASHES
        self.dash_cooldown = 0
        self.is_facing_right = True
        self.is_on_ground = True
        self.force = (0, 0)
        self.jump_index = -1

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the animation"""
        if not self.jump_index >= 0:
            if self.is_on_ground:
                self.cur_texture_index += 1
                if self.cur_texture_index >= 4 * ANIMATION_FREEZE_TIME * 3:
                    self.cur_texture_index = 0
                if self.force == (0, 0):
                    self.texture = self.idle[int(not self.is_facing_right)][self.cur_texture_index // (3 * ANIMATION_FREEZE_TIME)]
                else:
                    self.texture = self.move[int(not self.is_facing_right)][self.cur_texture_index // (4 * ANIMATION_FREEZE_TIME)]
            else:
                self.texture = self.jump[int(not self.is_facing_right)][7]
        else:
            self.texture = self.jump[int(not self.is_facing_right)][self.jump_index // (ANIMATION_FREEZE_TIME+3)]
            self.jump_index += 1
            if self.jump_index >= (ANIMATION_FREEZE_TIME+3) * 5:
                self.jump_index = -1

    def use_dash(self):
        """Uses a dash"""
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
