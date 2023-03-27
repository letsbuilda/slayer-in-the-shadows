"""Variables that are needed in multiple files and don't change."""

# Screen
SCREEN_WIDTH = 24 * 64
SCREEN_HEIGHT = 15 * 64
SCREEN_TITLE = "pyweek-2023-03"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_DASH_SPEED = 30

# Player constants
RIGHT_FACING = 0
LEFT_FACING = 1
