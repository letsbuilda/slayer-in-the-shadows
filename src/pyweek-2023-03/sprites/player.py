"""The player"""

import arcade

from .. import constants
from ..assets import get_sprite_path
from ..sprites.character import Character


class Player(Character):
    """The main player"""