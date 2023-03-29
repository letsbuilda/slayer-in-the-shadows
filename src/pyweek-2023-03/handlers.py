"""Custom handlers for things such as collisions."""

from .sprites.enemy import Enemy
from .sprites.player import Player


def player_hits_enemy(player: Player, enemy: Enemy, *args):
    if enemy.mode != 1:
        enemy.notice_player()

    # Deal damage to the player

    # Start damage cooldown

    return False