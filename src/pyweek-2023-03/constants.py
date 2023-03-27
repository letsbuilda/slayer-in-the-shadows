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
PLAYER_JUMP_SPEED = 20

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 3_000

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1_600
PLAYER_MOVE_FORCE_ON_GROUND = 30_000
PLAYER_MOVE_FORCE_IN_AIR = 10_000
PLAYER_JUMP_IMPULSE = 1800
