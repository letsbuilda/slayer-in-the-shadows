"""Custom handlers for things such as collisions."""

from .constants import COLLISION_DAMAGE
from .sprites.enemy import Enemy
from .sprites.player import Player


# pylint: disable=unused-argument
def player_hits_enemy(player: Player, enemy: Enemy, *args):
    """Handles player hitting enemy"""
    if enemy.mode != 1:
        enemy.notice_player()

    # Deal damage
    player.take_damage(COLLISION_DAMAGE)
    enemy.take_damage(COLLISION_DAMAGE)

    return False
